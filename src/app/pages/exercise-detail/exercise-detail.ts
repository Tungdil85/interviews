import { ChangeDetectionStrategy, Component, DestroyRef, ElementRef, computed, effect, inject, input, signal, viewChild } from '@angular/core';
import { toObservable, toSignal } from '@angular/core/rxjs-interop';
import { RouterLink } from '@angular/router';
import { switchMap } from 'rxjs';
import {
  Chrono,
  CodeEditor,
  CompileErrors,
  ConsolePanel,
  ExerciseDescription,
  ExercisesService,
  RunnerAlgoService,
  RunnerAngularService,
  TestResults,
  type CompileError,
  type ExerciseRunner,
  type TestResult,
} from '@features/exercises';
import { ProgressService } from '@features/progress';
import { difficultyLabel } from '@shared/question';

@Component({
  selector: 'app-exercise-detail',
  imports: [RouterLink, Chrono, CodeEditor, TestResults, ConsolePanel, CompileErrors, ExerciseDescription],
  templateUrl: './exercise-detail.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ExerciseDetail {
  /** Paramètre de route `:id` (withComponentInputBinding). */
  readonly id = input.required<string>();

  private readonly exercises = inject(ExercisesService);
  private readonly angularRunner = inject(RunnerAngularService);
  private readonly algoRunner = inject(RunnerAlgoService);
  private readonly progress = inject(ProgressService);
  private readonly preview = viewChild<ElementRef<HTMLElement>>('preview');

  protected readonly exercise = toSignal(toObservable(this.id).pipe(switchMap((id) => this.exercises.get(id))), {
    initialValue: undefined,
  });
  protected readonly code = signal('');
  protected readonly results = signal<TestResult[] | null>(null);
  protected readonly compileErrors = signal<CompileError[]>([]);
  /** Moteur selon le type d'exercice : composants Angular rendus, ou algo exécuté dans un Worker. */
  private readonly runner = computed<ExerciseRunner>(() => (this.exercise()?.kind === 'algo' ? this.algoRunner : this.angularRunner));
  protected readonly logs = computed(() => this.runner().logs());
  protected readonly running = signal(false);
  protected readonly shownHints = signal(0);
  protected readonly showSolution = signal(false);
  protected readonly label = difficultyLabel;
  protected readonly solved = computed(() => this.progress.solvedExercises().includes(this.id()));

  constructor() {
    inject(DestroyRef).onDestroy(() => {
      this.angularRunner.clear();
      this.algoRunner.clear();
    });
    effect(() => {
      const e = this.exercise();
      if (e) {
        this.code.set(this.exercises.loadCode(e));
        this.results.set(null);
        this.compileErrors.set([]);
        this.clearLogs();
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
      const report = await this.runner().run(this.code(), e.tests, this.preview()?.nativeElement, e.preview);
      this.compileErrors.set(report.compileErrors);
      // Sans compilation réussie, il n'y a pas de résultats de tests à afficher.
      const executed = report.results.length > 0;
      this.results.set(executed ? report.results : null);
      if (executed && report.results.every((r) => r.passed)) this.progress.markExerciseSolved(e.id);
    } finally {
      this.running.set(false);
    }
  }

  protected clearLogs(): void {
    this.angularRunner.clearLogs();
    this.algoRunner.clearLogs();
  }

  protected reset(): void {
    const e = this.exercise();
    if (!e) return;
    this.exercises.resetCode(e.id);
    this.code.set(e.starterCode);
    this.results.set(null);
    this.compileErrors.set([]);
    this.runner().clear();
    this.clearLogs();
    this.preview()?.nativeElement.replaceChildren();
  }
}
