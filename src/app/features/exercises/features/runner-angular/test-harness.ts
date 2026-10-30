import {
  ApplicationRef,
  ChangeDetectorRef,
  Component,
  ComponentRef,
  EnvironmentInjector,
  ErrorHandler,
  Provider,
  Type,
  createComponent,
  createEnvironmentInjector,
} from '@angular/core';

export interface RenderOptions {
  /** Composants / directives / pipes standalone utilisés par le template. */
  imports?: unknown[];
  providers?: Provider[];
  /** Propriétés posées sur le composant hôte (cible = template) — lisibles ensuite via `view.component`. */
  props?: Record<string, unknown>;
  /** Entrées posées via setInput (cible = classe de composant). */
  inputs?: Record<string, unknown>;
}

export interface View {
  /** Élément hôte du composant rendu. */
  el: HTMLElement;
  /** Instance du composant (ou du composant hôte pour un template). */
  component: any;
  detectChanges(): void;
  query(selector: string): HTMLElement | null;
  queryAll(selector: string): HTMLElement[];
  /** Texte normalisé (espaces compactés) de l'élément ciblé, ou de la vue entière. */
  text(selector?: string): string;
  click(selector: string): void;
  trigger(selector: string, eventName: string): void;
  /** Écrit une valeur dans un champ puis émet l'événement `input`. */
  type(selector: string, value: string): void;
  setInput(name: string, value: unknown): void;
  /** Laisse passer les tâches asynchrones en attente, puis rafraîchit. */
  stable(): Promise<void>;
}

let hostCounter = 0;
const normalize = (text: string | null) => (text ?? '').replace(/\s+/g, ' ').trim();

export interface Harness {
  render(target: string | Type<unknown>, options?: RenderOptions): View;
  createInjector(providers?: Provider[]): EnvironmentInjector;
  /** Détruit tout ce qui a été rendu (aperçu inclus). */
  dispose(): void;
}

export function createHarness(parent: EnvironmentInjector, preview?: HTMLElement | null): Harness {
  const appRef = parent.get(ApplicationRef);
  const refs: ComponentRef<unknown>[] = [];
  const errors: unknown[] = [];
  const errorProvider: Provider = { provide: ErrorHandler, useValue: { handleError: (e: unknown) => errors.push(e) } };

  const createInjector = (providers: Provider[] = []) =>
    createEnvironmentInjector([errorProvider, ...providers], parent);

  const render = (target: string | Type<unknown>, options: RenderOptions = {}): View => {
    const injector = createInjector(options.providers);
    let type: Type<unknown>;
    if (typeof target === 'string') {
      class TestHost {}
      Component({ selector: `test-host-${++hostCounter}`, template: target, imports: (options.imports ?? []) as never[] })(TestHost);
      type = TestHost;
    } else {
      type = target;
    }

    const ref = createComponent(type, { environmentInjector: injector });
    refs.push(ref);
    Object.assign(ref.instance as object, options.props ?? {});
    for (const [name, value] of Object.entries(options.inputs ?? {})) ref.setInput(name, value);

    const el = ref.location.nativeElement as HTMLElement;
    (preview ?? document.body).appendChild(el);
    appRef.attachView(ref.hostView);

    const detectChanges = () => {
      // Angular 22 : OnPush par défaut, et sans zone modifier une propriété simple ne planifie rien.
      // Pour un template de test, on marque donc le composant hôte « à vérifier » ; les composants
      // de l'utilisateur, eux, ne sont rafraîchis que si Angular les a marqués (signal, événement, setInput).
      if (typeof target === 'string') ref.injector.get(ChangeDetectorRef).markForCheck();
      appRef.tick();
      if (errors.length > 0) throw errors.shift();
    };
    const query = (selector: string) => el.querySelector<HTMLElement>(selector);
    const need = (selector: string) => {
      const found = query(selector);
      if (!found) throw new Error(`Élément introuvable : ${selector}`);
      return found;
    };

    detectChanges();

    return {
      el,
      component: ref.instance,
      detectChanges,
      query,
      queryAll: (selector) => Array.from(el.querySelectorAll<HTMLElement>(selector)),
      text: (selector) => normalize((selector ? need(selector) : el).textContent),
      click: (selector) => {
        need(selector).click();
        detectChanges();
      },
      trigger: (selector, eventName) => {
        need(selector).dispatchEvent(new Event(eventName, { bubbles: true }));
        detectChanges();
      },
      type: (selector, value) => {
        const input = need(selector) as HTMLInputElement;
        input.value = value;
        input.dispatchEvent(new Event('input', { bubbles: true }));
        detectChanges();
      },
      setInput: (name, value) => {
        ref.setInput(name, value);
        detectChanges();
      },
      stable: async () => {
        await new Promise((resolve) => setTimeout(resolve, 0));
        detectChanges();
      },
    };
  };

  const dispose = () => {
    for (const ref of refs.splice(0)) {
      appRef.detachView(ref.hostView);
      ref.destroy();
    }
  };

  return { render, createInjector, dispose };
}
