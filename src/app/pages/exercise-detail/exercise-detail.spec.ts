import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { RunnerAlgoService, RunnerAngularService, TS_LOADER } from '@features/exercises';
import { ProgressService } from '@features/progress';
import { loadNodeTypescript } from '../../../testing/node-typescript';
import { ExerciseDetail, LIVE_PREVIEW_DELAY_MS } from './exercise-detail';

const solution = `import { Pipe } from '@angular/core';
@Pipe({ name: 'shout' })
export class ShoutPipe { transform(v: string) { return v.toUpperCase(); } }`;

const dto = {
  id: 'e1', title: 'Pipe shout', difficulty: 'easy', topic: 'Pipe', description: 'Mets en majuscules.',
  starterCode: `import { Pipe } from '@angular/core';\n@Pipe({ name: 'shout' })\nexport class ShoutPipe { transform(v: string) { return v; } }`,
  tests: [{ name: 'majuscules', code: `const v = render('{{ t | shout }}', { imports: [ShoutPipe], props: { t: 'abc' } }); assert.equal(v.text(), 'ABC');` }],
  hints: ['indice 1'], solution,
  preview: `render('{{ "abc" | shout }}', { imports: [ShoutPipe] });`,
};

describe('ExerciseDetail', () => {
  function setup(exercise: Record<string, unknown> = dto) {
    localStorage.clear();
    TestBed.configureTestingModule({
      providers: [
        provideRouter([]),
        provideHttpClient(),
        provideHttpClientTesting(),
        { provide: TS_LOADER, useValue: loadNodeTypescript },
        { provide: LIVE_PREVIEW_DELAY_MS, useValue: 40 },
      ],
    });
    const fixture = TestBed.createComponent(ExerciseDetail);
    fixture.componentRef.setInput('id', exercise['id'] as string);
    fixture.detectChanges();
    TestBed.inject(HttpTestingController).expectOne('data/exercises.json').flush([exercise]);
    fixture.detectChanges();
    return fixture;
  }

  const button = (el: HTMLElement, label: string) =>
    Array.from(el.querySelectorAll('button')).find((b) => b.textContent?.includes(label))!;

  it('affiche l’énoncé, la zone d’aperçu, et révèle les indices progressivement', () => {
    const fixture = setup();
    const el = fixture.nativeElement as HTMLElement;
    expect(el.textContent).toContain('Mets en majuscules.');
    expect(el.querySelector('[aria-label="Aperçu du composant"]')).toBeTruthy();
    expect(el.textContent).not.toContain('indice 1');
    button(el, 'Indice').click();
    fixture.detectChanges();
    expect(el.textContent).toContain('indice 1');
  });

  it('exécute les tests : échec avec le code de départ, puis résolu avec la solution', async () => {
    const fixture = setup();
    const el = fixture.nativeElement as HTMLElement;
    const progress = TestBed.inject(ProgressService);

    button(el, 'Lancer').click();
    await vi.waitFor(() => expect(el.textContent).toContain('0 / 1 tests réussis'));
    expect(progress.solvedExercises()).toEqual([]);

    (fixture.componentInstance as unknown as { code: { set(v: string): void } }).code.set(solution);
    button(el, 'Lancer').click();
    await vi.waitFor(() => expect(el.textContent).toContain('1 / 1 tests réussis'));
    expect(progress.solvedExercises()).toEqual(['e1']);
  });

  it('détruit l’aperçu quand la page est détruite', () => {
    const fixture = setup();
    const clear = vi.spyOn(TestBed.inject(RunnerAngularService), 'clear');
    fixture.destroy();
    expect(clear).toHaveBeenCalled();
  });

  it('affiche les erreurs de compilation avec leur position, sans résultats de tests', async () => {
    const fixture = setup();
    const el = fixture.nativeElement as HTMLElement;
    (fixture.componentInstance as unknown as { code: { set(v: string): void } }).code.set('const a = ;');
    button(el, 'Lancer').click();
    await vi.waitFor(() => expect(el.textContent).toContain('1 erreur de compilation'));
    expect(el.textContent).toContain('Ligne 1');
    expect(el.textContent).toContain('Corrige les erreurs de compilation');
    expect(el.textContent).not.toContain('tests réussis');
  });

  it('affiche la console avec les logs du code exécuté', async () => {
    const fixture = setup();
    const el = fixture.nativeElement as HTMLElement;
    (fixture.componentInstance as unknown as { code: { set(v: string): void } }).code.set(`console.log('trace utilisateur');`);
    button(el, 'Lancer').click();
    await vi.waitFor(() => expect(el.querySelector('app-console-panel')?.textContent).toContain('trace utilisateur'));
  });

  describe('exercice algo', () => {
    const algo = {
      id: 'a1', kind: 'algo', durationMin: 30, title: 'Somme', difficulty: 'easy', topic: 'Tableaux', description: '**Objectif** : additionner.',
      starterCode: 'export function add(a: number, b: number): number { return 0; }',
      tests: [{ name: 'addition', code: 'assert.equal(add(1, 2), 3);' }],
      hints: [], solution: 'export function add(a: number, b: number): number { return a + b; }',
    };

    it('affiche le chrono et la durée conseillée, sans aperçu ni lien vers les exercices Angular', () => {
      const el = setup(algo).nativeElement as HTMLElement;
      expect(el.querySelector('app-chrono')).toBeTruthy();
      expect(el.textContent).toContain('30 min conseillées');
      expect(el.querySelector('[aria-label="Aperçu du composant"]')).toBeNull();
      expect(el.querySelector('a[href="/algo"]')).toBeTruthy();
    });

    it('exécute les tests avec le moteur algo et marque l’exercice résolu', async () => {
      const fixture = setup(algo);
      const el = fixture.nativeElement as HTMLElement;
      const runner = TestBed.inject(RunnerAlgoService);
      // jsdom n'a pas de Web Worker : on exécute dans le thread courant.
      vi.spyOn(runner, 'run').mockImplementation((code, tests) => runner.execute(code, tests));

      button(el, 'Lancer').click();
      await vi.waitFor(() => expect(el.textContent).toContain('0 / 1 tests réussis'));

      (fixture.componentInstance as unknown as { code: { set(v: string): void } }).code.set(algo.solution);
      button(el, 'Lancer').click();
      await vi.waitFor(() => expect(el.textContent).toContain('1 / 1 tests réussis'));
      expect(TestBed.inject(ProgressService).solvedExercises()).toEqual(['a1']);
    });
  });

  describe('aperçu interactif à la volée', () => {
    const previewText = (el: HTMLElement) => el.querySelector('.preview')?.textContent?.trim() ?? '';
    const setCode = (fixture: ReturnType<typeof setup>, code: string) =>
      (fixture.componentInstance as unknown as { code: { set(v: string): void } }).code.set(code);

    it('affiche un aperçu dès le chargement, avec le code de départ', async () => {
      const el = setup().nativeElement as HTMLElement;
      await vi.waitFor(() => expect(previewText(el)).toBe('abc'));
    });

    it('rafraîchit l’aperçu quand le code change, après le délai', async () => {
      const fixture = setup();
      const el = fixture.nativeElement as HTMLElement;
      await vi.waitFor(() => expect(previewText(el)).toBe('abc'));

      setCode(fixture, solution);
      fixture.detectChanges();
      expect(previewText(el)).toBe('abc'); // pas encore : le délai n'est pas écoulé
      await vi.waitFor(() => expect(previewText(el)).toBe('ABC'));
    });

    it('n’enchaîne qu’un seul rendu pour une rafale de modifications (debounce)', async () => {
      const fixture = setup();
      const el = fixture.nativeElement as HTMLElement;
      await vi.waitFor(() => expect(previewText(el)).toBe('abc'));
      const renderLive = vi.spyOn(TestBed.inject(RunnerAngularService), 'renderLive');

      for (const code of [`${solution}\n// 1`, `${solution}\n// 2`, `${solution}\n// 3`]) {
        setCode(fixture, code);
        fixture.detectChanges();
      }
      await vi.waitFor(() => expect(previewText(el)).toBe('ABC'));
      expect(renderLive).toHaveBeenCalledTimes(1);
    });

    it('affiche les erreurs de compilation à la volée, en gardant l’ancien aperçu', async () => {
      const fixture = setup();
      const el = fixture.nativeElement as HTMLElement;
      await vi.waitFor(() => expect(previewText(el)).toBe('abc'));

      setCode(fixture, 'const a = ;');
      fixture.detectChanges();
      await vi.waitFor(() => expect(el.textContent).toContain('1 erreur de compilation'));
      expect(previewText(el)).toBe('abc');

      setCode(fixture, solution);
      fixture.detectChanges();
      await vi.waitFor(() => expect(el.textContent).not.toContain('erreur de compilation'));
    });

    it('Réinitialiser redessine tout de suite l’aperçu avec le code de départ', async () => {
      const fixture = setup();
      const el = fixture.nativeElement as HTMLElement;
      setCode(fixture, solution);
      fixture.detectChanges();
      await vi.waitFor(() => expect(previewText(el)).toBe('ABC'));

      button(el, 'Réinitialiser').click();
      fixture.detectChanges();
      await vi.waitFor(() => expect(previewText(el)).toBe('abc'));
    });

    it('un exercice algo n’a pas d’aperçu : le moteur Angular n’est pas sollicité', async () => {
      const fixture = setup({
        id: 'a1', kind: 'algo', durationMin: 30, title: 'Somme', difficulty: 'easy', topic: 'T', description: '**Objectif** : x',
        starterCode: 'export function add() { return 0; }', tests: [], hints: [], solution: '',
      });
      const renderLive = vi.spyOn(TestBed.inject(RunnerAngularService), 'renderLive');
      await new Promise((resolve) => setTimeout(resolve, 120));
      expect(renderLive).not.toHaveBeenCalled();
      expect((fixture.nativeElement as HTMLElement).querySelector('.preview')).toBeNull();
    });
  });
});
