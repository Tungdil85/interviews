import { ChangeDetectionStrategy, Component, OnDestroy, computed, inject, signal } from '@angular/core';
import { Router } from '@angular/router';
import { ProgressService } from '@features/progress';
import { QuestionCard, QuizStore } from '@features/quiz';

@Component({
  selector: 'app-quiz-play',
  imports: [QuestionCard],
  templateUrl: './quiz-play.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class QuizPlay implements OnDestroy {
  protected readonly store = inject(QuizStore);
  private readonly progress = inject(ProgressService);
  private readonly router = inject(Router);

  private readonly now = signal(Date.now());
  private readonly timer = setInterval(() => this.now.set(Date.now()), 1000);

  protected readonly elapsed = computed(() => {
    const total = Math.max(0, Math.floor((this.now() - this.store.startedAt()) / 1000));
    return `${Math.floor(total / 60)}:${String(total % 60).padStart(2, '0')}`;
  });
  protected readonly percent = computed(() => Math.round(((this.store.index() + 1) / this.store.questions().length) * 100));
  protected readonly isExam = computed(() => this.store.mode() === 'exam');

  constructor() {
    if (!this.store.active()) void this.router.navigateByUrl('/quiz');
  }

  ngOnDestroy(): void {
    clearInterval(this.timer);
  }

  protected next(): void {
    this.store.next();
    if (this.store.finished()) this.complete();
  }

  protected quit(): void {
    this.store.finish();
    this.complete();
  }

  private complete(): void {
    const results = this.store.results();
    const answered = results.filter((r) => r.selected.length > 0);
    if (answered.length > 0) {
      this.progress.recordSession(
        {
          date: Date.now(),
          mode: this.store.mode(),
          total: answered.length,
          score: answered.filter((r) => r.correct).length,
          durationMs: (this.store.finishedAt() ?? Date.now()) - this.store.startedAt(),
        },
        answered.map((r) => ({ id: r.question.id, category: r.question.category, correct: r.correct })),
      );
    }
    void this.router.navigateByUrl('/quiz/result');
  }
}
