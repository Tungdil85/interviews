import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { QuizGateway } from './quiz.gateway';

describe('QuizGateway', () => {
  it('charge le fichier JSON de la catégorie', () => {
    TestBed.configureTestingModule({ providers: [provideHttpClient(), provideHttpClientTesting()] });
    const gateway = TestBed.inject(QuizGateway);
    const http = TestBed.inject(HttpTestingController);
    let result: unknown;

    gateway.fetchCategory('css').subscribe((r) => (result = r));
    const req = http.expectOne('data/qcm-css.json');
    expect(req.request.method).toBe('GET');
    req.flush([{ id: 'x' }]);

    expect(result).toEqual([{ id: 'x' }]);
    http.verify();
  });
});
