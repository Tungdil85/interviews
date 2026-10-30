import type { Difficulty } from '@shared/question';

export interface ExerciseTest {
  name: string;
  /** Corps d'une fonction async ; reçoit `assert` et voit le code de l'utilisateur. */
  code: string;
}

export type ExerciseKind = 'angular' | 'algo';

export interface Exercise {
  id: string;
  kind: ExerciseKind;
  /** Durée conseillée en entretien (minutes). */
  durationMin?: number;
  title: string;
  difficulty: Difficulty;
  topic: string;
  description: string;
  starterCode: string;
  tests: ExerciseTest[];
  hints: string[];
  solution: string;
  /** Code exécuté après les tests pour afficher un exemple interactif dans l'aperçu. */
  preview: string;
}
