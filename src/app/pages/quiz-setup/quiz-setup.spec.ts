import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { Router, provideRouter } from '@angular/router';
import { QuizStore } from '@features/quiz';
import { QuizSetup } from './quiz-setup';

describe('QuizSetup', () => {
  beforeEach(() => {
    localStorage.clear();
    TestBed.configureTestingModule({
      providers: [provideRouter([]), provideHttpClient(), provideHttpClientTesting()],
    });
  });

  it('affiche les catégories', () => {
    const fixture = TestBed.createComponent(QuizSetup);
    fixture.detectChanges();
    expect((fixture.nativeElement as HTMLElement).textContent).toContain('TypeScript');
  });

  it('charge les questions, démarre la session et navigue vers le jeu', () => {
    const fixture = TestBed.createComponent(QuizSetup);
    fixture.detectChanges();
    const navigate = vi.spyOn(TestBed.inject(Router), 'navigateByUrl').mockResolvedValue(true);
    const http = TestBed.inject(HttpTestingController);

    (fixture.nativeElement as HTMLElement).querySelector<HTMLButtonElement>('button[type="submit"]')!.click();
    http.expectOne('data/qcm-angular.json').flush([
      { id: 'a1', category: 'angular', difficulty: 'easy', question: 'Q', options: ['x', 'y'], answer: [0], explanation: '' },
    ]);

    expect(TestBed.inject(QuizStore).questions()).toHaveLength(1);
    expect(navigate).toHaveBeenCalledWith('/quiz/play');
  });

  it('signale une sélection de catégories vide', () => {
    const fixture = TestBed.createComponent(QuizSetup);
    fixture.detectChanges();
    const el = fixture.nativeElement as HTMLElement;
    el.querySelector<HTMLInputElement>('#cat-angular')!.click();
    fixture.detectChanges();
    el.querySelector<HTMLButtonElement>('button[type="submit"]')!.click();
    fixture.detectChanges();
    expect(el.querySelector('[role="alert"]')?.textContent).toContain('au moins une catégorie');
  });
});
