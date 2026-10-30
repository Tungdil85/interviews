import { EnvironmentInjector, Injectable, inject } from '@angular/core';
import type { TestCase, TestResult } from '../../models/test-result.model';
import { assert } from './assert';
import { addInitializerApiDecorators } from './initializer-apis';
import { loadModules } from './module-registry';
import { Harness, createHarness } from './test-harness';
import { TS_LOADER, TsApi } from './typescript-loader';

const AsyncFunction = Object.getPrototypeOf(async function () {}).constructor as new (
  ...args: string[]
) => (...values: unknown[]) => Promise<void>;

const wait = (ms: number) => new Promise<void>((resolve) => setTimeout(resolve, ms));

/**
 * Compile le TypeScript de l'utilisateur (transpilation + compilateur JIT d'Angular), rend ses
 * composants dans l'aperçu et exécute les tests contre le DOM obtenu.
 */
@Injectable({ providedIn: 'root' })
export class RunnerAngularService {
  private readonly injector = inject(EnvironmentInjector);
  private readonly loadTs = inject(TS_LOADER);
  private harness?: Harness;

  async run(userCode: string, tests: TestCase[], preview?: HTMLElement | null): Promise<TestResult[]> {
    this.clear();
    const fail = (message: string): TestResult[] => tests.map((t) => ({ name: t.name, passed: false, message }));

    let ts: TsApi;
    let modules: Record<string, unknown>;
    try {
      [ts, modules] = await Promise.all([this.loadTs(), loadModules()]);
    } catch (error) {
      return fail(`Chargement du moteur impossible : ${(error as Error).message}`);
    }

    let js: string;
    try {
      js = this.transpile(ts, userCode);
    } catch (error) {
      return fail((error as Error).message);
    }

    const require = (name: string) => {
      if (!(name in modules)) throw new Error(`Module non disponible : '${name}' (disponibles : ${Object.keys(modules).join(', ')})`);
      return modules[name];
    };

    const results: TestResult[] = [];
    for (const test of tests) {
      this.clear();
      if (preview) preview.replaceChildren();
      const harness = (this.harness = createHarness(this.injector, preview));
      try {
        // Le code de l'utilisateur et le test partagent la même portée : le test voit ses classes.
        await new AsyncFunction('require', 'exports', '__ng', 'assert', 'render', 'createInjector', 'wait', `${js}\n;${test.code}`)(
          require,
          {},
          modules['@angular/core'],
          assert,
          harness.render,
          harness.createInjector,
          wait,
        );
        results.push({ name: test.name, passed: true });
      } catch (error) {
        results.push({ name: test.name, passed: false, message: this.describe(error) });
      }
    }
    return results;
  }

  /** Détruit l'aperçu courant. */
  clear(): void {
    this.harness?.dispose();
    this.harness = undefined;
  }

  private transpile(ts: TsApi, code: string): string {
    const { outputText, diagnostics = [] } = ts.transpileModule(addInitializerApiDecorators(code), {
      compilerOptions: {
        target: ts.ScriptTarget.ES2022,
        module: ts.ModuleKind.CommonJS,
        experimentalDecorators: true,
        useDefineForClassFields: false,
      },
      reportDiagnostics: true,
    });
    // transpileModule ne signale que des erreurs de syntaxe (celles rattachées à un fichier).
    const syntax = diagnostics.filter((d) => d.file && d.category === 1);
    if (syntax.length > 0) {
      throw new Error(`Erreur de syntaxe : ${ts.flattenDiagnosticMessageText(syntax[0].messageText, '\n')}`);
    }
    return outputText;
  }

  private describe(error: unknown): string {
    const message = error instanceof Error ? error.message : String(error);
    return message.length > 400 ? `${message.slice(0, 400)}…` : message;
  }
}
