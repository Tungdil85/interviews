import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { QuizStore } from '@features/quiz';
import type { Question } from '@shared/question';
import { QuizResult } from './quiz-result';

const q = (id: string): Question => ({
  id, category: 'css', difficulty: 'easy', text: `Question ${id}`, options: ['a', 'b'],
  correct: [0], multiple: false, explanation: 'expl',
});

describe('QuizResult', () => {
  it('affiche le score et liste uniquement les erreurs', () => {
    TestBed.configureTestingModule({ providers: [provideRouter([]), provideHttpClient(), provideHttpClientTesting()] });
    const store = TestBed.inject(QuizStore);
    store.start([q('1'), q('2')], 'exam');
    store.toggleOption(0);
    store.next();
    store.toggleOption(1);
    store.next();

    const fixture = TestBed.createComponent(QuizResult);
    fixture.detectChanges();
    const text = (fixture.nativeElement as HTMLElement).textContent ?? '';
    expect(text).toContain('1 / 2');
    expect(text).toContain('Question 2');
    expect(text).not.toContain('Question 1');
  });
});
