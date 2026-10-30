import { ChangeDetectionStrategy, Component, computed, effect, inject, input, signal } from '@angular/core';
import { toObservable, toSignal } from '@angular/core/rxjs-interop';
import { RouterLink } from '@angular/router';
import { switchMap } from 'rxjs';
import { CodeEditor, ExercisesService, RunnerTsService, TestResults, type TestResult } from '@features/exercises';
import { ProgressService } from '@features/progress';
import { difficultyLabel } from '@shared/question';

@Component({
  selector: 'app-exercise-detail',
  imports: [RouterLink, CodeEditor, TestResults],
  templateUrl: './exercise-detail.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ExerciseDetail {
  /** Paramètre de route `:id` (withComponentInputBinding). */
  readonly id = input.required<string>();

  private readonly exercises = inject(ExercisesService);
  private readonly runner = inject(RunnerTsService);
  private readonly progress = inject(ProgressService);

  protected readonly exercise = toSignal(toObservable(this.id).pipe(switchMap((id) => this.exercises.get(id))), {
    initialValue: undefined,
  });
  protected readonly code = signal('');
  protected readonly results = signal<TestResult[] | null>(null);
  protected readonly running = signal(false);
  protected readonly shownHints = signal(0);
  protected readonly showSolution = signal(false);
  protected readonly label = difficultyLabel;
  protected readonly solved = computed(() => this.progress.solvedExercises().includes(this.id()));

  constructor() {
    effect(() => {
      const e = this.exercise();
      if (e) {
        this.code.set(this.exercises.loadCode(e));
        this.results.set(null);
        this.shownHints.set(0);
        this.showSolution.set(false);
      }
    });
  }

  protected onCodeChange(value: string): void {
    this.code.set(value);
    this.exercises.saveCode(this.id(), value);
  }

  protected async run(): Promise<void> {
    const e = this.exercise();
    if (!e) return;
    this.running.set(true);
    try {
      const results = await this.runner.run(this.code(), e.tests);
      this.results.set(results);
      if (results.length > 0 && results.every((r) => r.passed)) this.progress.markExerciseSolved(e.id);
    } catch (error) {
      this.results.set(e.tests.map((t) => ({ name: t.name, passed: false, message: String(error) })));
    } finally {
      this.running.set(false);
    }
  }

  protected reset(): void {
    const e = this.exercise();
    if (!e) return;
    this.exercises.resetCode(e.id);
    this.code.set(e.starterCode);
    this.results.set(null);
  }
}
