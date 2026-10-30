import { ChangeDetectionStrategy, Component, computed, inject } from '@angular/core';
import { DatePipe } from '@angular/common';
import { RouterLink } from '@angular/router';
import { ProgressService } from '@features/progress';
import { CATEGORIES } from '@shared/question';

@Component({
  selector: 'app-progress',
  imports: [RouterLink, DatePipe],
  templateUrl: './progress.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Progress {
  protected readonly progress = inject(ProgressService);

  protected readonly rows = computed(() =>
    CATEGORIES.map((c) => {
      const v = this.progress.byCategory()[c.id] ?? { total: 0, correct: 0 };
      return { ...c, ...v, rate: v.total ? Math.round((v.correct / v.total) * 100) : 0 };
    }),
  );
  protected readonly recent = computed(() => [...this.progress.sessions()].reverse().slice(0, 10));

  protected reset(): void {
    if (confirm('Effacer toute ta progression ?')) this.progress.reset();
  }
}
