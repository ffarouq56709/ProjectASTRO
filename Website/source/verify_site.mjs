// Website logic checks for ASTRO 365 R0.3 (no browser, no robot). Run: node verify_site.mjs
import fs from 'node:fs/promises';
import vm from 'node:vm';
import assert from 'node:assert/strict';
const data = JSON.parse(await fs.readFile(new URL('./dist/plan.json', import.meta.url), 'utf8'));
const app = await fs.readFile(new URL('./dist/app.js', import.meta.url), 'utf8');
const checks = [];
const check = (name, fn) => { fn(); checks.push({ name, result: 'PASS' }); };
const els = new Map();
const el = id => { if (!els.has(id)) els.set(id, { textContent: '', innerHTML: '', value: '', style: {}, classList: { add() {}, remove() {}, toggle() {} }, addEventListener() {}, focus() {}, close() {}, showModal() {} }); return els.get(id); };
const local = new Map();
const ctx = { console, Date, Intl, Number, Math, String, Object, Array, Set, JSON, URL, Blob, Promise, Error,
  setTimeout() { return 0; }, clearTimeout() {}, location: { hash: '#day/1' }, history: { replaceState() {} }, navigator: {},
  document: { getElementById: id => id === 'embedded-plan' ? null : el(id), addEventListener() {}, querySelector: () => el('sidebar'), createElement: () => ({ click() {}, remove() {} }), body: { append() {} } },
  localStorage: { setItem: (k, v) => local.set(k, v), getItem: k => local.get(k) || null },
  fetch: () => new Promise(() => {}) };
ctx.window = ctx; ctx.window.addEventListener = () => {}; ctx.window.scrollTo = () => {};
class FD { constructor(o) { this.o = o; } get(k) { return this.o[k] ?? ''; } }
ctx.FormData = FD;
vm.runInNewContext(app, ctx, { timeout: 5000 });
const api = ctx.window.__astro;
let s = api.init(data);
const reqIds = new Set(data.requirements.map(r => r[0]));
check('365 sequential days', () => assert.deepEqual(data.days.map(d => d.id), Array.from({ length: 365 }, (_, i) => i + 1)));
check('Unique titles and output paths', () => { assert.equal(new Set(data.days.map(d => d.title)).size, 365); assert.equal(new Set(data.days.map(d => d.output)).size, 365); });
check('Every day has 2-8 steps, 2-4 checks, a goal and inputs', () => assert(data.days.every(d => d.steps.length >= 2 && d.steps.length <= 8 && d.acceptance.length >= 2 && d.acceptance.length <= 4 && d.goal.length > 20 && d.inputs.length >= 1)));
check('Step minutes add up per day', () => assert(data.days.every(d => d.stepMinutes.reduce((a, b) => a + b, 0) === d.minutes)));
check('Planned time fits 2-3 h days (90-180 min)', () => assert(data.days.every(d => d.minutes >= 90 && d.minutes <= 180)));
const old = JSON.parse(await fs.readFile(new URL('./source_r02_plan.json', import.meta.url), 'utf8'));
check('Weeks, gates and stages unchanged from R0.2', () => assert(data.days.every((d, i) => d.week === old.days[i].week && JSON.stringify(d.gates) === JSON.stringify(old.days[i].gates) && JSON.stringify(d.stages) === JSON.stringify(old.days[i].stages))));
check('Requirement, gate and stage links exist', () => assert(data.days.every(d => d.requirements.every(r => reqIds.has(r)) && d.gates.every(g => data.gates.some(x => x.id === g)) && d.stages.every(g => data.stages.some(x => x.id === g)))));
check('Dependencies point backwards', () => assert(data.days.every(d => d.dependencyDays.every(k => k < d.id))));
check('Powered days name outside help', () => assert(data.days.filter(d => d.kind === 'powered').every(d => d.help && d.help.length > 20)));
check('Nothing passes at start', () => { assert.equal(api.dayCount(), 0); assert(data.gates.every(g => !api.gateSatisfied(g.id))); });
check('Initial actuator forecast uses the R0.3 listing screen', () => assert.equal(api.budgetTotals().forecast, 7000 + 3481));
const submit = (result, n) => { api.setDay(n); api.saveDay({ preventDefault() {}, target: { result, evidence: 'TEST ONLY', hours: '2', reviewer: 'TEST' } }); };
check('PASS needs every step and check', () => { submit('PASS', 1); assert.equal(api.dayState(1).result, ''); });
check('Variable-length steps record PASS when complete', () => { const r = api.dayState(1); r.steps.fill(true); r.checks.fill(true); submit('PASS', 1); assert.equal(api.dayState(1).result, 'PASS', el('outcome-error').textContent); });
check('Physical day cannot PASS without releases', () => { const r = api.dayState(302); r.steps.fill(true); r.checks.fill(true); submit('PASS', 302); assert.equal(r.result, ''); });
check('Hardware PASS needs releases', () => { api.setDay(304); api.saveHw({ preventDefault() {}, target: { result: 'PASS', run: 'X', date: '2026-10-27', notes: '' } }); assert.equal(api.dayState(304).hw.result, ''); });
check('Hardware FAIL can be recorded and is separate from the task record', () => { api.setDay(304); api.saveHw({ preventDefault() {}, target: { result: 'STOPPED', run: 'S14-RUN-01', date: '2026-10-27', notes: 'test' } }); const r = api.dayState(304); assert.equal(r.hw.result, 'STOPPED'); assert.equal(r.result, ''); });
check('R0.2 records migrate: outcome and notes kept, old ticks set aside', () => {
  const st = api.S; st.days[6] = { steps: [true, true, true, true, true, true], checks: [true, true, true], notes: 'old note', result: 'REWORK', evidence: 'day_006', reviewer: 'Owner', hours: 2, recordedAt: '2026-10-28T18:00:00Z', history: [] };
  const r = api.dayState(6); assert.equal(r.result, 'REWORK'); assert.equal(r.notes, 'old note'); assert.equal(r.hours, 2); assert.equal(r.legacy.rev, 'R0.2'); assert.equal(r.steps.length, data.days[5].steps.length); assert(!r.steps.some(Boolean)); });
