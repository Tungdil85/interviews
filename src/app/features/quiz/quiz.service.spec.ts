import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import type { Question } from '@shared/question';
import { QuizService } from './quiz.service';
import type { QuestionDto } from './dto/question.dto';

const dto = (id: string, difficulty: string, category = 'angular'): QuestionDto => ({
  id,
  category,
  difficulty,
  question: id,
  options: ['a', 'b'],
  answer: [0],
  explanation: '',
});

describe('QuizService', () => {
  let service: QuizService;
  let http: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({ providers: [provideHttpClient(), provideHttpClientTesting()] });
    service = TestBed.inject(QuizService);
    http = TestBed.inject(HttpTestingController);
  });

  it('filtre par difficulté et limite le nombre de questions', () => {
    let result: Question[] = [];
    service
      .loadQuestions({ categories: ['angular'], difficulties: ['easy'], count: 2 })
      .subscribe((r) => (result = r));
    http.expectOne('data/qcm-angular.json').flush([dto('1', 'easy'), dto('2', 'easy'), dto('3', 'easy'), dto('4', 'hard')]);
    expect(result).toHaveLength(2);
    expect(result.every((q) => q.difficulty === 'easy')).toBe(true);
  });

  it('fusionne plusieurs catégories', () => {
    let result: Question[] = [];
    service.loadQuestions({ categories: ['angular', 'css'], difficulties: [], count: 10 }).subscribe((r) => (result = r));
    http.expectOne('data/qcm-angular.json').flush([dto('1', 'easy')]);
    http.expectOne('data/qcm-css.json').flush([dto('2', 'easy', 'css')]);
    expect(result.map((q) => q.id).sort()).toEqual(['1', '2']);
  });

  it('restreint aux ids demandés (révision)', () => {
    let result: Question[] = [];
    service.loadQuestions({ categories: ['angular'], difficulties: [], count: 10, onlyIds: ['2'] }).subscribe((r) => (result = r));
    http.expectOne('data/qcm-angular.json').flush([dto('1', 'easy'), dto('2', 'easy')]);
    expect(result.map((q) => q.id)).toEqual(['2']);
  });

  it('refuse une liste de catégories vide', () => {
    expect(() => service.loadQuestions({ categories: [], difficulties: [], count: 5 })).toThrow();
  });

  it('compte les questions par catégorie', () => {
    let counts: Record<string, number> = {};
    service.countByCategory(['angular', 'css']).subscribe((c) => (counts = c));
    http.expectOne('data/qcm-angular.json').flush([dto('1', 'easy'), dto('2', 'easy')]);
    http.expectOne('data/qcm-css.json').flush([dto('3', 'easy', 'css')]);
    expect(counts).toEqual({ angular: 2, css: 1 });
  });

  describe('isCorrect', () => {
    const q = { correct: [0, 2] } as Question;
    it('accepte la bonne combinaison dans le désordre', () => {
      expect(service.isCorrect(q, [2, 0])).toBe(true);
    });
    it('refuse une réponse partielle ou en trop', () => {
      expect(service.isCorrect(q, [0])).toBe(false);
      expect(service.isCorrect(q, [0, 1, 2])).toBe(false);
    });
  });

  it('shuffle conserve les éléments', () => {
    expect(service.shuffle([1, 2, 3, 4]).sort()).toEqual([1, 2, 3, 4]);
  });

  it('mélange les options sans perdre les bonnes réponses', () => {
    const q = { options: ['a', 'b', 'c', 'd'], correct: [1, 3] } as Question;
    for (let i = 0; i < 20; i++) {
      const shuffled = service.shuffleOptions(q);
      expect([...shuffled.options].sort()).toEqual(['a', 'b', 'c', 'd']);
      expect(shuffled.correct.map((c) => shuffled.options[c]).sort()).toEqual(['b', 'd']);
    }
  });

  it('loadQuestions renvoie des options mélangées mais cohérentes', () => {
    let result: Question[] = [];
    service.loadQuestions({ categories: ['angular'], difficulties: [], count: 5 }).subscribe((r) => (result = r));
    http.expectOne('data/qcm-angular.json').flush([{ ...dto('1', 'easy'), options: ['bonne', 'x', 'y', 'z'], answer: [0] }]);
    expect(result[0].options[result[0].correct[0]]).toBe('bonne');
  });
});
