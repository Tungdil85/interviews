import type { Difficulty } from '@shared/question';

export interface ExerciseTest {
  name: string;
  /** Corps d'une fonction async ; reçoit `assert` et voit le code de l'utilisateur. */
  code: string;
}

export interface Exercise {
  id: string;
  title: string;
  difficulty: Difficulty;
  topic: string;
  description: string;
  starterCode: string;
  tests: ExerciseTest[];
  hints: string[];
  solution: string;
}
