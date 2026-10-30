/**
 * Corps (texte) de la fonction async `run(userCode, tests)` exécutée soit dans un Web Worker,
 * soit directement (tests unitaires). Volontairement une chaîne : le worker est créé depuis un Blob
 * et ne doit dépendre d'aucun symbole du bundle.
 */
export const RUNNER_BODY = `
  const fmt = (v) => { try { const s = JSON.stringify(v); return s === undefined ? String(v) : s; } catch { return String(v); } };
  const assert = {
    equal(actual, expected, msg) {
      if (actual !== expected) throw new Error(msg || 'Attendu ' + fmt(expected) + ', reçu ' + fmt(actual));
    },
    deepEqual(actual, expected, msg) {
      if (fmt(actual) !== fmt(expected)) throw new Error(msg || 'Attendu ' + fmt(expected) + ', reçu ' + fmt(actual));
    },
    ok(value, msg) {
      if (!value) throw new Error(msg || 'La valeur devrait être truthy, reçu ' + fmt(value));
    },
    throws(fn, msg) {
      let thrown = false;
      try { fn(); } catch { thrown = true; }
      if (!thrown) throw new Error(msg || 'Une exception était attendue');
    },
  };
  const AsyncFunction = Object.getPrototypeOf(async function () {}).constructor;
  const results = [];
  for (const test of tests) {
    try {
      await new AsyncFunction('assert', userCode + '\\n;' + test.code)(assert);
      results.push({ name: test.name, passed: true });
    } catch (error) {
      results.push({ name: test.name, passed: false, message: error && error.message ? String(error.message) : String(error) });
    }
  }
  return results;
`;

export const WORKER_SOURCE = `
  const run = new (Object.getPrototypeOf(async function () {}).constructor)('userCode', 'tests', ${JSON.stringify(RUNNER_BODY)});
  self.onmessage = async (event) => {
    const { userCode, tests } = event.data;
    self.postMessage(await run(userCode, tests));
  };
`;
