import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { toSignal } from '@angular/core/rxjs-interop';
import { RouterLink } from '@angular/router';
import { ExercisesService } from '@features/exercises';
import { ProgressService } from '@features/progress';
import { difficultyLabel } from '@shared/question';

@Component({
  selector: 'app-exercises-list',
  imports: [RouterLink],
  templateUrl: './exercises-list.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ExercisesList {
  protected readonly exercises = toSignal(inject(ExercisesService).list(), { initialValue: null });
  protected readonly progress = inject(ProgressService);
  protected readonly label = difficultyLabel;
}
