/**
 * Code (texte) qui exécute UN test : il est évalué dans un Web Worker (isolé, interruptible) et, pour
 * les tests unitaires, directement dans le thread courant. Volontairement une chaîne : le worker est
 * créé depuis un Blob et ne doit dépendre d'aucun symbole du bundle.
 */
export const RUNNER_SOURCE = `
  const format = (value) => {
    if (typeof value === 'string') return value;
    if (value instanceof Error) return value.name + ': ' + value.message;
    try { const json = JSON.stringify(value); return json === undefined ? String(value) : json; } catch { return String(value); }
  };
  const isEqual = (a, b) => {
    if (Object.is(a, b)) return true;
    if (typeof a !== 'object' || typeof b !== 'object' || !a || !b) return false;
    if (Array.isArray(a) !== Array.isArray(b)) return false;
    const keysA = Object.keys(a);
    const keysB = Object.keys(b);
    return keysA.length === keysB.length && keysA.every((k) => Object.prototype.hasOwnProperty.call(b, k) && isEqual(a[k], b[k]));
  };
  async function runOne(js, test, post) {
    const log = (level) => (...args) => post({ type: 'log', level, text: args.map(format).join(' ') });
    const console = { log: log('log'), info: log('info'), debug: log('log'), warn: log('warn'), error: log('error') };
    const assert = {
      equal(actual, expected, message) {
        if (actual !== expected) throw new Error(message || 'Attendu ' + format(expected) + ', reçu ' + format(actual));
      },
      deepEqual(actual, expected, message) {
        if (!isEqual(actual, expected)) throw new Error(message || 'Attendu ' + format(expected) + ', reçu ' + format(actual));
      },
      ok(value, message) {
        if (!value) throw new Error(message || 'La valeur devrait être truthy, reçu ' + format(value));
      },
      throws(fn, message) {
        let thrown = false;
        try { fn(); } catch { thrown = true; }
        if (!thrown) throw new Error(message || 'Une exception était attendue');
      },
      async rejects(promise, message) {
        let thrown = false;
        try { await promise; } catch { thrown = true; }
        if (!thrown) throw new Error(message || 'Un rejet de promesse était attendu');
      },
    };
    const AsyncFunction = Object.getPrototypeOf(async function () {}).constructor;
    const start = performance.now();
    try {
      await new AsyncFunction('console', 'assert', 'exports', js + '\\n;' + test.code)(console, assert, {});
      post({ type: 'result', passed: true, ms: performance.now() - start });
    } catch (error) {
      const message = error && error.message ? String(error.message) : String(error);
      post({ type: 'result', passed: false, message: message.length > 400 ? message.slice(0, 400) + '…' : message, ms: performance.now() - start });
    }
  }
`;

export const WORKER_SOURCE = `${RUNNER_SOURCE}
  self.onmessage = (event) => { runOne(event.data.js, event.data.test, (message) => self.postMessage(message)); };
`;
