import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { ExercisesList } from './exercises-list';

const dto = (id: string, kind: string, extra: object = {}) => ({
  id, kind, title: `Titre ${id}`, difficulty: 'medium', topic: 'Sujet', description: '', starterCode: '', tests: [], hints: [], solution: '', ...extra,
});

describe('ExercisesList', () => {
  function setup(kind?: 'angular' | 'algo') {
    localStorage.clear();
    TestBed.configureTestingModule({ providers: [provideRouter([]), provideHttpClient(), provideHttpClientTesting()] });
    const fixture = TestBed.createComponent(ExercisesList);
    if (kind) fixture.componentRef.setInput('kind', kind);
    fixture.detectChanges();
    TestBed.inject(HttpTestingController).expectOne('data/exercises.json').flush([
      dto('ng-1', 'angular'),
      dto('algo-1', 'algo', { durationMin: 30 }),
    ]);
    fixture.detectChanges();
    return fixture.nativeElement as HTMLElement;
  }

  it('liste par défaut les exercices Angular, avec des liens /exercises/:id', () => {
    const el = setup();
    expect(el.textContent).toContain('Titre ng-1');
    expect(el.textContent).not.toContain('Titre algo-1');
    expect(el.querySelector('a[href="/exercises/ng-1"]')).toBeTruthy();
  });

  it('liste les exercices algo avec leur durée, et des liens /algo/:id', () => {
    const el = setup('algo');
    expect(el.textContent).toContain('Algorithmique en TypeScript');
    expect(el.textContent).toContain('Titre algo-1');
    expect(el.textContent).toContain('30 min');
    expect(el.textContent).not.toContain('Titre ng-1');
    expect(el.querySelector('a[href="/algo/algo-1"]')).toBeTruthy();
  });
});
