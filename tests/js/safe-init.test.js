import { test } from 'node:test';
import assert from 'node:assert/strict';
import { JSDOM } from 'jsdom';
import { safeInit } from '../../src/static/js/catalog/safe-init.js';

const html = '<div id="a" data-x></div><div id="b" data-x></div><button id="plain"></button>';
const silent = { error() {} };

test('marks each root ready after a successful init', () => {
  const { document } = new JSDOM(html).window;
  safeInit('[data-x]', (root) => root.classList.add('on'), document, silent);
  assert.equal(document.getElementById('a').dataset.scriptState, 'ready');
  assert.ok(document.getElementById('b').classList.contains('on'));
});

test('a throwing init is contained and marks only that root failed', () => {
  const { document } = new JSDOM(html).window;
  const seen = [];
  const errors = [];
  assert.doesNotThrow(() =>
    safeInit('[data-x]', (root) => {
      if (root.id === 'a') throw new Error('boom');
      seen.push(root.id);
    }, document, { error: (...a) => errors.push(a) }),
  );
  assert.equal(document.getElementById('a').dataset.scriptState, 'failed');
  assert.equal(document.getElementById('b').dataset.scriptState, 'ready');
  assert.deepEqual(seen, ['b']);
  assert.equal(errors.length, 1);
});

test('a script that never loads leaves the rest of the page functional', () => {
  const { document } = new JSDOM(html + '<div id="c" data-y></div>').window;
  // Only the data-y script loads; the data-x script's file 404ed and never ran.
  safeInit('[data-y]', () => {}, document, silent);
  assert.equal(document.getElementById('c').dataset.scriptState, 'ready');
  assert.equal(document.getElementById('a').dataset.scriptState, undefined);
  assert.equal(document.getElementById('plain').disabled, false);
});

test('no matching root is a no-op', () => {
  const { document } = new JSDOM('<p></p>').window;
  assert.doesNotThrow(() => safeInit('[data-x]', () => { throw new Error('x'); }, document, silent));
});
