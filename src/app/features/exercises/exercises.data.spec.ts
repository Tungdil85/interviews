import { readFileSync } from 'node:fs';
import { RunnerTsService } from './features/runner-ts';
import type { ExerciseDto } from './dto/exercise.dto';

const exercises = JSON.parse(readFileSync('public/data/exercises.json', 'utf-8')) as ExerciseDto[];
const runner = new RunnerTsService();

describe('exercises.json', () => {
  it('a des ids uniques et au moins un test par exercice', () => {
    expect(new Set(exercises.map((e) => e.id)).size).toBe(exercises.length);
    expect(exercises.every((e) => e.tests.length > 0)).toBe(true);
  });

  describe.each(exercises.map((e) => [e.id, e] as const))('%s', (_id, exercise) => {
    it('la solution passe tous les tests', async () => {
      const results = await runner.execute(exercise.solution, exercise.tests);
      const failed = results.filter((r) => !r.passed);
      expect(failed).toEqual([]);
    });

    it('le code de départ ne passe pas tous les tests', async () => {
      const results = await runner.execute(exercise.starterCode, exercise.tests);
      expect(results.every((r) => r.passed)).toBe(false);
    });
  });
});
