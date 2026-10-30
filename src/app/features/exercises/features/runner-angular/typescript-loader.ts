import { InjectionToken } from '@angular/core';

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
  file?: unknown;
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
