// Optional browser-code regressions; uses only the installed Node standard library.
// Run: node tests/test_demo_ui.cjs
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.resolve(__dirname, '..');
const code = fs.readFileSync(path.join(root, 'demo/portfolio.js'), 'utf8');
const payload = JSON.parse(fs.readFileSync(path.join(root, 'demo/analysis.json'), 'utf8'));

async function mount(data) {
  const listeners = {};
  const elements = new Map();
  const downloads = [];
  const blobs = [];
  const exportButtons = ['markdown', 'json'].map(format => ({
    dataset: { export: format },
    addEventListener: (_, listener) => { listeners[format] = listener; }
  }));
  const document = {
    getElementById: id => {
      if (!elements.has(id)) elements.set(id, { innerHTML: '', textContent: '', hidden: false });
      return elements.get(id);
    },
    querySelectorAll: selector => selector === '[data-export]' ? exportButtons : [],
    createElement: () => {
      const link = { click() { downloads.push({ name: this.download, url: this.href }); }, remove() {} };
      return link;
    },
    body: { appendChild() {} }
  };
  const sandbox = {
    document, console,
    window: { location: { hash: '#care' }, addEventListener() {}, setTimeout: callback => callback() },
    fetch: async () => ({ ok: true, json: async () => data }),
    Blob,
    URL: { createObjectURL: blob => { blobs.push(blob); return 'blob:synthetic-test'; }, revokeObjectURL() {} }
  };
  vm.runInNewContext(code, sandbox);
  await new Promise(resolve => setImmediate(resolve));
  return { elements, downloads, blobs, listeners };
}

(async () => {
  const mounted = await mount(payload);
  assert.match(mounted.elements.get('app').innerHTML, /Association ready to review/);
  assert.match(mounted.elements.get('chart').innerHTML, /Prior-day timing unavailable/);
  mounted.listeners.json();
  mounted.listeners.markdown();
  assert.equal(mounted.downloads[0].name, 'liveforever-care-brief-2026-07-20.json');
  assert.equal(mounted.downloads[1].name, 'liveforever-care-brief-2026-07-20.md');
  assert.deepEqual(JSON.parse(await mounted.blobs[0].text()), payload.care_brief);
  assert.equal(await mounted.blobs[1].text(), payload.exports.care_brief_markdown);
  assert.match(mounted.blobs[0].type, /application\/json/);
  assert.match(mounted.blobs[1].type, /text\/markdown/);
  const hostile = structuredClone(payload);
  hostile.care_brief.visit_question = '<img src=x onerror="window.bad=true">';
  const safe = await mount(hostile);
  assert(!safe.elements.get('app').innerHTML.includes('<img src=x'));
  assert(safe.elements.get('app').innerHTML.includes('&lt;img src=x'));
  const missing = structuredClone(payload);
  missing.analysis.timeline = [];
  missing.analysis.primary_effect.effect = null;
  missing.analysis.primary_effect.ci_low = null;
  missing.analysis.primary_effect.ci_high = null;
  missing.analysis.secondary_effects = [];
  missing.analysis.genomics_context = {};
  missing.analysis.longevity_snapshot = {};
  const empty = await mount(missing);
  assert.match(empty.elements.get('chart').innerHTML, /No recorded values/);
  assert(!empty.elements.get('app').innerHTML.includes('Demo data could not load'));
  assert(!empty.elements.get('app').innerHTML.includes('NaN'));
  const noMarkdown = structuredClone(payload);
  delete noMarkdown.exports;
  const unavailable = await mount(noMarkdown);
  unavailable.listeners.markdown();
  assert.equal(unavailable.downloads.length, 0);
  assert.match(unavailable.elements.get('export-status').textContent, /unavailable/);
  console.log('PASS: JSON/Markdown bytes and filenames, source-preserving render, escaping, missing outcomes/context, empty chart, missing export.');
})().catch(error => { console.error(error); process.exitCode = 1; });
