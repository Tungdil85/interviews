import { EnvironmentInjector, Service, inject, signal } from '@angular/core';
import type { ExerciseRunner } from '../../models/exercise-runner.model';
import type { CompileError, LogEntry, LogLevel, RunReport, TestCase, TestResult } from '../../models/test-result.model';
import { assert } from './assert';
import { addInitializerApiDecorators } from './initializer-apis';
import { loadModules } from './module-registry';
import { Harness, createHarness } from './test-harness';
import { CompileFailure, TS_LOADER, TsApi, transpileTypescript } from '../../typescript';

const AsyncFunction = Object.getPrototypeOf(async function () {}).constructor as new (
  ...args: string[]
) => (...values: unknown[]) => Promise<void>;

type Execute = (body: string, harness?: Harness) => Promise<void>;

const wait = (ms: number) => new Promise<void>((resolve) => setTimeout(resolve, ms));
const MAX_LOGS = 300;
/** Erreurs d'Angular à présenter comme des erreurs de compilation (template invalide, propriété inconnue…). */
const ANGULAR_COMPILE_ERROR = /NG0\d{3,4}|NG\d{4}|Parser Error|Template parse|is not a known|Can't bind/;

function formatValue(value: unknown): string {
  if (typeof value === 'string') return value;
  if (value instanceof Error) return `${value.name}: ${value.message}`;
  try {
    return JSON.stringify(value) ?? String(value);
  } catch {
    return String(value);
  }
}

/**
 * Compile le TypeScript de l'utilisateur (transpilation + compilateur JIT d'Angular), rend ses
 * composants dans l'aperçu et exécute les tests contre le DOM obtenu.
 */
@Service()
export class RunnerAngularService implements ExerciseRunner {
  private readonly injector = inject(EnvironmentInjector);
  private readonly loadTs = inject(TS_LOADER);
  private harness?: Harness;
  /** Numéro du dernier rendu demandé : un rendu plus ancien que lui est abandonné. */
  private generation = 0;

  /** Sortie console du code de l'utilisateur, des tests et de l'aperçu (reste active tant que l'aperçu vit). */
  readonly logs = signal<LogEntry[]>([]);

  /**
   * Compile le code, exécute les tests, puis rend l'aperçu interactif.
   * @param previewCode code exécuté après les tests pour rendre un exemple interactif dans `preview`.
   */
  async run(userCode: string, tests: TestCase[], preview?: HTMLElement | null, previewCode?: string): Promise<RunReport> {
    this.generation++; // annule un éventuel rendu « à la volée » encore en cours
    this.clear();
    this.logs.set([]);
    preview?.replaceChildren();

    const prepared = await this.prepare(userCode);
    if ('compileErrors' in prepared) return { results: [], compileErrors: prepared.compileErrors };
    const { js, execute } = prepared;

    const onError = (error: unknown) => this.pushLog('error', formatValue(error));
    const results: TestResult[] = [];
    for (const test of tests) {
      this.clear();
      preview?.replaceChildren();
      const harness = (this.harness = createHarness(this.injector, preview, onError));
      try {
        // Le code de l'utilisateur et le test partagent la même portée : le test voit ses classes.
        await execute(`${js}\n;${test.code}`, harness);
        results.push({ name: test.name, passed: true });
      } catch (error) {
        results.push({ name: test.name, passed: false, message: this.describe(error) });
      }
    }

    const compileErrors = this.angularCompileErrors(results);
    await this.mountPreview(js, previewCode, preview, execute, onError);
    return { results, compileErrors };
  }

  /**
   * Rend seulement l'aperçu interactif (sans les tests) : sert à l'aperçu « à la volée ».
   * Si le code ne compile pas, l'ancien aperçu reste affiché et les erreurs sont renvoyées.
   *
   * @returns les erreurs de compilation (tableau vide = tout va bien), ou `null` si ce rendu a été
   * remplacé entre-temps par un plus récent (ou par un lancement des tests) : il faut alors l'ignorer.
   */
  async renderLive(userCode: string, previewCode: string, preview: HTMLElement): Promise<CompileError[] | null> {
    const generation = ++this.generation;
    this.logs.set([]);

    const prepared = await this.prepare(userCode);
    if (generation !== this.generation) return null;
    if ('compileErrors' in prepared) return prepared.compileErrors;

    const onError = (error: unknown) => this.pushLog('error', formatValue(error));
    const failure = await this.mountPreview(prepared.js, previewCode, preview, prepared.execute, onError);
    if (generation !== this.generation) return null;
    return failure && ANGULAR_COMPILE_ERROR.test(failure) ? [{ message: failure }] : [];
  }

