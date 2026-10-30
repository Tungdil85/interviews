import { Injectable, computed, inject, signal } from '@angular/core';
import { StorageService } from '@core/storage';
import type { Category } from '@shared/question';
import type { ProgressData, SessionRecord } from './progress.model';

const KEY = 'interviews.progress.v1';
const EMPTY: ProgressData = { sessions: [], wrongIds: [], solvedExercises: [] };

export interface QuestionOutcome {
  id: string;
  category: Category;
  correct: boolean;
}

@Injectable({ providedIn: 'root' })
export class ProgressService {
  private readonly storage = inject(StorageService);
  private readonly data = signal<ProgressData>({ ...EMPTY, ...this.storage.get<Partial<ProgressData>>(KEY, {}) });

  readonly sessions = computed(() => this.data().sessions);
  readonly wrongIds = computed(() => this.data().wrongIds);
  readonly solvedExercises = computed(() => this.data().solvedExercises);

  readonly totals = computed(() => {
    const sessions = this.data().sessions;
    const answered = sessions.reduce((n, s) => n + s.total, 0);
    const correct = sessions.reduce((n, s) => n + s.score, 0);
    return { sessions: sessions.length, answered, correct, rate: answered ? Math.round((correct / answered) * 100) : 0 };
  });

  readonly byCategory = computed(() => {
    const acc: Partial<Record<Category, { total: number; correct: number }>> = {};
    for (const s of this.data().sessions) {
      for (const [cat, v] of Object.entries(s.byCategory) as [Category, { total: number; correct: number }][]) {
        const cur = acc[cat] ?? { total: 0, correct: 0 };
        acc[cat] = { total: cur.total + v.total, correct: cur.correct + v.correct };
      }
    }
    return acc;
  });

  recordSession(session: Omit<SessionRecord, 'byCategory'>, outcomes: QuestionOutcome[]): void {
    const byCategory: SessionRecord['byCategory'] = {};
    for (const o of outcomes) {
      const cur = byCategory[o.category] ?? { total: 0, correct: 0 };
      byCategory[o.category] = { total: cur.total + 1, correct: cur.correct + (o.correct ? 1 : 0) };
    }
    const wrong = new Set(this.data().wrongIds);
    for (const o of outcomes) {
      if (o.correct) wrong.delete(o.id);
      else wrong.add(o.id);
    }
    this.update({
      ...this.data(),
      sessions: [...this.data().sessions, { ...session, byCategory }].slice(-100),
      wrongIds: [...wrong],
    });
  }

  markExerciseSolved(id: string): void {
    if (this.data().solvedExercises.includes(id)) return;
    this.update({ ...this.data(), solvedExercises: [...this.data().solvedExercises, id] });
  }

  reset(): void {
    this.update({ ...EMPTY });
  }

  private update(next: ProgressData): void {
    this.data.set(next);
    this.storage.set(KEY, next);
  }
}
