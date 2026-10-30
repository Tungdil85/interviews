import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import type { Question } from '@shared/question';
import { QuizStore } from './quiz.store';

const q = (id: string, correct: number[]): Question => ({
  id,
  category: 'angular',
  difficulty: 'easy',
  text: id,
  options: ['a', 'b', 'c'],
  correct,
  multiple: correct.length > 1,
  explanation: '',
});

describe('QuizStore', () => {
  let store: QuizStore;

  beforeEach(() => {
    TestBed.configureTestingModule({ providers: [provideHttpClient(), provideHttpClientTesting()] });
    store = TestBed.inject(QuizStore);
    store.start([q('1', [1]), q('2', [0, 2])], 'practice');
  });

  it('démarre sur la première question', () => {
    expect(store.active()).toBe(true);
    expect(store.current()?.id).toBe('1');
    expect(store.finished()).toBe(false);
  });

  it('choix unique : la sélection remplace la précédente', () => {
    store.toggleOption(0);
    store.toggleOption(1);
    expect(store.currentSelection()).toEqual([1]);
  });

  it('choix multiple : bascule les options', () => {
    store.next();
    store.toggleOption(0);
    store.toggleOption(2);
    store.toggleOption(0);
    expect(store.currentSelection()).toEqual([2]);
  });

  it('reveal exige une sélection puis verrouille la question', () => {
    store.reveal();
    expect(store.isCurrentRevealed()).toBe(false);
    store.toggleOption(1);
    store.reveal();
    expect(store.isCurrentRevealed()).toBe(true);
    store.toggleOption(0);
    expect(store.currentSelection()).toEqual([1]);
  });

  it('calcule le score et termine après la dernière question', () => {
    store.toggleOption(1);
    store.next();
    store.toggleOption(0);
    store.toggleOption(2);
    expect(store.isLast()).toBe(true);
    store.next();
    expect(store.finished()).toBe(true);
    expect(store.score()).toBe(2);
  });

  it('previous ne descend pas sous 0', () => {
    store.previous();
    expect(store.index()).toBe(0);
  });

  it('reset vide la session', () => {
    store.reset();
    expect(store.active()).toBe(false);
  });
});
