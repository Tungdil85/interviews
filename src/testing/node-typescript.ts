import { readFileSync } from 'node:fs';
import type { TsApi } from '../app/features/exercises/features/runner-angular';

let cached: TsApi | undefined;

/** Charge typescript.js comme le fait le navigateur (script classique qui définit `ts`), sans passer par le DOM. */
export async function loadNodeTypescript(): Promise<TsApi> {
  cached ??= new Function(`${readFileSync('node_modules/typescript/lib/typescript.js', 'utf-8')}\nreturn ts;`)() as TsApi;
  return cached;
}
