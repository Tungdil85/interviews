import { Service, inject } from '@angular/core';
import { Observable, forkJoin, map } from 'rxjs';
import type { Category, Difficulty, Question } from '@shared/question';
import { QuizGateway } from './quiz.gateway';
import { QuizMapper } from './quiz.mapper';

export interface QuizFilter {
  categories: Category[];
  difficulties: Difficulty[];
  count: number;
  /** Si renseigné, restreint aux questions dont l'id est dans la liste (révision des erreurs). */
  onlyIds?: string[];
}

@Service()
export class QuizService {
  private readonly gateway = inject(QuizGateway);
  private readonly mapper = inject(QuizMapper);

  loadQuestions(filter: QuizFilter): Observable<Question[]> {
    if (filter.categories.length === 0) {
      throw new Error('Au moins une catégorie est requise');
    }
    return forkJoin(filter.categories.map((c) => this.gateway.fetchCategory(c))).pipe(
      map((lists) => lists.flat().map((dto) => this.mapper.toQuestion(dto))),
      map((all) =>
        all.filter(
          (q) =>
            (filter.difficulties.length === 0 || filter.difficulties.includes(q.difficulty)) &&
            (!filter.onlyIds || filter.onlyIds.includes(q.id)),
        ),
      ),
      map((pool) => this.shuffle(pool).slice(0, filter.count).map((q) => this.shuffleOptions(q))),
    );
  }

  /** Nombre de questions disponibles par catégorie (pour l'écran de configuration). */
  countByCategory(categories: Category[]): Observable<Record<string, number>> {
    return forkJoin(categories.map((c) => this.gateway.fetchCategory(c))).pipe(
      map((lists) => Object.fromEntries(categories.map((c, i) => [c, lists[i].length]))),
    );
  }

  isCorrect(question: Question, selected: number[]): boolean {
    if (selected.length !== question.correct.length) return false;
    const sorted = [...selected].sort((a, b) => a - b);
    return question.correct.every((value, i) => value === sorted[i]);
  }

  /** Mélange l'ordre des options et recalcule les indices des bonnes réponses. */
  shuffleOptions(question: Question): Question {
    const order = this.shuffle(question.options.map((_, i) => i));
    return {
      ...question,
      options: order.map((i) => question.options[i]),
      correct: question.correct.map((c) => order.indexOf(c)).sort((a, b) => a - b),
    };
  }

  /** Fisher–Yates. */
  shuffle<T>(items: T[]): T[] {
    const copy = [...items];
    for (let i = copy.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [copy[i], copy[j]] = [copy[j], copy[i]];
    }
    return copy;
  }
}
