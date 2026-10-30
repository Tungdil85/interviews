import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { Router, provideRouter } from '@angular/router';
import { QuizStore } from '@features/quiz';
import type { Question } from '@shared/question';
import { QuizPlay } from './quiz-play';

const question: Question = {
  id: 'q1', category: 'css', difficulty: 'easy', text: 'Une question', options: ['a', 'b'],
  correct: [0], multiple: false, explanation: 'ok',
};

describe('QuizPlay', () => {
  beforeEach(() => {
    localStorage.clear();
    TestBed.configureTestingModule({ providers: [provideRouter([]), provideHttpClient(), provideHttpClientTesting()] });
  });

  it('redirige vers la configuration sans session', () => {
    const navigate = vi.spyOn(TestBed.inject(Router), 'navigateByUrl').mockResolvedValue(true);
    TestBed.createComponent(QuizPlay);
    expect(navigate).toHaveBeenCalledWith('/quiz');
  });

  it('en entraînement : valider affiche la correction, puis terminer envoie au résultat', () => {
    const navigate = vi.spyOn(TestBed.inject(Router), 'navigateByUrl').mockResolvedValue(true);
    TestBed.inject(QuizStore).start([question], 'practice');
    const fixture = TestBed.createComponent(QuizPlay);
    fixture.detectChanges();
    const el = fixture.nativeElement as HTMLElement;

    el.querySelector<HTMLButtonElement>('fieldset button')!.click();
    fixture.detectChanges();
    Array.from(el.querySelectorAll('button')).find((b) => b.textContent?.includes('Valider'))!.click();
    fixture.detectChanges();
    expect(el.textContent).toContain('Explication');

    Array.from(el.querySelectorAll('button')).find((b) => b.textContent?.includes('Terminer') && !b.textContent.includes('maintenant'))!.click();
    expect(navigate).toHaveBeenCalledWith('/quiz/result');
    expect(TestBed.inject(QuizStore).score()).toBe(1);
  });
});
