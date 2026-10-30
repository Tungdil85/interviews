export type Category = 'angular' | 'typescript' | 'rxjs' | 'css';
export type Difficulty = 'easy' | 'medium' | 'hard';

export interface Question {
  id: string;
  category: Category;
  difficulty: Difficulty;
  text: string;
  code?: string;
  options: string[];
  /** Indices des bonnes réponses. */
  correct: number[];
  multiple: boolean;
  explanation: string;
  source?: string;
  license?: string;
}

export const CATEGORIES: { id: Category; label: string }[] = [
  { id: 'angular', label: 'Angular' },
  { id: 'typescript', label: 'TypeScript' },
  { id: 'rxjs', label: 'RxJS' },
  { id: 'css', label: 'CSS' },
];

export const DIFFICULTIES: { id: Difficulty; label: string }[] = [
  { id: 'easy', label: 'Facile' },
  { id: 'medium', label: 'Moyen' },
  { id: 'hard', label: 'Difficile' },
];

export function categoryLabel(id: Category): string {
  return CATEGORIES.find((c) => c.id === id)?.label ?? id;
}

export function difficultyLabel(id: Difficulty): string {
  return DIFFICULTIES.find((d) => d.id === id)?.label ?? id;
}
