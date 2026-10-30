import { readFileSync } from 'node:fs';
import { TestBed } from '@angular/core/testing';
import { loadNodeTypescript } from '../../../testing/node-typescript';
import type { ExerciseDto } from './dto/exercise.dto';
import { RunnerAngularService, TS_LOADER } from './features/runner-angular';

const exercises = JSON.parse(readFileSync('public/data/exercises.json', 'utf-8')) as ExerciseDto[];

describe('exercises.json', () => {
  let runner: RunnerAngularService;

  beforeEach(() => {
    TestBed.configureTestingModule({ providers: [{ provide: TS_LOADER, useValue: loadNodeTypescript }] });
    runner = TestBed.inject(RunnerAngularService);
  });

  afterEach(() => runner.clear());

  it('a des ids uniques et au moins un test par exercice', () => {
    expect(new Set(exercises.map((e) => e.id)).size).toBe(exercises.length);
    expect(exercises.every((e) => e.tests.length > 0)).toBe(true);
  });

  describe.each(exercises.map((e) => [e.id, e] as const))('%s', (_id, exercise) => {
    it('la solution passe tous les tests', { timeout: 20_000 }, async () => {
      const { results, compileErrors } = await runner.run(exercise.solution, exercise.tests);
      expect(compileErrors).toEqual([]);
      expect(results.filter((r) => !r.passed)).toEqual([]);
    });

    it('l’aperçu interactif se rend sans erreur avec la solution', { timeout: 20_000 }, async () => {
      expect(exercise.preview, 'un aperçu est attendu').toBeTruthy();
      const preview = document.createElement('div');
      document.body.appendChild(preview);
      await runner.run(exercise.solution, [], preview, exercise.preview);
      expect(runner.logs().filter((l) => l.level === 'error')).toEqual([]);
      preview.remove();
    });

    it('le code de départ compile mais ne passe pas tous les tests', { timeout: 20_000 }, async () => {
      const { results, compileErrors } = await runner.run(exercise.starterCode, exercise.tests);
      expect(compileErrors).toEqual([]);
      expect(results.every((r) => r.passed)).toBe(false);
    });
  });
});
