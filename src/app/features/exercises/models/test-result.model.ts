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
