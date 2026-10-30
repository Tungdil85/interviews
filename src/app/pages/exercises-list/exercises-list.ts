import { ChangeDetectionStrategy, Component, computed, inject, input } from '@angular/core';
import { toSignal } from '@angular/core/rxjs-interop';
import { RouterLink } from '@angular/router';
import { ExercisesService, type ExerciseKind } from '@features/exercises';
import { ProgressService } from '@features/progress';
import { difficultyLabel } from '@shared/question';

@Component({
  selector: 'app-exercises-list',
  imports: [RouterLink],
  templateUrl: './exercises-list.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ExercisesList {
  /** Donnée de route (`data: { kind }`) liée via withComponentInputBinding. */
  readonly kind = input<ExerciseKind>('angular');

  private readonly all = toSignal(inject(ExercisesService).list(), { initialValue: null });
  protected readonly progress = inject(ProgressService);
  protected readonly label = difficultyLabel;

  protected readonly exercises = computed(() => this.all()?.filter((e) => e.kind === this.kind()) ?? null);
  protected readonly isAlgo = computed(() => this.kind() === 'algo');
  protected readonly basePath = computed(() => (this.isAlgo() ? '/algo' : '/exercises'));
}
