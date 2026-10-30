import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { ExercisesGateway } from './exercises.gateway';

describe('ExercisesGateway', () => {
  it('charge exercises.json', () => {
    TestBed.configureTestingModule({ providers: [provideHttpClient(), provideHttpClientTesting()] });
    const gateway = TestBed.inject(ExercisesGateway);
    const http = TestBed.inject(HttpTestingController);
    let result: unknown;
    gateway.fetchAll().subscribe((r) => (result = r));
    const req = http.expectOne('data/exercises.json');
    expect(req.request.method).toBe('GET');
    req.flush([]);
    expect(result).toEqual([]);
  });
});
