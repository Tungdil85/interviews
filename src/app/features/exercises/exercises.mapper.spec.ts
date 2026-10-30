import { ExercisesMapper } from './exercises.mapper';
import type { ExerciseDto } from './dto/exercise.dto';

describe('ExercisesMapper', () => {
  const dto: ExerciseDto = {
    id: 'e1',
    title: 'Titre',
    difficulty: 'medium',
    topic: 'RxJS',
    description: 'desc',
    starterCode: 'function f(){}',
    tests: [{ name: 't', code: 'assert.ok(true)' }],
    hints: ['h'],
    solution: 'sol',
  };

  it('convertit un DTO en modèle', () => {
    const e = new ExercisesMapper().toExercise(dto);
    expect(e.difficulty).toBe('medium');
    expect(e.tests).toEqual([{ name: 't', code: 'assert.ok(true)' }]);
    expect(e.hints).toEqual(['h']);
  });

  it('tolère une liste d’indices absente', () => {
    const e = new ExercisesMapper().toExercise({ ...dto, hints: undefined as unknown as string[] });
    expect(e.hints).toEqual([]);
  });
});
