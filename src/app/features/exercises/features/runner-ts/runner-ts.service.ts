import { Injectable } from '@angular/core';
import { RUNNER_BODY, WORKER_SOURCE } from './runner-source';

export interface TestCase {
  name: string;
  code: string;
}

export interface TestResult {
  name: string;
  passed: boolean;
  message?: string;
}

const AsyncFunction = Object.getPrototypeOf(async function () {}).constructor as new (
  ...args: string[]
) => (userCode: string, tests: TestCase[]) => Promise<TestResult[]>;

/** Exécute le code JavaScript de l'utilisateur contre des tests, isolé dans un Web Worker. */
@Injectable({ providedIn: 'root' })
export class RunnerTsService {
  /** Exécution directe (même thread, sans timeout) — utilisée par les tests unitaires. */
  execute(userCode: string, tests: TestCase[]): Promise<TestResult[]> {
    return new AsyncFunction('userCode', 'tests', RUNNER_BODY)(userCode, tests);
  }

  /** Exécution isolée avec timeout (protège des boucles infinies). */
  run(userCode: string, tests: TestCase[], timeoutMs = 3000): Promise<TestResult[]> {
    if (typeof Worker === 'undefined') {
      return Promise.reject(new Error('Web Worker indisponible'));
    }
    return new Promise((resolve) => {
      const url = URL.createObjectURL(new Blob([WORKER_SOURCE], { type: 'text/javascript' }));
      const worker = new Worker(url);
      const finish = (results: TestResult[]) => {
        clearTimeout(timer);
        worker.terminate();
        URL.revokeObjectURL(url);
        resolve(results);
      };
      const failAll = (message: string) => finish(tests.map((t) => ({ name: t.name, passed: false, message })));
      const timer = setTimeout(() => failAll(`Délai dépassé (${timeoutMs} ms) : boucle infinie ?`), timeoutMs);
      worker.onmessage = (event: MessageEvent<TestResult[]>) => finish(event.data);
      worker.onerror = (event) => failAll(event.message || "Erreur d'exécution");
      worker.postMessage({ userCode, tests });
    });
  }
}
