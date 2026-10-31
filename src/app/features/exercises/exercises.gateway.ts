import { HttpClient } from '@angular/common/http';
import { Service, inject } from '@angular/core';
import { Observable } from 'rxjs';
import type { ExerciseDto } from './dto/exercise.dto';

@Service()
export class ExercisesGateway {
  private readonly http = inject(HttpClient);

  fetchAll(): Observable<ExerciseDto[]> {
    return this.http.get<ExerciseDto[]>('data/exercises.json');
  }
}
