import { TestBed } from '@angular/core/testing';
import { ProgressService } from './progress.service';

describe('ProgressService', () => {
  let service: ProgressService;
  const base = { date: 1, mode: 'practice' as const, total: 2, score: 1, durationMs: 1000 };

  beforeEach(() => {
    localStorage.clear();
    service = TestBed.inject(ProgressService);
  });

  it('démarre vide', () => {
    expect(service.totals()).toEqual({ sessions: 0, answered: 0, correct: 0, rate: 0 });
  });

  it('enregistre une session et agrège par catégorie', () => {
    service.recordSession(base, [
      { id: 'a', category: 'angular', correct: true },
      { id: 'b', category: 'css', correct: false },
    ]);
    expect(service.totals().rate).toBe(50);
    expect(service.byCategory().css).toEqual({ total: 1, correct: 0 });
  });

  it('mémorise les erreurs puis les retire quand elles sont réussies', () => {
    service.recordSession(base, [{ id: 'b', category: 'css', correct: false }]);
    expect(service.wrongIds()).toEqual(['b']);
    service.recordSession(base, [{ id: 'b', category: 'css', correct: true }]);
    expect(service.wrongIds()).toEqual([]);
  });

  it('persiste dans le stockage', () => {
    service.markExerciseSolved('ex-1');
    service.markExerciseSolved('ex-1');
    expect(service.solvedExercises()).toEqual(['ex-1']);
    TestBed.resetTestingModule();
    expect(TestBed.inject(ProgressService).solvedExercises()).toEqual(['ex-1']);
  });

  it('reset efface tout', () => {
    service.markExerciseSolved('ex-1');
    service.reset();
    expect(service.solvedExercises()).toEqual([]);
  });
});
