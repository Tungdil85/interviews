export interface TestCase {
  name: string;
  /** Corps d'une fonction async ; voit le code de l'utilisateur et reçoit `assert`, `render`, `createInjector`, `wait`. */
  code: string;
}

export interface TestResult {
  name: string;
  passed: boolean;
  message?: string;
}

export type LogLevel = 'log' | 'info' | 'warn' | 'error';

export interface LogEntry {
  level: LogLevel;
  text: string;
}

export interface CompileError {
  message: string;
  /** Numéros 1-indexés, quand l'erreur est localisable dans le code. */
  line?: number;
  column?: number;
}

export interface RunReport {
  /** Résultats des tests ; vide si le code ne compile pas ou ne se charge pas. */
  results: TestResult[];
  compileErrors: CompileError[];
}
