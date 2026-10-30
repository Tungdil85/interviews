function format(value: unknown): string {
  try {
    const json = JSON.stringify(value);
    return json === undefined ? String(value) : json;
  } catch {
    return String(value);
  }
}

export const assert = {
  equal(actual: unknown, expected: unknown, message?: string): void {
    if (actual !== expected) throw new Error(message ?? `Attendu ${format(expected)}, reçu ${format(actual)}`);
  },
  deepEqual(actual: unknown, expected: unknown, message?: string): void {
    if (format(actual) !== format(expected)) throw new Error(message ?? `Attendu ${format(expected)}, reçu ${format(actual)}`);
  },
  ok(value: unknown, message?: string): void {
    if (!value) throw new Error(message ?? `La valeur devrait être truthy, reçu ${format(value)}`);
  },
  includes(text: string, part: string, message?: string): void {
    if (!String(text).includes(part)) throw new Error(message ?? `Attendu que ${format(text)} contienne ${format(part)}`);
  },
  throws(fn: () => unknown, message?: string): void {
    try {
      fn();
    } catch {
      return;
    }
    throw new Error(message ?? 'Une exception était attendue');
  },
};
