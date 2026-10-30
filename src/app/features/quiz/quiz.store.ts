import { Injectable, computed, inject, signal } from '@angular/core';
import type { Question } from '@shared/question';
import { QuizService } from './quiz.service';

export type QuizMode = 'practice' | 'exam';

export interface AnswerResult {
  question: Question;
  selected: number[];
  correct: boolean;
}

@Injectable({ providedIn: 'root' })
export class QuizStore {
  private readonly service = inject(QuizService);

  readonly questions = signal<Question[]>([]);
  readonly mode = signal<QuizMode>('practice');
  readonly index = signal(0);
  readonly answers = signal<Record<string, number[]>>({});
  /** Questions dont la correction a été affichée (mode entraînement). */
  readonly revealed = signal<Set<string>>(new Set());
  readonly startedAt = signal(0);
  readonly finishedAt = signal<number | null>(null);

  readonly active = computed(() => this.questions().length > 0);
  readonly current = computed(() => this.questions()[this.index()] ?? null);
  readonly isLast = computed(() => this.index() === this.questions().length - 1);
  readonly currentSelection = computed(() => {
    const q = this.current();
    return q ? (this.answers()[q.id] ?? []) : [];
  });
  readonly isCurrentRevealed = computed(() => {
    const q = this.current();
    return !!q && this.revealed().has(q.id);
  });
  readonly results = computed<AnswerResult[]>(() =>
    this.questions().map((question) => {
      const selected = this.answers()[question.id] ?? [];
      return { question, selected, correct: this.service.isCorrect(question, selected) };
    }),
  );
  readonly score = computed(() => this.results().filter((r) => r.correct).length);
  readonly finished = computed(() => this.finishedAt() !== null);

  start(questions: Question[], mode: QuizMode): void {
    this.questions.set(questions);
    this.mode.set(mode);
    this.index.set(0);
    this.answers.set({});
    this.revealed.set(new Set());
    this.startedAt.set(Date.now());
    this.finishedAt.set(null);
  }

  toggleOption(optionIndex: number): void {
    const q = this.current();
    if (!q || this.isCurrentRevealed()) return;
    const selected = this.currentSelection();
    let next: number[];
    if (q.multiple) {
      next = selected.includes(optionIndex) ? selected.filter((i) => i !== optionIndex) : [...selected, optionIndex];
    } else {
      next = [optionIndex];
    }
    this.answers.update((a) => ({ ...a, [q.id]: next }));
  }

  /** Mode entraînement : affiche la correction de la question courante. */
  reveal(): void {
    const q = this.current();
    if (!q || this.currentSelection().length === 0) return;
    this.revealed.update((set) => new Set(set).add(q.id));
  }

  next(): void {
    if (this.isLast()) {
      this.finish();
    } else {
      this.index.update((i) => i + 1);
    }
  }

  previous(): void {
    this.index.update((i) => Math.max(0, i - 1));
  }

  finish(): void {
    if (this.finishedAt() === null) this.finishedAt.set(Date.now());
  }

  reset(): void {
    this.questions.set([]);
    this.finishedAt.set(null);
  }
}
