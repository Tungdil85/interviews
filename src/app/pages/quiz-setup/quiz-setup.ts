import { ChangeDetectionStrategy, Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { ProgressService } from '@features/progress';
import { QuizService, QuizStore, type QuizMode } from '@features/quiz';
import { CATEGORIES, DIFFICULTIES, type Category, type Difficulty } from '@shared/question';

@Component({
  selector: 'app-quiz-setup',
  imports: [FormsModule],
  templateUrl: './quiz-setup.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class QuizSetup {
  private readonly quiz = inject(QuizService);
  private readonly store = inject(QuizStore);
  private readonly router = inject(Router);
  protected readonly progress = inject(ProgressService);

  protected readonly categories = CATEGORIES;
  protected readonly difficulties = DIFFICULTIES;
  protected readonly counts = [10, 20, 30, 50];

  protected readonly selectedCategories = signal<Category[]>(['angular']);
  protected readonly selectedDifficulties = signal<Difficulty[]>([]);
  protected readonly count = signal(10);
  protected readonly mode = signal<QuizMode>('practice');
  protected readonly loading = signal(false);
  protected readonly error = signal<string | null>(null);

  protected toggle<T>(list: ReturnType<typeof signal<T[]>>, value: T): void {
    list.update((l) => (l.includes(value) ? l.filter((v) => v !== value) : [...l, value]));
  }

  protected start(onlyIds?: string[]): void {
    const categories = onlyIds ? CATEGORIES.map((c) => c.id) : this.selectedCategories();
    if (categories.length === 0) {
      this.error.set('Choisis au moins une catégorie.');
      return;
    }
    this.error.set(null);
    this.loading.set(true);
    this.quiz
      .loadQuestions({
        categories,
        difficulties: onlyIds ? [] : this.selectedDifficulties(),
        count: onlyIds ? onlyIds.length : this.count(),
        onlyIds,
      })
      .subscribe({
        next: (questions) => {
          this.loading.set(false);
          if (questions.length === 0) {
            this.error.set('Aucune question ne correspond à ces critères.');
            return;
          }
          this.store.start(questions, this.mode());
          void this.router.navigateByUrl('/quiz/play');
        },
        error: () => {
          this.loading.set(false);
          this.error.set('Impossible de charger les questions.');
        },
      });
  }
}
