import { ChangeDetectionStrategy, Component, computed, inject } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { QuestionCard, QuizStore } from '@features/quiz';

@Component({
  selector: 'app-quiz-result',
  imports: [RouterLink, QuestionCard],
  templateUrl: './quiz-result.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class QuizResult {
  protected readonly store = inject(QuizStore);
  private readonly router = inject(Router);

  protected readonly percent = computed(() => {
    const total = this.store.questions().length;
    return total ? Math.round((this.store.score() / total) * 100) : 0;
  });
  protected readonly verdict = computed(() => {
    const p = this.percent();
    if (p >= 80) return 'Excellent, tu es prêt !';
    if (p >= 50) return 'Pas mal, continue à t’entraîner.';
    return 'Il reste du travail : relis les explications.';
  });
  protected readonly mistakes = computed(() => this.store.results().filter((r) => !r.correct));

  constructor() {
    if (!this.store.active()) void this.router.navigateByUrl('/quiz');
  }
}
