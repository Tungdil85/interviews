import { Service, inject } from '@angular/core';
import { StorageService } from '@core/storage';
import { Observable, map, shareReplay } from 'rxjs';
import { ExercisesGateway } from './exercises.gateway';
import { ExercisesMapper } from './exercises.mapper';
import type { Exercise } from './models/exercise.model';

const codeKey = (id: string) => `interviews.exercise.code.${id}`;

@Service()
export class ExercisesService {
  private readonly gateway = inject(ExercisesGateway);
  private readonly mapper = inject(ExercisesMapper);
  private readonly storage = inject(StorageService);

  private readonly all$ = this.gateway.fetchAll().pipe(
    map((dtos) => dtos.map((d) => this.mapper.toExercise(d))),
    shareReplay(1),
  );

  list(): Observable<Exercise[]> {
    return this.all$;
  }

  get(id: string): Observable<Exercise | undefined> {
    return this.all$.pipe(map((list) => list.find((e) => e.id === id)));
  }

  loadCode(exercise: Exercise): string {
    return this.storage.get<string>(codeKey(exercise.id), exercise.starterCode);
  }

  saveCode(id: string, code: string): void {
    this.storage.set(codeKey(id), code);
  }

  resetCode(id: string): void {
    this.storage.remove(codeKey(id));
  }
}