  /** Détruit l'aperçu courant. */
  clear(): void {
    this.harness?.dispose();
    this.harness = undefined;
  }

  clearLogs(): void {
    this.logs.set([]);
  }

  /**
   * Étapes communes au lancement des tests et à l'aperçu : charger les outils, transpiler le code,
   * fabriquer l'environnement d'exécution (`require`, `console`…) et charger une première fois le module.
   */
  private async prepare(userCode: string): Promise<{ js: string; execute: Execute } | { compileErrors: CompileError[] }> {
    let ts: TsApi;
    let modules: Record<string, unknown>;
    try {
      [ts, modules] = await Promise.all([this.loadTs(), loadModules()]);
    } catch (error) {
      return { compileErrors: [{ message: `Chargement du moteur impossible : ${(error as Error).message}` }] };
    }

    let js: string;
    try {
      js = this.transpile(ts, userCode);
    } catch (error) {
      return { compileErrors: (error as CompileFailure).errors ?? [{ message: (error as Error).message }] };
    }

    const require = (name: string) => {
      if (!(name in modules)) throw new Error(`Module non disponible : '${name}' (disponibles : ${Object.keys(modules).join(', ')})`);
      return modules[name];
    };
    const console = this.createConsole();
    const execute: Execute = (body, harness) =>
      new AsyncFunction('require', 'exports', '__ng', 'console', 'assert', 'render', 'createInjector', 'wait', body)(
        require,
        {},
        modules['@angular/core'],
        console,
        assert,
        harness?.render,
        harness?.createInjector,
        wait,
      );

    // Le module de l'utilisateur doit d'abord se charger seul : une erreur ici est inutile à répéter pour chaque test.
    try {
      await execute(js);
    } catch (error) {
      return { compileErrors: [{ message: this.describe(error) }] };
    }
    return { js, execute };
  }

  /**
   * Remplace l'aperçu par le rendu de `previewCode` (le composant reste vivant, donc cliquable).
   * @returns le message de l'erreur survenue pendant le rendu, le cas échéant.
   */
  private async mountPreview(
    js: string,
    previewCode: string | undefined,
    preview: HTMLElement | null | undefined,
    execute: Execute,
    onError: (error: unknown) => void,
  ): Promise<string | undefined> {
    this.clear();
    preview?.replaceChildren();
    if (!previewCode) return undefined;
    const harness = (this.harness = createHarness(this.injector, preview, onError));
    try {
      await execute(`${js}\n;${previewCode}`, harness);
      return undefined;
    } catch (error) {
      const message = this.describe(error);
      this.pushLog('error', `Aperçu : ${message}`);
      return message;
    }
  }

  private createConsole() {
    const log = (level: LogLevel) => (...args: unknown[]) => this.pushLog(level, args.map(formatValue).join(' '));
    return { log: log('log'), info: log('info'), debug: log('log'), warn: log('warn'), error: log('error') };
  }

  private pushLog(level: LogLevel, text: string): void {
    this.logs.update((logs) => [...logs, { level, text }].slice(-MAX_LOGS));
  }

  private angularCompileErrors(results: TestResult[]): CompileError[] {
    const messages = new Set<string>();
    for (const r of results) {
      if (!r.passed && r.message && ANGULAR_COMPILE_ERROR.test(r.message)) messages.add(r.message);
    }
    return [...messages].map((message) => ({ message }));
  }

  private transpile(ts: TsApi, code: string): string {
    return transpileTypescript(ts, addInitializerApiDecorators(code));
  }

  private describe(error: unknown): string {
    const message = error instanceof Error ? error.message : String(error);
    return message.length > 400 ? `${message.slice(0, 400)}…` : message;
  }
}
