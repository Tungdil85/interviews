import type { Signal } from '@angular/core';
import type { LogEntry, RunReport, TestCase } from './test-result.model';

/** Contrat commun des moteurs d'exécution (exercices Angular et algos). */
export interface ExerciseRunner {
  /** Sortie console du code de l'utilisateur et des tests. */
  readonly logs: Signal<LogEntry[]>;
  /** @param preview / previewCode : zone et code d'un aperçu interactif (exercices Angular seulement). */
  run(code: string, tests: TestCase[], preview?: HTMLElement | null, previewCode?: string): Promise<RunReport>;
  /** Détruit l'aperçu courant, le cas échéant. */
  clear(): void;
  clearLogs(): void;
}
