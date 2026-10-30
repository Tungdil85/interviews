/** Modules que le code des exercices peut importer (`import { … } from '@angular/core'`). */
export type ModuleRegistry = Record<string, unknown>;

let cached: Promise<ModuleRegistry> | undefined;

export function loadModules(): Promise<ModuleRegistry> {
  cached ??= (async () => {
    // Le compilateur doit être chargé avant toute définition JIT de composant.
    await import('@angular/compiler');
    const [core, interop, common, http, httpTesting, forms, rxjs, operators] = await Promise.all([
      import('@angular/core'),
      import('@angular/core/rxjs-interop'),
      import('@angular/common'),
      import('@angular/common/http'),
      import('@angular/common/http/testing'),
      import('@angular/forms'),
      import('rxjs'),
      import('rxjs/operators'),
    ]);
    return {
      '@angular/core': core,
      '@angular/core/rxjs-interop': interop,
      '@angular/common': common,
      '@angular/common/http': http,
      '@angular/common/http/testing': httpTesting,
      '@angular/forms': forms,
      rxjs,
      'rxjs/operators': operators,
    };
  })();
  return cached;
}
