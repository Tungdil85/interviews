import { Injectable } from '@angular/core';
import type { Difficulty } from '@shared/question';
import type { ExerciseDto } from './dto/exercise.dto';
import type { Exercise } from './models/exercise.model';

@Injectable({ providedIn: 'root' })
export class ExercisesMapper {
  toExercise(dto: ExerciseDto): Exercise {
    return {
      id: dto.id,
      title: dto.title,
      difficulty: dto.difficulty as Difficulty,
      topic: dto.topic,
      description: dto.description,
      starterCode: dto.starterCode,
      tests: dto.tests.map((t) => ({ name: t.name, code: t.code })),
      hints: dto.hints ?? [],
      solution: dto.solution,
    };
  }
}
