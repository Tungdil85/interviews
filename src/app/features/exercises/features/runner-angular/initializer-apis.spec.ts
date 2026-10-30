import { addInitializerApiDecorators } from './initializer-apis';

describe('addInitializerApiDecorators', () => {
  it('ajoute @Input aux input() et input.required()', () => {
    const out = addInitializerApiDecorators(`  name = input('x');\n  id = input.required<number>();`);
    expect(out).toContain(`@__ng.Input({ isSignal: true, alias: 'name', required: false, transform: undefined }) name = input('x');`);
    expect(out).toContain(`@__ng.Input({ isSignal: true, alias: 'id', required: true, transform: undefined }) id = input.required<number>();`);
  });

  it('ajoute @Output aux output() génériques', () => {
    expect(addInitializerApiDecorators(`  rated = output<number>();`)).toBe(`  @__ng.Output('rated') rated = output<number>();`);
  });

  it('gère model() comme une entrée + une sortie `…Change`', () => {
    const out = addInitializerApiDecorators(`  value = model(0);`);
    expect(out).toContain(`@__ng.Output('valueChange')`);
    expect(out).toContain(`@__ng.Input({ isSignal: true, alias: 'value'`);
  });

  it('conserve les modificateurs et les génériques imbriqués', () => {
    const out = addInitializerApiDecorators(`  readonly items = input<Array<Record<string, number>>>([]);`);
    expect(out).toMatch(/^ {2}@__ng\.Input\(.*\) readonly items = input</);
  });

  it('ne touche pas aux autres champs', () => {
    const code = `  count = signal(0);\n  inputValue = 5;\n  const x = input;`;
    expect(addInitializerApiDecorators(code)).toBe(code);
  });
});
