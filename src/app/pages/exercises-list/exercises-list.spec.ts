import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { ExercisesList } from './exercises-list';

describe('ExercisesList', () => {
  it('liste les exercices chargés', () => {
    localStorage.clear();
    TestBed.configureTestingModule({ providers: [provideRouter([]), provideHttpClient(), provideHttpClientTesting()] });
    const fixture = TestBed.createComponent(ExercisesList);
    fixture.detectChanges();
    TestBed.inject(HttpTestingController).expectOne('data/exercises.json').flush([
      { id: 'e1', title: 'Debounce', difficulty: 'medium', topic: 'RxJS', description: '', starterCode: '', tests: [], hints: [], solution: '' },
    ]);
    fixture.detectChanges();
    expect((fixture.nativeElement as HTMLElement).textContent).toContain('Debounce');
  });
});
