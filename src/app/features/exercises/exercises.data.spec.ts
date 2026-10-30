import { readFileSync } from 'node:fs';
import { TestBed } from '@angular/core/testing';
import { loadNodeTypescript } from '../../../testing/node-typescript';
import type { ExerciseDto } from './dto/exercise.dto';
import { RunnerAlgoService } from './features/runner-algo';
import { RunnerAngularService } from './features/runner-angular';
import { TS_LOADER } from './typescript';

const exercises = JSON.parse(readFileSync('public/data/exercises.json', 'utf-8')) as ExerciseDto[];
const angular = exercises.filter((e) => e.kind === 'angular');
const algos = exercises.filter((e) => e.kind === 'algo');

describe('exercises.json', () => {
  let angularRunner: RunnerAngularService;
  let algoRunner: RunnerAlgoService;

  beforeEach(() => {
    TestBed.configureTestingModule({ providers: [{ provide: TS_LOADER, useValue: loadNodeTypescript }] });
    angularRunner = TestBed.inject(RunnerAngularService);
    algoRunner = TestBed.inject(RunnerAlgoService);
  });

  afterEach(() => angularRunner.clear());

  it('a des ids uniques, un type valide et au moins un test par exercice', () => {
    expect(new Set(exercises.map((e) => e.id)).size).toBe(exercises.length);
    expect(exercises.every((e) => e.kind === 'angular' || e.kind === 'algo')).toBe(true);
    expect(exercises.every((e) => e.tests.length > 0)).toBe(true);
    expect(algos.length).toBeGreaterThanOrEqual(10);
  });

  it('les exercices algo ont une durée conseillée de 20 à 35 minutes', () => {
    for (const e of algos) {
      expect(e.durationMin, e.id).toBeGreaterThanOrEqual(20);
      expect(e.durationMin, e.id).toBeLessThanOrEqual(35);
    }
  });

  describe.each(angular.map((e) => [e.id, e] as const))('angular · %s', (_id, exercise) => {
    it('la solution passe tous les tests', { timeout: 20_000 }, async () => {
      const { results, compileErrors } = await angularRunner.run(exercise.solution, exercise.tests);
      expect(compileErrors).toEqual([]);
      expect(results.filter((r) => !r.passed)).toEqual([]);
    });

    it('l’aperçu interactif se rend sans erreur avec la solution', { timeout: 20_000 }, async () => {
      expect(exercise.preview, 'un aperçu est attendu').toBeTruthy();
      const preview = document.createElement('div');
      document.body.appendChild(preview);
      await angularRunner.run(exercise.solution, [], preview, exercise.preview);
      expect(angularRunner.logs().filter((l) => l.level === 'error')).toEqual([]);
      preview.remove();
    });

    it('le code de départ compile mais ne passe pas tous les tests', { timeout: 20_000 }, async () => {
      const { results, compileErrors } = await angularRunner.run(exercise.starterCode, exercise.tests);
      expect(compileErrors).toEqual([]);
      expect(results.every((r) => r.passed)).toBe(false);
    });
  });

  describe.each(algos.map((e) => [e.id, e] as const))('algo · %s', (_id, exercise) => {
    it('la solution passe tous les tests, sans dépasser 5 s par test', { timeout: 60_000 }, async () => {
      const { results, compileErrors } = await algoRunner.execute(exercise.solution, exercise.tests);
      expect(compileErrors).toEqual([]);
      expect(results.filter((r) => !r.passed)).toEqual([]);
      expect(results.filter((r) => (r.durationMs ?? 0) > 2000), 'tests trop lents pour une bonne solution').toEqual([]);
    });

    it('le code de départ compile mais ne passe pas tous les tests', { timeout: 20_000 }, async () => {
      const { results, compileErrors } = await algoRunner.execute(exercise.starterCode, exercise.tests);
      expect(compileErrors).toEqual([]);
      expect(results.every((r) => r.passed)).toBe(false);
    });

    it('a une consigne structurée (objectif, exemples, à faire) et des indices', () => {
      expect(exercise.description).toContain('**Objectif**');
      expect(exercise.description).toContain('**À faire**');
      expect(exercise.hints.length).toBeGreaterThanOrEqual(2);
    });
  });
});
