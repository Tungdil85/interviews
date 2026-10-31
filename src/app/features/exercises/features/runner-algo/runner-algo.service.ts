import { Service, inject, signal } from '@angular/core';
import type { ExerciseRunner } from '../../models/exercise-runner.model';
import type { CompileError, LogEntry, LogLevel, RunReport, TestCase, TestResult } from '../../models/test-result.model';
import { CompileFailure, TS_LOADER, TsApi, transpileTypescript } from '../../typescript';
import { RUNNER_SOURCE, WORKER_SOURCE } from './runner-source';

/** Au-delà, on considère la solution trop lente (ou bloquée dans une boucle infinie). */
export const TEST_TIMEOUT_MS = 5000;
const MAX_LOGS = 300;

type WorkerMessage =
  | { type: 'log'; level: LogLevel; text: string }
  | { type: 'result'; passed: boolean; message?: string; ms: number };

type RunOne = (js: string, test: TestCase, post: (message: WorkerMessage) => void) => Promise<void>;

/**
 * Exécute le TypeScript d'un exercice d'algorithmique contre ses tests. Chaque test tourne dans son
 * propre Web Worker, interrompu après {@link TEST_TIMEOUT_MS} : une boucle infinie ou une complexité
 * trop élevée échoue sans figer la page.
 */
@Service()
export class RunnerAlgoService implements ExerciseRunner {
  private readonly loadTs = inject(TS_LOADER);

  readonly logs = signal<LogEntry[]>([]);

  async run(code: string, tests: TestCase[]): Promise<RunReport> {
    // Un Worker par test, tous en parallèle : une boucle infinie coûte 5 s au total, pas 5 s par test.
    return this.runAll(code, tests, (js, test) => this.runInWorker(js, test), true);
  }

  /** Exécution directe, dans le thread courant et sans délai maximum (tests unitaires, jsdom sans Worker). */
  async execute(code: string, tests: TestCase[]): Promise<RunReport> {
    const runOne = new Function(`${RUNNER_SOURCE}\nreturn runOne;`)() as RunOne;
    return this.runAll(code, tests, (js, test) => this.runInThread(runOne, js, test), false);
  }

  clear(): void {
    // Pas d'aperçu à détruire : chaque worker est terminé à la fin de son test.
  }

  clearLogs(): void {
    this.logs.set([]);
  }

  private async runAll(
    code: string,
    tests: TestCase[],
    runTest: (js: string, test: TestCase) => Promise<TestResult>,
    parallel: boolean,
  ): Promise<RunReport> {
    this.clearLogs();
    const failed = (compileErrors: CompileError[]): RunReport => ({ results: [], compileErrors });

    let ts: TsApi;
    try {
      ts = await this.loadTs();
    } catch (error) {
      return failed([{ message: `Chargement du moteur impossible : ${(error as Error).message}` }]);
    }

    let js: string;
    try {
      js = transpileTypescript(ts, code);
    } catch (error) {
      return failed((error as CompileFailure).errors ?? [{ message: (error as Error).message }]);
    }

    if (parallel) return { results: await Promise.all(tests.map((test) => runTest(js, test))), compileErrors: [] };
    const results: TestResult[] = [];
    for (const test of tests) results.push(await runTest(js, test));
    return { results, compileErrors: [] };
  }

  private async runInThread(runOne: RunOne, js: string, test: TestCase): Promise<TestResult> {
    let result: TestResult = { name: test.name, passed: false, message: 'Aucun résultat' };
    await runOne(js, test, (message) => {
      if (message.type === 'log') this.pushLog(message.level, message.text);
      else result = this.toResult(test, message);
    });
    return result;
  }

  private runInWorker(js: string, test: TestCase): Promise<TestResult> {
    if (typeof Worker === 'undefined') {
      return Promise.resolve({ name: test.name, passed: false, message: 'Web Worker indisponible' });
    }
    return new Promise((resolve) => {
      const url = URL.createObjectURL(new Blob([WORKER_SOURCE], { type: 'text/javascript' }));
      const worker = new Worker(url);
      const finish = (result: TestResult) => {
        clearTimeout(timer);
        worker.terminate();
        URL.revokeObjectURL(url);
        resolve(result);
      };
      const timer = setTimeout(
        () =>
          finish({
            name: test.name,
            passed: false,
            message: `Délai dépassé (${TEST_TIMEOUT_MS / 1000} s) : boucle infinie ou algorithme trop lent ?`,
            durationMs: TEST_TIMEOUT_MS,
          }),
        TEST_TIMEOUT_MS,
      );
      worker.onmessage = (event: MessageEvent<WorkerMessage>) => {
        const message = event.data;
        if (message.type === 'log') this.pushLog(message.level, message.text);
        else finish(this.toResult(test, message));
      };
      worker.onerror = (event) => finish({ name: test.name, passed: false, message: event.message || "Erreur d'exécution" });
      worker.postMessage({ js, test });
    });
  }

  private toResult(test: TestCase, message: Extract<WorkerMessage, { type: 'result' }>): TestResult {
    return { name: test.name, passed: message.passed, message: message.message, durationMs: Math.round(message.ms) };
  }

  private pushLog(level: LogLevel, text: string): void {
    this.logs.update((logs) => [...logs, { level, text }].slice(-MAX_LOGS));
  }
}
