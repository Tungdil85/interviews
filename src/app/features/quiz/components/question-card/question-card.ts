import { ChangeDetectionStrategy, Component, computed, input, output } from '@angular/core';
import { categoryLabel, difficultyLabel, type Question } from '@shared/question';

@Component({
  selector: 'app-question-card',
  templateUrl: './question-card.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class QuestionCard {
  readonly question = input.required<Question>();
  readonly selected = input<number[]>([]);
  readonly revealed = input(false);
  readonly optionToggled = output<number>();

  protected readonly category = computed(() => categoryLabel(this.question().category));
  protected readonly difficulty = computed(() => difficultyLabel(this.question().difficulty));
  protected readonly letters = 'ABCDEFGH';

  protected optionClasses(index: number): string {
    const base = 'flex w-full items-start gap-3 border-2 px-4 py-3 text-left transition-colors';
    const isSelected = this.selected().includes(index);
    if (this.revealed()) {
      const isCorrect = this.question().correct.includes(index);
      if (isCorrect) return `${base} border-brand-green bg-green-50`;
      if (isSelected) return `${base} border-brand-red bg-red-50`;
      return `${base} border-gray-200 bg-white opacity-70`;
    }
    return isSelected
      ? `${base} border-primary bg-purple-50`
      : `${base} border-gray-200 bg-white hover:border-primary`;
  }

  protected feedback(index: number): string {
    if (!this.revealed()) return '';
    if (this.question().correct.includes(index)) return 'Bonne réponse';
    return this.selected().includes(index) ? 'Réponse incorrecte' : '';
  }
}
