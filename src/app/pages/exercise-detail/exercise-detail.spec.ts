import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { RunnerTsService } from '@features/exercises';
import { ProgressService } from '@features/progress';
import { ExerciseDetail } from './exercise-detail';

const dto = {
  id: 'e1', title: 'Somme', difficulty: 'easy', topic: 'JS', description: 'Additionne.',
  starterCode: 'function add(){}', tests: [{ name: 't', code: 'assert.equal(add(1,2),3)' }],
  hints: ['indice 1'], solution: 'function add(a,b){return a+b}',
};

describe('ExerciseDetail', () => {
  function setup() {
    localStorage.clear();
    TestBed.configureTestingModule({ providers: [provideRouter([]), provideHttpClient(), provideHttpClientTesting()] });
    const fixture = TestBed.createComponent(ExerciseDetail);
    fixture.componentRef.setInput('id', 'e1');
    fixture.detectChanges();
    TestBed.inject(HttpTestingController).expectOne('data/exercises.json').flush([dto]);
    fixture.detectChanges();
    return fixture;
  }

  it('affiche l’énoncé et révèle les indices progressivement', () => {
    const fixture = setup();
    const el = fixture.nativeElement as HTMLElement;
    expect(el.textContent).toContain('Additionne.');
    expect(el.textContent).not.toContain('indice 1');
    Array.from(el.querySelectorAll('button')).find((b) => b.textContent?.includes('Indice'))!.click();
    fixture.detectChanges();
    expect(el.textContent).toContain('indice 1');
  });

  it('marque l’exercice résolu quand tous les tests passent', async () => {
    const fixture = setup();
    const runner = TestBed.inject(RunnerTsService);
    vi.spyOn(runner, 'run').mockImplementation((code, tests) => runner.execute(code, tests));
    (fixture.componentInstance as unknown as { code: { set(v: string): void } }).code.set(dto.solution);
    Array.from((fixture.nativeElement as HTMLElement).querySelectorAll('button'))
      .find((b) => b.textContent?.includes('Lancer'))!.click();
    await fixture.whenStable();
    expect(TestBed.inject(ProgressService).solvedExercises()).toEqual(['e1']);
  });
});