check('R0.2 backup imports', () => { const n = api.sanitizeImport({ format: 'astro365-progress', version: 2, state: { version: 2, start: '2026-10-24', days: { 5: { steps: [true, true, true, true, true, true], checks: [true, true, true], result: 'PASS', evidence: 'day_005', hours: 2.5, notes: 'n' } } } }); assert.equal(n.days['5'].result, 'PASS'); assert.equal(n.days['5'].planRev, 'R0.2'); });
check('Unsupported backup rejected', () => assert.throws(() => api.sanitizeImport({ version: 1 })));
check('Escaping works', () => assert.equal(api.esc('<b>'), '&lt;b&gt;'));
check('All views render', () => { for (const f of ['renderDay', 'renderPlan', 'renderRoadmap', 'renderReviews', 'renderControls', 'renderResources', 'renderSettings', 'renderRegister']) assert(api[f]().length > 500, f); });
for (const name of ['Project_ASTRO_Mission_R0_1.pdf', 'Project_ASTRO_Engineering_Baseline_R0_1.pdf', 'Project_ASTRO_Control_Workbook_R0_1.xlsx', 'Project_ASTRO_Complete_Package_R0_1.zip', 'ASTRO_365_Daily_Plan.csv', 'Requirements_R0_1.csv', 'Hazards_R0_1.csv', 'Verification_R0_1.csv', 'Day_006_Configuration_R0_3.pdf', 'astro-rigid-panel-concept-v1.png']) await fs.access(new URL('./dist/resources/' + name, import.meta.url));
checks.push({ name: 'All linked resources exist', result: 'PASS' });
const report = { date: '2026-11-05', plan: data.meta.revision, scope: 'Website data and logic only. No robot test.', checks };
await fs.mkdir(new URL('./qa/', import.meta.url), { recursive: true });
await fs.writeFile(new URL('./qa/logic_checks_R0_3.json', import.meta.url), JSON.stringify(report, null, 2));
console.log(JSON.stringify({ checks: checks.length, all: checks.every(c => c.result === 'PASS') }));
