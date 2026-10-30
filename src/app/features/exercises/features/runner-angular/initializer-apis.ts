/**
 * En compilation JIT, `input()`, `output()` et `model()` ne sont reconnus que si le champ porte les
 * décorateurs que le compilateur Angular (AOT) ajoute normalement. On les ajoute ici, en texte,
 * juste avant la transpilation. `__ng` désigne `@angular/core` (fourni par le runner).
 */
const FIELD = String.raw`^([ \t]*)((?:(?:public|protected|private|readonly|static)[ \t]+)*)(\w+)(!?)([ \t]*=[ \t]*)`;
const GENERIC = String.raw`(?:<[^()]*?>)?`;

const rules: { pattern: RegExp; decorators: (name: string) => string }[] = [
  {
    pattern: new RegExp(`${FIELD}(input\\.required)${GENERIC}\\(`, 'gm'),
    decorators: (n) => `@__ng.Input({ isSignal: true, alias: '${n}', required: true, transform: undefined }) `,
  },
  {
    pattern: new RegExp(`${FIELD}(input)${GENERIC}\\(`, 'gm'),
    decorators: (n) => `@__ng.Input({ isSignal: true, alias: '${n}', required: false, transform: undefined }) `,
  },
  {
    pattern: new RegExp(`${FIELD}(model\\.required|model)${GENERIC}\\(`, 'gm'),
    decorators: (n) =>
      `@__ng.Input({ isSignal: true, alias: '${n}', required: false, transform: undefined }) @__ng.Output('${n}Change') `,
  },
  { pattern: new RegExp(`${FIELD}(output)${GENERIC}\\(`, 'gm'), decorators: (n) => `@__ng.Output('${n}') ` },
];

export function addInitializerApiDecorators(code: string): string {
  let result = code;
  for (const { pattern, decorators } of rules) {
    result = result.replace(pattern, (match, indent: string, modifiers: string, name: string) => {
      return `${indent}${decorators(name)}${modifiers}${match.slice(indent.length + modifiers.length)}`;
    });
  }
  return result;
}
