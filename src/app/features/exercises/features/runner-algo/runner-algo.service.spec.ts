import { TestBed } from '@angular/core/testing';
import { loadNodeTypescript } from '../../../../../testing/node-typescript';
import { TS_LOADER } from '../../typescript';
import { RunnerAlgoService } from './runner-algo.service';

describe('RunnerAlgoService', () => {
  let runner: RunnerAlgoService;

  beforeEach(() => {
    TestBed.configureTestingModule({ providers: [{ provide: TS_LOADER, useValue: loadNodeTypescript }] });
    runner = TestBed.inject(RunnerAlgoService);
  });

  const code = `export function add(a: number, b: number): number { return a + b; }`;

  it('valide un code TypeScript correct, avec une durée par test', async () => {
    const { results, compileErrors } = await runner.execute(code, [{ name: 'somme', code: 'assert.equal(add(1, 2), 3)' }]);
    expect(compileErrors).toEqual([]);
    expect(results).toHaveLength(1);
    expect(results[0]).toMatchObject({ name: 'somme', passed: true });
    expect(results[0].durationMs).toBeGreaterThanOrEqual(0);
  });

  it('remonte le message d’un test en échec', async () => {
    const { results } = await runner.execute(`function add(a, b) { return a - b; }`, [{ name: 'somme', code: 'assert.equal(add(1, 2), 3)' }]);
    expect(results[0].passed).toBe(false);
    expect(results[0].message).toContain('Attendu 3, reçu -1');
  });

  it('deepEqual compare structurellement (tableaux, objets, undefined)', async () => {
    const { results } = await runner.execute('', [
      { name: 'ok', code: 'assert.deepEqual({ a: [1, { b: 2 }] }, { a: [1, { b: 2 }] })' },
      { name: 'clé undefined ≠ clé absente', code: 'assert.deepEqual({ a: undefined }, {})' },
      { name: 'ordre des tableaux', code: 'assert.deepEqual([1, 2], [2, 1])' },
    ]);
    expect(results.map((r) => r.passed)).toEqual([true, false, false]);
  });

  it('supporte les tests asynchrones et assert.rejects', async () => {
    const { results } = await runner.execute(`export const later = async () => 42; export const boom = async () => { throw new Error('x'); };`, [
      { name: 'async', code: 'assert.equal(await later(), 42)' },
      { name: 'rejects', code: 'await assert.rejects(boom())' },
      { name: 'rejects absent', code: 'await assert.rejects(later())' },
    ]);
    expect(results.map((r) => r.passed)).toEqual([true, true, false]);
  });

  it('capture console.log du code et des tests', async () => {
    await runner.execute(`console.log('chargé', [1]);`, [{ name: 't', code: `console.warn('dans le test');` }]);
    expect(runner.logs()).toEqual([
      { level: 'log', text: 'chargé [1]' },
      { level: 'warn', text: 'dans le test' },
    ]);
  });

  it('signale une erreur de syntaxe avec sa position, sans exécuter les tests', async () => {
    const report = await runner.execute('const a = 1;\nconst b = ;', [{ name: 't', code: '' }]);
    expect(report.results).toEqual([]);
    expect(report.compileErrors[0]).toMatchObject({ line: 2 });
  });

  it('échoue proprement quand les Web Workers sont indisponibles (jsdom)', async () => {
    const { results } = await runner.run(code, [{ name: 't', code: 'assert.ok(true)' }]);
    expect(results[0].passed).toBe(false);
    expect(results[0].message).toContain('Worker');
  });
});
