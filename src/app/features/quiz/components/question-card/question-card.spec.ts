import { TestBed } from '@angular/core/testing';
import type { Question } from '@shared/question';
import { QuestionCard } from './question-card';

const question: Question = {
  id: 'x',
  category: 'angular',
  difficulty: 'easy',
  text: 'Quelle option ?',
  options: ['un', 'deux', 'trois'],
  correct: [1],
  multiple: false,
  explanation: 'Parce que deux.',
};

describe('QuestionCard', () => {
  function setup(inputs: { selected?: number[]; revealed?: boolean } = {}) {
    const fixture = TestBed.createComponent(QuestionCard);
    fixture.componentRef.setInput('question', question);
    if (inputs.selected) fixture.componentRef.setInput('selected', inputs.selected);
    if (inputs.revealed !== undefined) fixture.componentRef.setInput('revealed', inputs.revealed);
    fixture.detectChanges();
    return fixture;
  }

  it('affiche la question et les options', () => {
    const el = setup().nativeElement as HTMLElement;
    expect(el.textContent).toContain('Quelle option ?');
    expect(el.querySelectorAll('button')).toHaveLength(3);
  });

  it('émet optionToggled au clic', () => {
    const fixture = setup();
    const emitted: number[] = [];
    fixture.componentInstance.optionToggled.subscribe((i) => emitted.push(i));
    (fixture.nativeElement as HTMLElement).querySelectorAll('button')[2].click();
    expect(emitted).toEqual([2]);
  });

  it("n'affiche l'explication qu'une fois la correction révélée", () => {
    expect(((setup().nativeElement) as HTMLElement).textContent).not.toContain('Parce que deux.');
    expect(((setup({ selected: [0], revealed: true }).nativeElement) as HTMLElement).textContent).toContain(
      'Parce que deux.',
    );
  });

  it('marque les options sélectionnées avec aria-pressed', () => {
    const buttons = (setup({ selected: [0] }).nativeElement as HTMLElement).querySelectorAll('button');
    expect(buttons[0].getAttribute('aria-pressed')).toBe('true');
    expect(buttons[1].getAttribute('aria-pressed')).toBe('false');
  });
});
