import { InjectionToken } from '@angular/core';
import type { CompileError } from './models/test-result.model';

/** Sous-ensemble de l'API du compilateur TypeScript utilisé pour transpiler le code des exercices. */
export interface TsApi {
  transpileModule(
    input: string,
    options: { compilerOptions: Record<string, unknown>; reportDiagnostics?: boolean },
  ): { outputText: string; diagnostics?: TsDiagnostic[] };
  ScriptTarget: { ES2022: number };
  ModuleKind: { CommonJS: number };
  flattenDiagnosticMessageText(message: unknown, newLine: string): string;
}

export interface TsDiagnostic {
  file?: { getLineAndCharacterOfPosition(position: number): { line: number; character: number } };
  start?: number;
  category: number;
  messageText: unknown;
}

const TS_URL = 'vendor/typescript.js';
let pending: Promise<TsApi> | undefined;

/** Charge typescript.js (≈ 9 Mo) à la demande, une seule fois, via une balise <script>. */
function loadFromScriptTag(): Promise<TsApi> {
  const existing = (globalThis as { ts?: TsApi }).ts;
  if (existing) return Promise.resolve(existing);
  pending ??= new Promise<TsApi>((resolve, reject) => {
    const script = document.createElement('script');
    script.src = TS_URL;
    script.onload = () => {
      const ts = (globalThis as { ts?: TsApi }).ts;
      ts ? resolve(ts) : reject(new Error('TypeScript introuvable après chargement'));
    };
    script.onerror = () => {
      pending = undefined;
      reject(new Error(`Impossible de charger ${TS_URL}`));
    };
    document.head.appendChild(script);
  });
  return pending;
}

export const TS_LOADER = new InjectionToken<() => Promise<TsApi>>('TS_LOADER', {
  providedIn: 'root',
  factory: () => loadFromScriptTag,
});

export interface CompileFailure extends Error {
  errors?: CompileError[];
}

/**
 * Transpile du TypeScript en JavaScript CommonJS (décorateurs expérimentaux, champs de classe
 * assignés dans le constructeur). Ne fait pas de vérification de types : seules les erreurs de
 * syntaxe sont remontées, avec leur position.
 */
export function transpileTypescript(ts: TsApi, code: string): string {
  const { outputText, diagnostics = [] } = ts.transpileModule(code, {
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
    const failure = new Error('Erreur de syntaxe') as CompileFailure;
    failure.errors = syntax.map((d) => {
      const position = d.file && d.start !== undefined ? d.file.getLineAndCharacterOfPosition(d.start) : undefined;
      return {
        message: ts.flattenDiagnosticMessageText(d.messageText, '\n'),
        line: position ? position.line + 1 : undefined,
        column: position ? position.character + 1 : undefined,
      };
    });
    throw failure;
  }
  return outputText;
}
