import { Service } from '@angular/core';
import type { Difficulty } from '@shared/question';
import type { ExerciseDto } from './dto/exercise.dto';
import type { Exercise } from './models/exercise.model';

@Service()
export class ExercisesMapper {
  toExercise(dto: ExerciseDto): Exercise {
    return {
      id: dto.id,
      kind: dto.kind === 'algo' ? 'algo' : 'angular',
      durationMin: dto.durationMin,
      title: dto.title,
      difficulty: dto.difficulty as Difficulty,
      topic: dto.topic,
      description: dto.description,
      starterCode: dto.starterCode,
      tests: dto.tests.map((t) => ({ name: t.name, code: t.code })),
      hints: dto.hints ?? [],
      solution: dto.solution,
      preview: dto.preview ?? '',
    };
  }
}
