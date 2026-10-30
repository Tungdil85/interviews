import { RunnerTsService } from './runner-ts.service';

describe('RunnerTsService', () => {
  const runner = new RunnerTsService();

  it('valide un code correct', async () => {
    const results = await runner.execute('function add(a,b){return a+b}', [
      { name: 'addition', code: 'assert.equal(add(1,2), 3)' },
    ]);
    expect(results).toEqual([{ name: 'addition', passed: true }]);
  });

  it('remonte le message d’un test en échec', async () => {
    const [r] = await runner.execute('function add(a,b){return a-b}', [
      { name: 'addition', code: 'assert.equal(add(1,2), 3)' },
    ]);
    expect(r.passed).toBe(false);
    expect(r.message).toContain('Attendu 3');
  });

  it('isole chaque test et gère une erreur de syntaxe', async () => {
    const results = await runner.execute('function (', [{ name: 'x', code: 'assert.ok(true)' }]);
    expect(results[0].passed).toBe(false);
  });

  it('supporte les tests asynchrones et deepEqual / throws', async () => {
    const results = await runner.execute('const f = async () => [1,2]; const boom = () => { throw 1 }', [
      { name: 'async', code: 'assert.deepEqual(await f(), [1,2])' },
      { name: 'throws', code: 'assert.throws(boom)' },
      { name: 'throws absent', code: 'assert.throws(() => 1)' },
    ]);
    expect(results.map((r) => r.passed)).toEqual([true, true, false]);
  });

  it('rejette si les Web Workers sont indisponibles', async () => {
    const original = globalThis.Worker;
    // @ts-expect-error simulation d'un environnement sans Worker
    delete globalThis.Worker;
    await expect(runner.run('', [])).rejects.toThrow();
    globalThis.Worker = original;
  });
});
