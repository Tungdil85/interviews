import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { ExercisesService } from './exercises.service';
import type { ExerciseDto } from './dto/exercise.dto';

const dto = (id: string): ExerciseDto => ({
  id,
  title: id,
  difficulty: 'easy',
  topic: 'JS',
  description: '',
  starterCode: 'start',
  tests: [],
  hints: [],
  solution: '',
});

describe('ExercisesService', () => {
  let service: ExercisesService;
  let http: HttpTestingController;

  beforeEach(() => {
    localStorage.clear();
    TestBed.configureTestingModule({ providers: [provideHttpClient(), provideHttpClientTesting()] });
    service = TestBed.inject(ExercisesService);
    http = TestBed.inject(HttpTestingController);
  });

  it('liste et retrouve un exercice avec une seule requête HTTP', () => {
    let found: string | undefined;
    let count = 0;
    service.list().subscribe((l) => (count = l.length));
    service.get('b').subscribe((e) => (found = e?.id));
    http.expectOne('data/exercises.json').flush([dto('a'), dto('b')]);
    expect(count).toBe(2);
    expect(found).toBe('b');
  });

  it('retourne undefined pour un id inconnu', () => {
    let result: unknown = 'init';
    service.get('zzz').subscribe((e) => (result = e));
    http.expectOne('data/exercises.json').flush([dto('a')]);
    expect(result).toBeUndefined();
  });

  it('sauvegarde, recharge et réinitialise le code', () => {
    const exercise = { id: 'a', starterCode: 'start' } as Parameters<ExercisesService['loadCode']>[0];
    expect(service.loadCode(exercise)).toBe('start');
    service.saveCode('a', 'mon code');
    expect(service.loadCode(exercise)).toBe('mon code');
    service.resetCode('a');
    expect(service.loadCode(exercise)).toBe('start');
  });
});
