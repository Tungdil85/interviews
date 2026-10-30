import type { Category } from '@shared/question';

export interface SessionRecord {
  date: number;
  mode: 'practice' | 'exam';
  total: number;
  score: number;
  durationMs: number;
  byCategory: Partial<Record<Category, { total: number; correct: number }>>;
}

export interface ProgressData {
  sessions: SessionRecord[];
  /** Ids des questions actuellement ratées (retirées dès qu'elles sont réussies). */
  wrongIds: string[];
  solvedExercises: string[];
}
