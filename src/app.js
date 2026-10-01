// Cracking Problems Hub — the scope, the unit, the case files.
// Data is inlined at build time in <script id="hub-data">; scripts/build.mjs and
// scripts/derive.mjs define every field read here.

const DATA = JSON.parse(document.getElementById('hub-data').textContent);
const DAY = 86400000;
const NOW = Date.now();
const REDUCED = matchMedia('(prefers-reduced-motion: reduce)').matches;
const SVGNS = 'http://www.w3.org/2000/svg';

const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const md = s => esc(s)
  .replace(/`([^`]+)`/g, '<code>$1</code>')
  .replace(/\*\*(.+?)\*\*/g, '<b>$1</b>')
  .replace(/~~(.+?)~~/g, '<s>$1</s>')
  .replace(/(^|[\s(])\*([^*\s][^*]*?)\*(?=[\s).,;:]|$)/g, '$1<em>$2</em>');

const W1 = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve',
  'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen'];
const W10 = ['', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety'];
const words = n => n < 20 ? W1[n] : n < 100 ? W10[Math.floor(n / 10)] + (n % 10 ? '-' + W1[n % 10] : '') : String(n);
const Words = n => { const w = words(n); return w[0].toUpperCase() + w.slice(1); };

const MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
const toDate = iso => new Date(iso.length === 10 ? iso + 'T00:00:00Z' : iso);
const dm = iso => { const d = toDate(iso); return `${d.getUTCDate()} ${MON[d.getUTCMonth()]}`; };
const ageDays = iso => iso ? (NOW - toDate(iso).getTime()) / DAY : Infinity;
const rel = iso => {
  if (!iso) return '—';
  const m = Math.floor((NOW - new Date(iso).getTime()) / 60000);
  if (m < 60) return `${Math.max(1, m)}m ago`;
  if (m < 1440) return `${Math.floor(m / 60)}h ago`;
  const d = Math.floor(m / 1440);
  return d < 60 ? `${d}d ago` : new Date(iso).toISOString().slice(0, 10);
};
const sha7 = s => (s || '').slice(0, 7);
const REPO = DATA.repo.url;
const blob = p => esc(`${REPO}/blob/main/${p}`);
const tree = p => esc(`${REPO}/tree/main/${p}`);
const commitUrl = sha => esc(`${REPO}/commit/${sha}`);

// ---- Vocabulary -----------------------------------------------------------

// Radius on the scope is closeness to cracked: 0 is PASS, 1 is the edge.
const STAGES = {
  solved:    { label: 'Solved',        stamp: 'Solved',     r: 0.00, order: 0 },
  pass:      { label: 'PASS',          stamp: 'Pass',       r: 0.00, order: 1 },
  held:      { label: 'Held',          stamp: 'Held',       r: 0.27, order: 2, ring: 'Held · 3×PARTIAL' },
  panel:     { label: 'Panel pending', stamp: 'For panel',  r: 0.41, order: 3, ring: 'Panel pending' },
  working:   { label: 'In work',       stamp: 'Active',     r: 0.56, order: 4, ring: 'In work' },
  blocked:   { label: 'Blocked',       stamp: 'Blocked',    r: 0.56, order: 5 },
  unworked:  { label: 'Unworked',      stamp: 'Unopened',   r: 0.71, order: 6, ring: 'Unworked' },
  method:    { label: 'Method note',   stamp: 'Method',     r: 0.86, order: 7, ring: 'Method notes' },
  withdrawn: { label: 'Withdrawn',     stamp: 'Withdrawn',  r: 0.97, order: 8 },
};
const SECTORS = [
  { key: 'ciphers', label: 'Ciphers' },
  { key: 'historical-texts', label: 'Undeciphered texts' },
  { key: 'historical-controversies', label: 'Controversies' },
  { key: 'ireland', label: 'Ireland' },
];
const DOMAIN = {
  'ciphers': { short: 'Ciphers', drawer: 'A', prefix: 'C' },
  'historical-texts': { short: 'Texts', drawer: 'B', prefix: 'T' },
  'historical-controversies': { short: 'Controversies', drawer: 'C', prefix: 'H' },
  'ireland': { short: 'Ireland', drawer: 'D', prefix: 'I' },
  'discovered': { short: 'Discovered', drawer: 'E', prefix: 'P' },
};

// The unit. Callsigns are this site's; creeds and models are quoted from the
// repository (_roles/*.md, board/SCHEDULE.md) at build time.
const UNITS = [
  { key: 'breaker', no: '01', name: 'The Breakers', role: 'Breaker', orders: 'Takes an unclaimed problem, or advances a held one, and works it against primary evidence.' },
  { key: 'validator', no: '02', name: 'The Tribunal', role: 'Validator', orders: 'Three seats, one of them the refuter. Convened by Overwatch whenever a solve-claim is waiting.' },
  { key: 'orchestrator', no: '03', name: 'Overwatch', role: 'Orchestrator', orders: 'Reads the whole board, breaks silos between folders, keeps STATUS.md honest.' },
  { key: 'finder', no: '04', name: 'Pathfinders', role: 'Finder', orders: 'Brings back four verified problems a run, and checks nobody solved them first.' },
  { key: 'irregular', no: '05', name: 'The Irregulars', role: 'Outside the routines', orders: 'Sessions run by hand: the Codex lane and the human. Not configured from this repository.' },
];
const UNIT = Object.fromEntries(UNITS.map(u => [u.key, u]));

// Insignia: one geometric idea per unit, drawn on a 64-unit grid.
const SIGIL = {
  breaker: '<circle cx="32" cy="32" r="15"/><path d="M33 13l-5 9 7 6-6 8 5 6-3 9"/><path d="M20 44l-6 6M44 20l6-6"/>',
  validator: '<path d="M16 24L32 14l16 10z"/><path d="M22 27v17M32 27v17M42 27v17M15 47h34"/>',
  orchestrator: '<circle cx="32" cy="32" r="16"/><circle cx="32" cy="32" r="7"/><circle cx="32" cy="32" r="1.6" class="fill"/><path d="M32 10v6M32 48v6M10 32h6M48 32h6M32 32l11-11"/>',
  finder: '<path d="M32 11l4.5 16.5L53 32l-16.5 4.5L32 53l-4.5-16.5L11 32l16.5-4.5z"/><path d="M32 18v8"/>',
  irregular: '<path d="M32 12l17 10v20L32 52 15 42V22z" stroke-dasharray="4 4"/><path d="M32 24l7 8-7 8-7-8z"/>',
};
const sigil = (k, cls = '') => `<svg class="sigil ${cls}" viewBox="0 0 64 64" aria-hidden="true">${SIGIL[k] || ''}</svg>`;

const LIVE = DATA.problems.filter(p => !p.isStub);
// Coverage clock: the last working session, or the day the folder opened.
const workedAt = p => p.lastWorked || p.firstTouch || p.lastTouch;
const BY = Object.fromEntries(DATA.problems.map(p => [p.slug, p]));
const stageOf = p => STAGES[p.stage] ? p.stage : 'working';
const nameOf = p => p.shortTitle || p.title;
const count = k => LIVE.filter(p => stageOf(p) === k).length;
const hash = s => [...s].reduce((h, c) => (h * 31 + c.charCodeAt(0)) >>> 0, 7);
// A file's sector on the scope is its stream in the draw, so the two views agree.
const STREAM_OF = Object.fromEntries((DATA.draw?.streams || []).flatMap((s, i) => s.files.map(f => [f.slug, i])));
const sectorOf = p => {
  if (STREAM_OF[p.slug] != null && SECTORS[STREAM_OF[p.slug]]) return SECTORS[STREAM_OF[p.slug]].key;
  if (p.domain !== 'discovered') return p.domain;
  const s = p.statusRow?.suggestedDomain;
  return SECTORS.some(x => x.key === s) ? s : SECTORS[hash(p.id) % 4].key;
};

// Stable case numbers: per drawer, in the order the files were opened.
const CASE = {};
for (const d of Object.keys(DOMAIN)) {
  LIVE.filter(p => p.domain === d)
    .sort((a, b) => (a.firstTouch || '9').localeCompare(b.firstTouch || '9') || a.id.localeCompare(b.id))
    .forEach((p, i) => { CASE[p.slug] = `${DOMAIN[d].prefix}-${String(i + 1).padStart(2, '0')}`; });
}

// Where the repository contradicts itself, or a file has stalled, say so.
function flagsOf(p) {
  const f = [], st = stageOf(p);
  if (st === 'held' && !p.claim) f.push('Held, but no row in the STATUS.md validation queue names this folder.');
  if (st === 'held' && p.claim?.since && ageDays(p.claim.since) > 14) f.push(`On hold ${Math.floor(ageDays(p.claim.since))} days and the decisive check has not been run.`);
  if (st === 'unworked' && (p.roleTouches?.breaker || 0) > 0) f.push(`STATUS.md says never worked, but breaker sessions have committed here ${p.roleTouches.breaker} time${p.roleTouches.breaker === 1 ? '' : 's'}.`);
  if (st === 'working' && ageDays(workedAt(p)) > 14) f.push(`Listed as in work, but no working session for ${Math.floor(ageDays(workedAt(p)))} days.`);
  if (['working', 'unworked', 'held'].includes(st) && !p.nextMove && !p.claim) f.push('No next move in HANDOVER.md. Whoever takes this writes one before releasing.');
  if (st === 'panel' && ageDays(p.lastTouch) > 7) f.push(`Waiting for a panel; nothing has touched the folder for ${Math.floor(ageDays(p.lastTouch))} days.`);
  return f;
}
const FLAGS = Object.fromEntries(LIVE.map(p => [p.slug, flagsOf(p)]));

// ---- Decrypt effect -------------------------------------------------------
// Headlines resolve out of ogham, runes and Greek: the scripts this board works on.

const GLYPHS = 'ᚁᚂᚃᚄᚅᚆᚇᚈᚉᚊᚋᚌᚍᚎᚏᚐᚑᚒᚓᚔᚠᚢᚦᚨᚱᚲᚷᚹᚺᚾᛁᛃᛇᛈᛉᛊᛏᛒᛖᛗᛚᛜᛞᛟΔΘΛΞΠΣΦΨ';
function scramble(el, { speed = 16, spread = 260 } = {}) {
  if (REDUCED || !el || el.dataset.done) return;
  el.dataset.done = '1';
  el.style.minHeight = el.getBoundingClientRect().height + 'px';
  const nodes = [];
  const walk = n => n.nodeType === 3 ? nodes.push(n) : n.childNodes.forEach(walk);
  walk(el);
  let i = 0;
  const items = nodes.map(n => {
    const final = n.nodeValue;
    return { n, final, at: [...final].map(ch => /\s/.test(ch) ? 0 : (i++) * speed + Math.random() * spread) };
  });
  const t0 = performance.now(), end = i * speed + spread;
  const frame = t => {
    const e = t - t0;
    for (const it of items) {
      const chars = [...it.final];
      let s = '';
      for (let k = 0; k < chars.length; k++) s += e >= it.at[k] || /\s/.test(chars[k]) ? chars[k] : GLYPHS[(Math.random() * GLYPHS.length) | 0];
      it.n.nodeValue = s;
    }
    if (e < end) requestAnimationFrame(frame);
    else { items.forEach(it => { it.n.nodeValue = it.final; }); el.style.minHeight = ''; }
  };
  requestAnimationFrame(frame);
}

// ---- Clock, deployments, ticker -------------------------------------------

function nextFire(rule, from) {
  const b = new Date(from);
  for (let d = 0; d < 8; d++) {
    const y = b.getUTCFullYear(), m = b.getUTCMonth(), dd = b.getUTCDate() + d;
    if (rule.weekdays && !rule.weekdays.includes(new Date(Date.UTC(y, m, dd)).getUTCDay())) continue;
    for (const hr of rule.hours) { const t = Date.UTC(y, m, dd, hr, rule.minute); if (t > from) return t; }
  }
  return null;
}
const cd = ms => {
  const s = Math.max(0, Math.floor(ms / 1000)), h = Math.floor(s / 3600), m = Math.floor((s % 3600) / 60), sec = s % 60;
  return h >= 24 ? `${Math.floor(h / 24)}d ${String(h % 24).padStart(2, '0')}h` : `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(sec).padStart(2, '0')}`;
};
function tick() {
  const now = Date.now();
  $('#clock').textContent = new Date(now).toISOString().slice(11, 19) + 'Z';
  const fc = $('#fb-clock'); if (fc) fc.textContent = new Date(now).toISOString().slice(11, 19);
  const next = (DATA.routines || []).map(r => ({ ...r, at: nextFire(r.rule, now) })).filter(r => r.at).sort((a, b) => a.at - b.at)[0];
  if (next) $('#mast-next').innerHTML = `<span class="dim">${esc(UNIT[next.key]?.name || next.label)} deploy in</span> ${cd(next.at - now)}`;
  $$('[data-countdown]').forEach(el => {
    const r = DATA.routines.find(x => x.key === el.dataset.countdown);
    const at = r && nextFire(r.rule, now);
    if (at) el.textContent = cd(at - now);
  });
}

function paintTicker() {
  const pool = DATA.activity.filter(a => !['merge', 'infra', 'other'].includes(a.role));
  const rows = [...pool.filter(a => a.role !== 'orchestrator').slice(0, 12), ...pool.filter(a => a.role === 'orchestrator').slice(0, 4)]
    .sort((a, b) => b.date.localeCompare(a.date));
  if (!rows.length) { $('.ticker').hidden = true; return; }
  const who = a => a.unit === 'irregular' ? 'irregular' : a.role;
  const item = a => `<span class="tk" data-role="${esc(who(a))}"><i></i><b>${esc(UNIT[who(a)]?.name || a.role)}</b> ${esc(rel(a.date))} <span>${esc(a.subject)}</span></span>`;
  const run = rows.map(item).join('');
  const track = $('#ticker');
  track.innerHTML = `<div class="tk-run">${run}</div><div class="tk-run" aria-hidden="true">${run}</div>`;
  requestAnimationFrame(() => track.style.setProperty('--tk-dur', `${Math.round($('.tk-run', track).scrollWidth / 40)}s`));
}

// ---- Hero -----------------------------------------------------------------

function paintHero() {
  const live = LIVE.length, held = count('held'), passed = count('pass') + count('solved');
  const day = DATA.history?.since ? Math.floor(ageDays(DATA.history.since)) + 1 : null;
  const built = new Date(DATA.generatedAt).toISOString();
  $('#kicker').innerHTML = [day ? `Day ${day}` : null, `${dm(built)} ${built.slice(11, 16)}Z`,
    DATA.totals.research7d != null ? `${DATA.totals.research7d} research commits this week` : null,
    `<a href="${commitUrl(DATA.repo.headSha)}" target="_blank" rel="noopener">${esc(sha7(DATA.repo.headSha))}</a>`]
    .filter(Boolean).join('<span class="sep">·</span>');
  const lead = passed === 0
    ? `${Words(live)} problems.${day ? ` ${day} days.` : ''} Nothing cracked.`
    : `${Words(live)} problems. ${Words(passed)} cracked.`;
  $('#bluf').innerHTML = `<span class="l1">${esc(lead)}</span>` +
    (held ? `<span class="l2"><em>${Words(held)} ${held === 1 ? 'claim sits' : 'claims sit'} one signature out.</em></span>` : '');
  const su = DATA.statusUpdated;
  if (su) $('#bluf-sub').innerHTML = `The latest pass, ${esc(dm(su.date))}: ${esc(su.label)}${su.detail ? ` — ${md(su.detail)}` : ''}.${su.report ? ` <a href="${blob(su.report)}" target="_blank" rel="noopener">Read it</a>.` : ''}`;
  requestAnimationFrame(() => scramble($('#bluf'), { speed: 14, spread: 320 }));
}

// ---- The scope ------------------------------------------------------------

const svg = (tag, attrs = {}, parent) => {
  const n = document.createElementNS(SVGNS, tag);
  for (const [k, v] of Object.entries(attrs)) n.setAttribute(k, v);
  if (parent) parent.appendChild(n);
  return n;
};
const polar = (deg, r) => { const a = deg * Math.PI / 180; return [r * Math.sin(a), -r * Math.cos(a)]; };
const arc = (a1, a2, r, sw = 1) => { const [x1, y1] = polar(a1, r), [x2, y2] = polar(a2, r); return `M${x1} ${y1}A${r} ${r} 0 0 ${sw} ${x2} ${y2}`; };

function layout(R) {
  const groups = {};
  for (const p of LIVE) {
    const st = stageOf(p), ring = st === 'blocked' ? 'working' : st;
    (groups[`${sectorOf(p)}|${ring}`] ||= []).push(p);
  }
  const pts = [];
  for (const [key, list] of Object.entries(groups)) {
    const [sec, ring] = key.split('|');
    const si = SECTORS.findIndex(s => s.key === sec);
    list.sort((a, b) => STAGES[stageOf(a)].order - STAGES[stageOf(b)].order || nameOf(a).localeCompare(nameOf(b)));
    const pad = 11, span = 90 - pad * 2;
    list.forEach((p, i) => {
      const deg = si * 90 + pad + (i + 0.5) * span / list.length;
      const stagger = list.length > 5 ? (i % 2 ? 0.028 : -0.028) : 0;
      const [x, y] = polar(deg, (STAGES[ring].r + stagger) * R);
      pts.push({ p, deg, x, y });
    });
  }
  return pts;
}

const scopes = [];
function buildScope(host, { mini = false } = {}) {
  const R = 400;
  const root = svg('svg', { viewBox: '-500 -500 1000 1000', role: 'img', 'aria-label': `Scope of ${LIVE.length} problems by closeness to cracked` });
  const defs = svg('defs', {}, root);
  const face = svg('g', {}, root);
  svg('circle', { r: R, class: 'disc' }, face);
  for (const [k, s] of Object.entries(STAGES)) {
    if (!s.ring) continue;
    svg('circle', { r: s.r * R, class: `ring ring-${k}` }, face);
  }
  for (let a = 0; a < 360; a += 90) { const [x1, y1] = polar(a, 0.1 * R), [x2, y2] = polar(a, R); svg('line', { x1, y1, x2, y2, class: 'axis' }, face); }
  if (!mini) for (let a = 0; a < 360; a += 2) {
    const long = a % 30 === 0, mid = a % 10 === 0;
    const [x1, y1] = polar(a, R), [x2, y2] = polar(a, R + (long ? 12 : mid ? 7 : 4));
    svg('line', { x1, y1, x2, y2, class: long ? 'tick long' : 'tick' }, face);
  }
  SECTORS.forEach((s, i) => {
    const lower = i === 1 || i === 2, id = `arc-${mini ? 'm' : 'h'}-${i}`;
    const a1 = i * 90 + 6, a2 = i * 90 + 84;
    svg('path', { id, d: lower ? arc(a2, a1, R + (mini ? 44 : 40), 0) : arc(a1, a2, R + (mini ? 22 : 26), 1), fill: 'none' }, defs);
    const t = svg('text', { class: 'sector-label' }, face);
    const n = DATA.draw?.streams[i]?.files.length ?? LIVE.filter(p => sectorOf(p) === s.key).length;
    svg('textPath', { href: `#${id}`, startOffset: '50%', 'text-anchor': 'middle' }, t).textContent = mini ? s.label.toUpperCase() : `${s.label.toUpperCase()}  ·  ${n}`;
  });
  const passed = count('pass') + count('solved');
  svg('circle', { r: 0.1 * R, class: 'bull' + (passed ? ' lit' : '') }, face);
  svg('text', { y: mini ? 10 : -2, class: 'bull-label' }, face).textContent = 'PASS';
  if (!mini) svg('text', { y: 26, class: 'bull-n' }, face).textContent = String(passed);

  const sweep = svg('g', { class: 'sweep' }, root);
  for (let i = 0; i < 14; i++) {
    const [x1, y1] = polar(-(i + 1) * 4, R), [x2, y2] = polar(-i * 4, R);
    svg('path', { d: `M0 0L${x1} ${y1}A${R} ${R} 0 0 1 ${x2} ${y2}Z`, class: 'wake', style: `opacity:${(0.2 * (1 - i / 14) ** 1.6).toFixed(3)}` }, sweep);
  }
  svg('line', { x1: 0, y1: 0, x2: 0, y2: -R, class: 'beam' }, sweep);
  if (REDUCED) sweep.style.display = 'none';

  const links = svg('g', { class: 'links' }, root);
  const blips = svg('g', {}, root);
  const pts = layout(R);
  const nodes = pts.map(({ p, deg, x, y }) => {
    const st = stageOf(p);
    const size = (mini ? 7 : 6) + Math.min(9, Math.sqrt(p.commits30d || 0) * 2.1);
    const g = svg('g', { class: `blip s-${st}`, transform: `translate(${x.toFixed(1)} ${y.toFixed(1)})`, 'data-slug': p.slug, tabindex: mini ? -1 : 0, role: 'button', 'aria-label': `${nameOf(p)}, ${STAGES[st].label}` }, blips);
    svg('circle', { r: size * 1.9, class: 'halo' }, g);
    svg('circle', { r: size, class: 'core' }, g);
    if (!mini && FLAGS[p.slug].length) svg('circle', { cx: size * 0.8, cy: -size * 0.8, r: 4.5, class: 'flag-dot' }, g);
    svg('circle', { r: Math.max(size * 2.2, mini ? 16 : 26), class: 'hit' }, g);
    const idle = ageDays(workedAt(p));
    const expected = !['method', 'withdrawn'].includes(st);
    return { g, deg, x, y, size, p, idle,
      base: 0.28 + 0.5 * Math.max(0, 1 - idle / 21),
      neglect: expected ? Math.max(0.14, Math.min(1, idle / 14)) : 0.06 };
  });

  // Neglect mode labels the coldest files that are supposed to be moving.
  const labels = svg('g', { class: 'neglect-labels' }, root);
  if (!mini) nodes.filter(n => n.neglect > 0.06).sort((a, b) => b.idle - a.idle).slice(0, 6).forEach(n => {
    const right = n.x >= 0;
    const t = svg('text', { x: n.x + (right ? n.size + 10 : -n.size - 10), y: n.y + 4, 'text-anchor': right ? 'start' : 'end' }, labels);
    t.textContent = `${nameOf(n.p).replace(/\s*\(.*?\)\s*$/, '')} · ${Math.floor(n.idle)}d`;
  });
  const pulses = svg('g', { class: 'pulses' }, root);
  const agentLayer = svg('g', { class: 'agents' }, root);

  // Mark where the Breakers last went in.
  let mark = null;
  const last = DATA.lastByRole?.breaker;
  const target = !mini && last?.problems?.map(s => nodes.find(n => n.p.slug === s)).find(Boolean);
  if (target) {
    const { x, y, size } = target, o = size + 9, l = 7;
    mark = svg('g', { class: 'sortie', transform: `translate(${x.toFixed(1)} ${y.toFixed(1)})` }, root);
    for (const [sx, sy] of [[-1, -1], [1, -1], [1, 1], [-1, 1]]) {
      svg('path', { d: `M${sx * o} ${sy * (o - l)}V${sy * o}H${sx * (o - l)}` }, mark);
    }
  }

  host.appendChild(root);
  const scope = { mini, R, root, sweep, nodes, by: Object.fromEntries(nodes.map(n => [n.p.slug, n])), links, pulses, agentLayer, visible: true };
  nodes.forEach(n => n.g.style.setProperty('--g', REDUCED ? n.base + 0.2 : n.base));
  scopes.push(scope);
  new IntersectionObserver(([e]) => { scope.visible = e.isIntersecting; }).observe(host);
  return scope;
}

// ---- The mini scope's sweep ----------------------------------------------------

const PERIOD = 9000;
function spin(t) {
  const a = (t % PERIOD) / PERIOD * 360;
  for (const s of scopes) {
    if (!s.visible) continue;
    s.sweep.setAttribute('transform', `rotate(${a.toFixed(2)})`);
    for (const n of s.nodes) {
      const behind = (a - n.deg + 360) % 360;
      const glow = behind < 320 ? Math.exp(-behind / 50) : 0;
      n.g.style.setProperty('--g', Math.min(1, n.base + glow * 0.9).toFixed(3));
    }
  }
  if (!document.hidden) requestAnimationFrame(spin);
}
document.addEventListener('visibilitychange', () => { if (!document.hidden && !REDUCED) requestAnimationFrame(spin); });

// ---- Shared bits ----------------------------------------------------------

const SPAN = Math.max(14, Math.min(90, (DATA.pulse || []).length || 30));
function strip(dates, days, w, h, cls = '') {
  const b = new Array(days).fill(0);
  for (const d of dates || []) { const a = Math.floor(ageDays(d)); if (a >= 0 && a < days) b[days - 1 - a]++; }
  const max = Math.max(3, ...b), step = w / days;
  const bars = b.map((v, i) => v ? `<rect x="${(i * step).toFixed(2)}" y="${h - Math.max(3, v / max * (h - 1))}" width="${Math.max(1.2, step - 1).toFixed(2)}" height="${Math.max(3, v / max * (h - 1))}"${i >= days - 7 ? ' class="r"' : ''}/>` : '').join('');
  return `<svg class="strip ${cls}" viewBox="0 0 ${w} ${h}" preserveAspectRatio="none" aria-hidden="true"><line x1="0" x2="${w}" y1="${h - 0.5}" y2="${h - 0.5}"/>${bars}</svg>`;
}
// The units that have worked a file, as small insignia with counts.
function marks(p, cls = '') {
  const t = p.roleTouches || {};
  const keys = UNITS.map(u => u.key).filter(k => t[k]);
  return keys.length
    ? `<span class="marks ${cls}">${keys.map(k => `<span class="mark" data-role="${k}" title="${esc(UNIT[k].name)}: ${t[k]} commit${t[k] === 1 ? '' : 's'}">${sigil(k)}<span class="mono">${t[k]}</span></span>`).join('')}</span>`
    : `<span class="marks ${cls} none">No unit has worked this file</span>`;
}
const badge = p => { const s = stageOf(p); return `<span class="badge s-${s}">${esc(STAGES[s].label)}</span>`; };
const stampEl = (p, cls = '') => { const s = stageOf(p); return `<span class="rubber s-${s} ${cls}">${esc(STAGES[s].stamp)}</span>`; };
const chips = slugs => (slugs || []).filter(s => BY[s]).map(s => `<button type="button" class="pchip" data-slug="${esc(s)}">${esc(nameOf(BY[s]).replace(/\s*\(.*?\)\s*$/, ''))}</button>`).join('');

// ---- I. Priority files ----------------------------------------------------

function paintPriority() {
  const held = LIVE.filter(p => stageOf(p) === 'held').sort((a, b) => (a.claim?.since || '9').localeCompare(b.claim?.since || '9'));
  const tilt = [-7, 4, -3, 6, -5];
  $('#priority-files').innerHTML = held.map((p, i) => {
    const c = p.claim, days = c?.since ? Math.floor(ageDays(c.since)) : null;
    return `
    <article class="pfile paper" data-slug="${esc(p.slug)}" tabindex="0" role="button" aria-label="Open priority file ${esc(CASE[p.slug])}: ${esc(nameOf(p))}">
      <div class="pf-band mono"><span>Priority</span><span>${esc(CASE[p.slug])}</span></div>
      <p class="pf-meta typed">${esc(DOMAIN[p.domain].short)} · opened ${p.firstTouch ? esc(dm(p.firstTouch)) : '—'}</p>
      <h3 class="pf-title">${esc(nameOf(p))}</h3>
      <div class="pf-stamps">${['Validator', 'Validator', 'Refuter'].map((who, j) =>
        `<span class="rubber partial" style="--t:${tilt[(i + j) % 5]}deg">Partial<i>${who}</i></span>`).join('')}</div>
      <div class="pf-lock">${inkLock('held')}<p class="typed">Five of seven pins set. PASS and a signature outstanding.</p></div>
      <div class="pf-held"><span class="mono">${days ?? '—'}</span><span class="typed">days on hold${c?.since ? `<br>panel closed ${esc(dm(c.since))}` : ''}</span></div>
      <p class="pf-label typed">Action required</p>
      <p class="pf-check"><mark>${c ? md(c.missingCheck) : 'No validation-queue row names this folder.'}</mark></p>
      <div class="pf-sign"><span class="typed">Human sign-off</span><span class="line"></span><span class="typed dim-ink">pending</span></div>
      <footer class="pf-foot">${marks(p)}<span class="typed">${esc(rel(p.lastTouch))}</span></footer>
    </article>`;
  }).join('') || '<p class="empty">No claim is held.</p>';

  const panel = LIVE.filter(p => stageOf(p) === 'panel');
  $('#anteroom').innerHTML = panel.length ? `
    <h3 class="label">Awaiting a panel — bounded claims with no verdict yet</h3>
    <div class="slips">${panel.map(p => `
      <article class="slip paper" data-slug="${esc(p.slug)}" tabindex="0" role="button">
        <p class="typed slip-no">${esc(CASE[p.slug])} · for panel</p>
        <h4>${esc(nameOf(p))}</h4>
        <p class="typed">${md(p.claim?.missingCheck || '')}</p>
      </article>`).join('')}</div>` : '';
}

// ---- The board --------------------------------------------------------------
// Rendered from DATA.draw, which scripts/derive.mjs computes: the same numbers a
// Breaker session gets from `npm run draw`. The site never re-ranks on its own.
// Rows are closeness to cracked, top is nearest; columns are the four streams in
// rotation order; within a cell, files stand in draw order, highest debt first.

const boardName = p => nameOf(p).split(/\s+[—–]\s+|:\s|\s\(/)[0];
// Idle days were counted at build time; keep counting since.
const DRIFT = Math.max(0, (NOW - Date.parse(DATA.generatedAt)) / DAY);
const idleOf = f => Math.floor(f.idle + DRIFT);
const ROWS = [
  { k: 'held', note: 'Survived a panel at 3×PARTIAL. One check and a signature from PASS.' },
  { k: 'panel', note: 'A bounded claim waiting for its panel. Owed to Overwatch, never drawn.' },
  { k: 'working', note: 'Opened by a Breaker and still moving.' },
  { k: 'unworked', note: 'No Breaker has gone in yet.' },
  { k: 'blocked', note: 'Evidence out of reach. Ranked, but never leads.' },
];

function paintFiring() {
  const d = DATA.draw, P = d?.pick, L = d?.rotation.last;
  if (!P) { $('#firing').innerHTML = '<p class="label">Next Breaker firing</p><p class="f-why">Nothing is drawable right now.</p>'; return; }
  const f = d.streams.flatMap(s => s.files).find(x => x.slug === P.slug), p = BY[P.slug];
  const S = d.streams.find(s => s.id === P.stream);
  const order = d.streams.map(s => s.id);
  const after = [1, 2, 3].map(i => order[(order.indexOf(P.stream) + i) % order.length]);
  $('#firing').className = `firing s-${f.stage}`;
  $('#firing').innerHTML = `
    <p class="f-head"><span class="label">Next Breaker firing</span><span class="mono f-cd" data-countdown="breaker">--:--:--</span></p>
    <p class="f-stream mono">Stream ${esc(P.stream)} · ${esc(S.label)}</p>
    <h2 class="f-name"><button type="button" data-slug="${esc(P.slug)}">${esc(nameOf(p))}</button></h2>
    <p class="f-why"><span class="badge s-${f.stage}">${esc(STAGES[f.stage].label)}</span> idle ${idleOf(f)} days · debt ${Math.round(f.debt)}${f.pickup ? ' · <b class="pickup">pick-up rule</b>' : ''}. ${esc(P.reason[0].toUpperCase() + P.reason.slice(1))}.</p>
    ${f.next ? `<p class="f-next"><span class="label">Its next move</span>${md(f.next)}</p>` : '<p class="f-next warn-text">No next move written. The session writes one before it may release.</p>'}
    <ol class="f-rot mono" aria-label="Rotation">
      ${L ? `<li class="was"><b>${esc(L.stream)}</b>last · ${esc(rel(L.date))}</li>` : ''}
      <li class="now"><b>${esc(P.stream)}</b>next</li>
      ${after.filter(x => x !== L?.stream).map(x => `<li><b>${esc(x)}</b></li>`).join('')}
    </ol>
    ${d.overwatch?.length ? `<p class="f-ow"><span class="label">Owed to Overwatch</span>${d.overwatch.map(s => `<button type="button" class="linkish" data-slug="${esc(s)}">${esc(boardName(BY[s]))}</button>`).join(', ')}: panels, which no Breaker can convene.</p>` : ''}
    <a class="f-more" href="/framework">How the draw works →</a>`;
}

function paintBoard() {
  const d = DATA.draw;
  if (!d) { $('#board').innerHTML = '<p class="empty">No draw in this build.</p>'; return; }
  const P = d.pick, L = d.rotation.last;
  const all = d.streams.flatMap(s => s.files);
  const max = Math.max(1, ...all.map(f => f.debt));
  const n = k => all.filter(f => f.stage === k).length;
  const passed = count('pass') + count('solved');
  const chip = f => {
    const p = BY[f.slug], idle = idleOf(f);
    const pick = P?.slug === f.slug, last = L?.slug === f.slug;
    const cold = f.movable && idle > 14;
    const tags = [
      pick && '<i class="t-next">next</i>',
      f.pickup && '<i class="t-pickup">pick-up</i>',
      last && '<i class="t-last">last</i>',
      f.claimed && '<i class="t-claimed">claimed</i>',
      f.slug.startsWith('discovered/') && '<i class="t-new">new</i>',
      f.movable && !f.next && '<i class="t-warn" title="No next move written" aria-label="No next move written">!</i>',
    ].filter(Boolean).join('');
    return `<button type="button" class="fc s-${f.stage}${pick ? ' is-pick' : ''}${cold ? ' is-cold' : ''}${idle < 3 ? ' is-fresh' : ''}" data-slug="${esc(f.slug)}" style="--d:${(f.debt / max).toFixed(3)}">
      <span class="fc-n">${esc(boardName(p))}</span>${tags ? `<span class="fc-t">${tags}</span>` : ''}<span class="fc-i mono">${idle}d</span></button>`;
  };
  const rail = `
    <div class="b-rail" aria-hidden="true">
      <div class="b-rh"><span class="mono">Closer to cracked</span><svg viewBox="0 0 10 40"><path d="M5 39V2M1 7l4-5 4 5"/></svg></div>
      <div class="b-rl s-pass"><span class="b-rn">PASS<b class="mono">${passed}</b></span></div>
      ${ROWS.map(r => `<div class="b-rl s-${r.k}"><span class="b-rn">${esc(STAGES[r.k].label)}<b class="mono">${n(r.k)}</b></span><span class="b-rnote">${esc(r.note)}</span></div>`).join('')}
    </div>`;
  const pass = `<div class="b-pass s-pass">${passed ? `${Words(passed)} ${passed === 1 ? 'file has' : 'files have'} crossed.` : '<b>Nothing has crossed.</b> A file reaches PASS only when two validators and a refuter all pass it and a human signs.'}</div>`;
  const cols = d.streams.map((s, si) => {
    const isNext = P?.stream === s.id, isLast = L?.stream === s.id;
    const cold = s.files.filter(f => f.movable && idleOf(f) > 14).length;
    return `
    <section class="b-col${isNext ? ' is-next' : ''}${isLast ? ' is-last' : ''}" data-stream="${esc(s.id)}" style="grid-column:${si + 2}" aria-label="Stream ${esc(s.id)}, ${esc(s.label)}">
      <header class="b-head">
        <span class="b-id">${esc(s.id)}</span>
        <div class="b-ht"><h3>${esc(s.label)}</h3>
        <p class="mono">${s.files.length} files${cold ? ` · <b class="cold">${cold} cold</b>` : ''}</p></div>
        ${isNext ? '<span class="b-flag next">Next firing</span>' : isLast ? `<span class="b-flag last">Last · ${esc(rel(L.date))}</span>` : ''}
      </header>
      ${ROWS.map((r, i) => {
        const fs = s.files.filter(f => f.stage === r.k);
        return `<div class="b-cell s-${r.k}${fs.length ? '' : ' is-empty'}" style="grid-row:${i + 3}" data-label="${esc(STAGES[r.k].label)}">${fs.map(chip).join('')}</div>`;
      }).join('')}
    </section>`;
  }).join('');
  $('#board').innerHTML = rail + pass + cols;
  $('#b-tabs').innerHTML = `<p class="b-mpass s-pass"><b class="mono">PASS ${passed}</b> ${passed ? 'crossed' : 'nothing has crossed'}</p><div class="b-tab-row">${d.streams.map(s => `<button type="button" role="tab" data-tab="${esc(s.id)}" aria-selected="false"${P?.stream === s.id ? ' class="is-next"' : ''}><b>${esc(s.id)}</b>${esc(s.label.replace('Undeciphered texts', 'Texts'))}</button>`).join('')}</div>`;
  const other = LIVE.length - all.length;
  $('#board-foot').innerHTML = `Within each cell, files stand in draw order: highest coverage debt first, and the bar under each is its debt (days since a Breaker or Validator session × a stage weight). The number is idle days; past ${d.pickupDays}, a file is cold. <span class="t-warn-inline">!</span> marks a file with no next move written.${other ? ` ${Words(other)} ${other === 1 ? 'file is' : 'files are'} not drawn: method notes and withdrawn claims, kept in the case files.` : ''} <a href="/framework">The rules →</a>`;

  // Narrow screens: the columns become a swipeable carousel with stream tabs.
  const board = $('#board'), tabs = $$('#b-tabs [data-tab]');
  const sync = () => {
    const w = $('.b-col', board)?.offsetWidth || 1;
    const per = Math.max(1, Math.round(board.clientWidth / w));
    const k = Math.min(Math.round(board.scrollLeft / w), tabs.length - per);
    tabs.forEach((t, j) => t.setAttribute('aria-selected', j >= k && j < k + per));
    fit(k, per);
  };
  // The carousel is as tall as the stream in view, not the longest one.
  let shown = '';
  const fit = (i, per) => {
    const cols = $$('.b-col', board), key = `${i}/${per}`;
    if (key === shown) return; shown = key;
    const h = Math.max(...cols.slice(i, i + per).map(c => c.scrollHeight));
    board.style.height = getComputedStyle(board).display === 'flex' && h > 0 ? `${h}px` : '';
  };
  board.addEventListener('scroll', () => requestAnimationFrame(sync), { passive: true });
  addEventListener('resize', () => { shown = ''; sync(); });
  $('#b-tabs').addEventListener('click', e => {
    const t = e.target.closest('[data-tab]'); if (!t) return;
    const col = $(`.b-col[data-stream="${t.dataset.tab}"]`, board);
    board.scrollTo({ left: col.offsetLeft - board.offsetLeft, behavior: REDUCED ? 'auto' : 'smooth' });
  });
  const start = $$('.b-col', board).findIndex(c => c.classList.contains('is-next'));
  requestAnimationFrame(() => {
    if (start > 0 && getComputedStyle(board).display === 'flex') board.scrollLeft = start * $('.b-col', board).offsetWidth;
    sync();
  });
}

// ---- IV. The job: crew records ------------------------------------------------

function paintUnits() {
  const days = DATA.pulse || [];
  const prof = DATA.roleProfiles || {};
  const last = DATA.lastByRole || {};
  $('#units').innerHTML = UNITS.map(u => {
    const series = days.map(d => d[u.key] || 0);
    const total = series.reduce((a, b) => a + b, 0);
    const active = series.filter(Boolean).length;
    const max = Math.max(1, ...series);
    const tape = `<svg class="tape" viewBox="0 0 ${series.length * 6} 28" preserveAspectRatio="none" aria-hidden="true">${series.map((v, i) =>
      v ? `<rect x="${i * 6}" y="${28 - Math.max(3, v / max * 26)}" width="4" height="${Math.max(3, v / max * 26)}" rx="1"/>` : `<rect x="${i * 6}" y="26" width="4" height="2" class="nil"/>`).join('')}</svg>`;
    const routine = (DATA.routines || []).find(r => r.key === u.key);
    const p = prof[u.key];
    const l = last[u.key];
    const deploy = routine
      ? `<span class="label">Next deployment</span><span class="cd mono" data-countdown="${u.key}">--:--:--</span><span class="cad mono">${esc(routine.cadence)}</span>`
      : u.key === 'validator'
        ? `<span class="label">Next deployment</span><span class="cd mono oncall">On call</span><span class="cad mono">convened by Overwatch</span>`
        : `<span class="label">Next deployment</span><span class="cd mono oncall">Unscheduled</span><span class="cad mono">run by hand</span>`;
    const model = u.key === 'validator' ? 'spawned by Overwatch' : u.key === 'irregular' ? 'Codex lane and others'
      : (p?.model || '—').replace(/\s*\(pinned (\d{4}-\d\d-\d\d)\)/, (_, d) => ` · pinned ${dm(d)}`);
    return `
    <article class="unit-card" data-role="${u.key}">
      <header class="uc-head">
        ${sigil(u.key, 'big')}
        <div><p class="uc-no mono">Unit ${u.no} · ${esc(u.role)}</p><h3>${esc(u.name)}</h3></div>
      </header>
      ${p?.creed ? `<blockquote class="uc-creed">“${esc(p.creed)}”<cite class="mono"><a href="${blob(p.file)}" target="_blank" rel="noopener">${esc(p.file)}</a></cite></blockquote>`
        : `<blockquote class="uc-creed plain">${esc(u.orders)}</blockquote>`}
      ${p?.creed ? `<p class="uc-orders">${esc(u.orders)}</p>` : ''}
      <dl class="uc-stats">
        <div><dt>Sorties</dt><dd class="mono">${total}</dd></div>
        <div><dt>Days out</dt><dd class="mono">${active}<span>/${series.length}</span></dd></div>
        <div class="wide"><dt>Model</dt><dd class="mono sm">${esc(model)}</dd></div>
      </dl>
      ${tape}
      <div class="uc-deploy">${deploy}</div>
      <div class="uc-last">${l ? `<span class="label">Last sortie · ${esc(rel(l.date))}</span><a href="${commitUrl(l.sha)}" target="_blank" rel="noopener">${esc(l.subject)}</a>${l.problems?.length ? `<div class="pchips">${chips(l.problems)}</div>` : ''}` : '<span class="label">No sortie in window</span>'}</div>
    </article>`;
  }).join('');
}

// ---- Shared by the scenes -------------------------------------------------

const DRAWN = Object.fromEntries((DATA.draw?.streams || []).flatMap(s => s.files.map(f => [f.slug, { ...f, stream: s.id }])));
const STREAMS = DATA.draw?.streams || [];
// The seven gates between an opened folder and a signed solution.
const GATES = ['Opened', 'Worked', 'Claim staked', 'Panel sat', '3×PARTIAL held', 'PASS', 'Signed'];
const gatesOf = st => ({ held: 5, panel: 3, working: 2, blocked: 2, unworked: 1, pass: 6, solved: 7 }[st] || 1);
const rng = seed => () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
const clip = (s, n) => s.length > n ? s.slice(0, n - 1) + '…' : s;
// Every scene's file marks carry data-slug (opens the case file) and data-tip
// (the paper tooltip with the next move), so they behave like the board's chips.
const tipAttrs = slug => `data-slug="${esc(slug)}" data-tip="${esc(slug)}"`;

// A tumbler lock in ink, for paper: pins set as far as the file's gates.
function inkLock(st) {
  const g = gatesOf(st), cw = 30, H = 46, sy = 23;
  const cells = GATES.map((name, i) => {
    const x = i * cw + 2, set = i < g, never = i >= 5;
    const drop = set ? 0 : 7;
    return `<rect x="${x}" y="1" width="${cw - 4}" height="${H - 2}" rx="2" class="lk-ch${never ? ' never' : ''}"/>
      <rect x="${x + 5}" y="5" width="${cw - 14}" height="${sy - 7 + drop}" rx="1.5" class="lk-dr"/>
      <rect x="${x + 5}" y="${sy + 1 + drop}" width="${cw - 14}" height="${H - sy - 6 - drop}" rx="1.5" class="${set ? 'lk-set' : 'lk-un'}"/>
      <text x="${x + (cw - 4) / 2}" y="${H + 13}" class="lk-n">${['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii'][i]}</text>`;
  }).join('');
  return `<svg class="inklock" viewBox="0 0 212 62" role="img" aria-label="${g} of 7 gates passed"><title>${g} of 7 gates passed: ${GATES.slice(0, g).join(', ')}</title>${cells}<line x1="0" x2="212" y1="${sy}" y2="${sy}" class="lk-sh"/></svg>`;
}

// ---- II. The ascent ---------------------------------------------------------
// Each stream is a mountain and PASS its summit; every file is a party camped at
// the altitude its evidence has reached. Fog settles on anything idle past 14 days.

const CAMPS = [
  { k: 'unworked', l: 'Base camp', s: 'unworked', r: '', h: .1 },
  { k: 'working', l: 'Camp I', s: 'in work · blocked', r: 'I', h: .34 },
  { k: 'panel', l: 'Camp II', s: 'claim before a panel', r: 'II', h: .55 },
  { k: 'held', l: 'Camp III', s: 'held at 3×PARTIAL', r: 'III', h: .74 },
  { k: 'pass', l: 'Summit', s: 'PASS · nobody yet', r: 'PASS', h: .95 },
];
const PW = 360, PH = 640, BASE = 586, TOPY = 56;
const altY = h => BASE - h * (BASE - TOPY);

function paintAscent() {
  const host = $('#ascent');
  if (!STREAMS.length) { host.innerHTML = '<p class="empty">No draw in this build.</p>'; return; }
  // Rail: the camp names, drawn at the same scale as the peaks beside it.
  const rail = `<svg class="as-rail" viewBox="0 0 150 ${PH}" aria-hidden="true">${CAMPS.map(c =>
    `<text x="0" y="${altY(c.h) - 4}" class="as-cl">${esc(c.l.toUpperCase())}</text><text x="0" y="${altY(c.h) + 12}" class="as-cs">${esc(c.s)}</text>`).join('')}</svg>`;
  const peaks = STREAMS.map(s => {
    const r = rng(hash(s.id) + 11), cx = PW / 2, half = 168, N = 30;
    const pts = [];
    for (let j = 0; j <= N; j++) {
      const t = j / N, side = t < .5 ? t * 2 : (1 - t) * 2;
      const hh = j === N / 2 ? .97 : Math.max(0, side ** 1.25 * .97 + (j && j < N ? (r() - .5) * .1 : 0));
      pts.push([cx - half + t * half * 2, altY(hh)]);
    }
    const ridge = pts.map(([x, y]) => `${x.toFixed(1)} ${y.toFixed(1)}`).join('L');
    const shape = `M${ridge}L${cx + half} ${BASE + 30}L${cx - half} ${BASE + 30}Z`;
    const widthAt = h => half * (1 - (h / .97) ** .8) * .6;
    // Parties by camp, blocked files camping at Camp I with the in-work ones.
    const byCamp = {};
    for (const f of s.files) (byCamp[f.stage === 'blocked' ? 'working' : f.stage] ||= []).push(f);
    const top = [...CAMPS].reverse().find(c => byCamp[c.k]?.length);
    // The route: a switchback from base camp to the summit, inked as far as anyone has climbed.
    const route = CAMPS.map((c, i) => [cx + (i % 2 ? 1 : -1) * widthAt(c.h) * .55 * (i === 4 ? 0 : 1), altY(c.h) + (i === 4 ? 0 : 6)]);
    const reached = Math.max(0, CAMPS.indexOf(top));
    const path = pts2 => 'M' + pts2.map(([x, y]) => `${x.toFixed(1)} ${y.toFixed(1)}`).join('L');
    let parties = '', fog = '', labels = '';
    for (const c of CAMPS) {
      const fs = (byCamp[c.k] || []).sort((a, b) => b.debt - a.debt);
      const w = widthAt(c.h);
      fs.forEach((f, j) => {
        const t = fs.length === 1 ? 0 : (j / (fs.length - 1)) * 2 - 1;
        const x = cx + t * w, y = altY(c.h) - 9 - (j % 2) * 8;
        const idle = idleOf(f), cold = f.movable && idle > 14, p = BY[f.slug];
        const mark = f.stage === 'blocked'
          ? `<path d="M-5 -5L5 5M5 -5L-5 5" class="as-x"/>`
          : `<circle r="${f.stage === 'held' ? 8 : 6}" class="as-dot"/>`;
        parties += `<g class="as-party s-${f.stage}${cold ? ' cold' : ''}" transform="translate(${x.toFixed(1)} ${y.toFixed(1)})" ${tipAttrs(f.slug)} tabindex="0" role="button" aria-label="${esc(nameOf(p))}, ${esc(STAGES[f.stage]?.label || f.stage)}, idle ${idle} days"><circle r="15" class="hit"/>${mark}${
          f.slug === DATA.draw.pick?.slug ? `<line x1="0" x2="0" y1="-9" y2="-44" class="as-pole"/><path d="M0 -44l24 6l-24 6Z" class="as-flag next"/><text y="-52" class="as-ft next">NEXT ASCENT</text>` : ''}${
''}</g>`;
        if (cold) fog += `<ellipse cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" rx="34" ry="15" class="as-fog" style="animation-delay:${-(hash(f.slug) % 90) / 10}s"/>`;
        if (f.stage === 'held') {
          const lx = Math.min(PW - 92, Math.max(92, x));
          labels += `<text x="${lx.toFixed(1)}" y="${(altY(c.h) - 48 - j * 36).toFixed(1)}" text-anchor="middle" class="as-lab">${esc(clip(boardName(p), 20))}${f.pickup ? `<tspan x="${lx.toFixed(1)}" dy="15" class="as-pu">pick-up rule</tspan>` : ''}</text>`;
        }
      });
    }
    const cold = s.files.filter(f => f.movable && idleOf(f) > 14).length;
    return `
    <figure class="as-peak${DATA.draw.pick?.stream === s.id ? ' is-next' : ''}">
      <svg viewBox="0 0 ${PW} ${PH}" role="img" aria-label="Stream ${esc(s.id)}, ${esc(s.label)}: ${s.files.length} files, highest at ${esc(top?.l || 'base camp')}">
        <defs><clipPath id="as-clip-${esc(s.id)}"><path d="${shape}"/></clipPath><filter id="as-blur-${esc(s.id)}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="8"/></filter></defs>
        ${CAMPS.map(c => `<line x1="0" x2="${PW}" y1="${altY(c.h)}" y2="${altY(c.h)}" class="as-camp${c.k === 'pass' ? ' summit' : ''}"/><text x="${PW - 4}" y="${altY(c.h) - 5}" class="as-roman">${c.r}</text>`).join('')}
        <path d="${shape}" class="as-fill"/>
        <g clip-path="url(#as-clip-${esc(s.id)})">${Array.from({ length: Math.ceil((BASE + 30 - TOPY) / 7) }, (_, i) => `<line x1="0" x2="${PW}" y1="${TOPY + i * 7}" y2="${TOPY + i * 7 + 3}" class="as-eng"/>`).join('')}</g>
        <path d="M${ridge}" class="as-edge"/>
        <path d="${path(route)}" class="as-route"/>
        <path d="${path(route.slice(0, reached + 1))}" class="as-route done"/>
        <line x1="${cx}" x2="${cx}" y1="${altY(.97)}" y2="${altY(.97) - 34}" class="as-pole"/><path d="M${cx} ${altY(.97) - 34}l22 6l-22 6Z" class="as-flag empty"/>
        <g filter="url(#as-blur-${esc(s.id)})">${fog}</g>
        ${parties}${labels}
      </svg>
      <figcaption><span class="as-id">${esc(s.id)}</span><span class="as-name">${esc(s.label)}</span><span class="as-sum mono">${esc(top?.l || 'Base camp')} · ${s.files.length} parties</span>${cold ? `<span class="as-sum mono"><b>${cold} in fog</b></span>` : ''}</figcaption>
    </figure>`;
  }).join('');
  host.innerHTML = rail + peaks;
}

// The islands: the same data in three dimensions, loaded only when the section is near.
function tipFile(slug, rect) {
  const f = DRAWN[slug], p = BY[slug]; if (!f || !p) return;
  tip(`<span class="mono tip-no">${esc(CASE[p.slug])}</span> <b>${esc(nameOf(p))}</b><br><span class="tip-st s-${f.stage}">${esc(STAGES[f.stage].label)}</span> · stream ${esc(f.stream)} · idle ${idleOf(f)}d${f.next ? `<span class="tip-next">${esc(f.next.length > 170 ? f.next.slice(0, 168) + '…' : f.next)}</span>` : ''}`, rect);
}
function wireAscent3d() {
  const host = $('#ascent3d'), flatEl = $('#ascent'), toggle = $('#a3-toggle');
  $('#a3-legend').innerHTML = ['held', 'panel', 'working', 'blocked', 'unworked'].map(k => `<span class="k s-${k}"><i></i>${esc(STAGES[k].label)}</span>`).join('')
    + '<span class="k fogk"><i></i>Fog: idle 14+ days</span><span class="k beam"><i></i>Next firing</span>';
  const show = v => {
    host.hidden = v !== '3d'; flatEl.hidden = v === '3d';
    $$('button', toggle).forEach(b => b.setAttribute('aria-pressed', b.dataset.v === v));
  };
  let gl = false;
  try { const c = document.createElement('canvas'); gl = !!(c.getContext('webgl2') || c.getContext('webgl')); } catch { gl = false; }
  if (!STREAMS.length || !gl) { toggle.hidden = true; show('flat'); return; }
  show('3d');
  toggle.addEventListener('click', e => { const b = e.target.closest('button'); if (b) show(b.dataset.v); });
  new IntersectionObserver(async ([e], o) => {
    if (!e.isIntersecting) return;
    o.disconnect();
    try {
      const m = await import('./ascent3d.js');
      m.mount(host, {
        streams: STREAMS.map(s => ({ id: s.id, label: esc(s.label), files: s.files.map(f => ({ ...f, name: esc(clip(boardName(BY[f.slug]), 22)), idleNow: idleOf(f) })) })),
        pick: DATA.draw.pick, reduced: REDUCED, onOpen: openFile, onTip: tipFile, onUntip: untip,
      });
      host.classList.add('ready');
    } catch (err) {
      console.error('Islands unavailable, showing the flat chart', err);
      toggle.hidden = true; show('flat');
    }
  }, { rootMargin: '600px 0px' }).observe(host);
}

// ---- III. The wall -----------------------------------------------------------
// Files pinned by stream, red string between files the board's own dispatches name
// together. The layout is fixed; nothing drifts.

let WALL_MIN = 5;
const THREADS = (() => {
  const seen = new Set(), out = [];
  for (const [a, list] of Object.entries(DATA.connections || {})) for (const [b, w] of list) {
    const k = [a, b].sort().join('|');
    if (a === b || seen.has(k) || !DRAWN[a] || !DRAWN[b]) continue;
    seen.add(k); out.push({ a, b, w });
  }
  return out.sort((x, y) => y.w - x.w);
})();
const tilt = s => ((hash(s) % 60) - 30) / 10;

function paintWall() {
  if (!STREAMS.length) return;
  const order = ['held', 'panel', 'working', 'blocked', 'unworked'];
  $('#wall-cols').innerHTML = STREAMS.map(s => {
    const fs = [...s.files].sort((a, b) => order.indexOf(a.stage) - order.indexOf(b.stage) || b.debt - a.debt);
    return `<section class="w-col" aria-label="Stream ${esc(s.id)}"><h3 class="w-h"><b>${esc(s.id)}</b>${esc(s.label)}</h3><div class="w-cards">${fs.map(f => {
      const p = BY[f.slug];
      return `<button type="button" class="w-card s-${f.stage}${f.stage === 'held' ? ' big' : ''}${f.slug === DATA.draw.pick?.slug ? ' pick' : ''}" ${tipAttrs(f.slug)} style="--r:${tilt(f.slug)}deg">
        <span class="w-pin"></span><span class="w-no">${esc(CASE[f.slug] || '')} · stream ${esc(s.id)}</span>
        <span class="w-t">${esc(boardName(p))}</span><span class="w-foot"><span class="w-stamp">${esc(STAGES[f.stage].label)}</span><span>${idleOf(f)}d</span></span></button>`;
    }).join('')}</div></section>`;
  }).join('');
  const counts = [5, 3, 1].map(m => THREADS.filter(t => t.w >= m).length);
  $('#wall-ctl').innerHTML = `<span class="label">Show</span>${[[5, 'Strongest'], [3, 'Strong'], [1, 'Every thread']].map(([m, l], i) =>
    `<button type="button" data-min="${m}" aria-pressed="${m === WALL_MIN}">${l}<span class="mono">${counts[i]}</span></button>`).join('')}`;
  $('#wall-ctl').addEventListener('click', e => {
    const b = e.target.closest('[data-min]'); if (!b) return;
    WALL_MIN = +b.dataset.min;
    $$('#wall-ctl [data-min]').forEach(x => x.setAttribute('aria-pressed', x === b));
    drawStrings(); paintThreadList();
  });
  paintThreadList();
  const wall = $('#wall');
  wall.addEventListener('pointerover', e => { const c = e.target.closest('.w-card'); focusWall(c ? [c.dataset.slug] : null); });
  wall.addEventListener('pointerleave', () => focusWall(null));
  wall.addEventListener('focusin', e => { const c = e.target.closest('.w-card'); if (c) focusWall([c.dataset.slug]); });
  $('#wall-threads').addEventListener('pointerover', e => { const t = e.target.closest('[data-pair]'); focusWall(t ? t.dataset.pair.split('|') : null, true); });
  $('#wall-threads').addEventListener('pointerleave', () => focusWall(null));
  addEventListener('resize', () => requestAnimationFrame(drawStrings));
  document.fonts?.ready.then(drawStrings);
  new IntersectionObserver(([e], o) => { if (e.isIntersecting) { drawStrings(); o.disconnect(); } }).observe(wall);
  drawStrings();
}
function paintThreadList() {
  const list = THREADS.filter(t => t.w >= Math.max(WALL_MIN, 3)).slice(0, 8);
  $('#wall-threads').innerHTML = `<p class="label">Strongest threads</p><ol>${list.map(t =>
    `<li data-pair="${esc(t.a)}|${esc(t.b)}"><span class="wt-n mono">${t.w}</span><span><button type="button" class="linkish" data-slug="${esc(t.a)}">${esc(boardName(BY[t.a]))}</button> <i>and</i> <button type="button" class="linkish" data-slug="${esc(t.b)}">${esc(boardName(BY[t.b]))}</button></span></li>`).join('')}</ol>
    <p class="fine">The number is how many dispatches name both files. Hover a pair to pull its string; tap a name to open the file.</p>`;
}
function drawStrings() {
  const wall = $('#wall'), svgEl = $('#wall-strings');
  if (!wall || !svgEl) return;
  const box = wall.getBoundingClientRect();
  svgEl.setAttribute('viewBox', `0 0 ${box.width} ${box.height}`);
  const pin = s => { const c = $(`.w-card[data-slug="${CSS.escape(s)}"] .w-pin`, wall); if (!c) return null; const r = c.getBoundingClientRect(); return [r.left + r.width / 2 - box.left, r.top + r.height / 2 - box.top]; };
  svgEl.innerHTML = THREADS.filter(t => t.w >= WALL_MIN).map(t => {
    const A = pin(t.a), B = pin(t.b); if (!A || !B) return '';
    const len = Math.hypot(B[0] - A[0], B[1] - A[1]);
    const mx = (A[0] + B[0]) / 2, my = (A[1] + B[1]) / 2 + Math.min(110, len * .16);
    return `<path d="M${A[0].toFixed(1)} ${A[1].toFixed(1)}Q${mx.toFixed(1)} ${my.toFixed(1)} ${B[0].toFixed(1)} ${B[1].toFixed(1)}" stroke-width="${Math.min(3.4, .9 + t.w * .4).toFixed(2)}" data-a="${esc(t.a)}" data-b="${esc(t.b)}"/>`;
  }).join('');
}
function focusWall(slugs, pairOnly = false) {
  const wall = $('#wall');
  wall.classList.toggle('focus', !!slugs);
  $$('.w-card.on', wall).forEach(c => c.classList.remove('on'));
  $$('#wall-strings path.on').forEach(p => p.classList.remove('on'));
  if (!slugs) return;
  const on = new Set(slugs);
  $$('#wall-strings path').forEach(p => {
    const hit = pairOnly ? on.has(p.dataset.a) && on.has(p.dataset.b) : on.has(p.dataset.a) || on.has(p.dataset.b);
    if (!hit) return;
    p.classList.add('on'); on.add(p.dataset.a); on.add(p.dataset.b);
  });
  on.forEach(s => $(`.w-card[data-slug="${CSS.escape(s)}"]`, wall)?.classList.add('on'));
}

// ---- IV. The job ---------------------------------------------------------------
// The five crews as raccoons in trench coats, working a very large safe. Each one
// is doing its real job, and its record below comes from the commit log.

function rHead(p, x, y, c, s = 1, hat = true) {
  const head = svg('g', { transform: `translate(${x} ${y}) scale(${s})` }, p);
  head.innerHTML = `<path d="M-30 -14L-38 -40L-14 -28Z M30 -14L38 -40L14 -28Z" class="rc-ear"/><path d="M-29 -20L-33 -34L-20 -27Z M29 -20L33 -34L20 -27Z" class="rc-dark"/>
    <ellipse rx="36" ry="30" class="rc-fur"/><path d="M-34 -4Q-20 -16 0 -6Q20 -16 34 -4Q30 10 14 8Q0 2 -14 8Q-30 10 -34 -4Z" class="rc-dark"/>
    <ellipse cy="14" rx="15" ry="12" class="rc-muzzle"/><circle cx="-14" cy="-3" r="5" class="rc-eye"/><circle cx="14" cy="-3" r="5" class="rc-eye"/>
    <circle cx="-13" cy="-2" r="2.6" class="rc-pupil"/><circle cx="15" cy="-2" r="2.6" class="rc-pupil"/><ellipse cy="9" rx="5" ry="3.5" class="rc-pupil"/>
    <path d="M-22 -22Q0 -32 22 -22" class="rc-brow"/>${hat ? `<ellipse cy="-24" rx="48" ry="9" class="rc-brim"/><path d="M-28 -26Q-30 -62 0 -60Q30 -62 28 -26Z" class="rc-crown"/><path d="M-28 -32Q0 -26 28 -32V-40Q0 -34 -28 -40Z" style="fill:${c}"/><path d="M-10 -58Q0 -50 10 -58" class="rc-dent"/>` : ''}`;
  return head;
}
// A raccoon in a trench coat; (x, y) is the point between its feet.
function raccoon(p, { x, y, s = 1, c, flip = false, hat = true, head = true, coatH = 150, arm = null }) {
  const g = svg('g', { transform: `translate(${x} ${y}) scale(${flip ? -s : s} ${s})` }, p);
  const top = -coatH - 8;
  g.innerHTML = `<g transform="translate(30 -40) rotate(-28)">${Array.from({ length: 6 }, (_, i) => `<ellipse cx="${10 + i * 13}" rx="9" ry="${12 - i * .6}" class="${i % 2 ? 'rc-dark' : 'rc-fur'}"/>`).join('')}</g>
    <ellipse cx="-16" cy="-4" rx="13" ry="6" class="rc-foot"/><ellipse cx="16" cy="-4" rx="13" ry="6" class="rc-foot"/>
    <path d="M-30 ${top}Q-40 ${top + 40} -46 -8H46Q40 ${top + 40} 30 ${top}Z" class="rc-coat"/><path d="M0 ${top + 6}V-10" class="rc-seam"/>
    <path d="M-30 ${top}L-4 ${top + 34}L-18 ${top + 50}Z M30 ${top}L4 ${top + 34}L18 ${top + 50}Z" class="rc-lapel"/>
    <rect x="-42" y="${top + coatH * .55}" width="84" height="9" class="rc-belt"/><rect x="-6" y="${top + coatH * .55 - 1}" width="12" height="11" rx="2" class="rc-buckle"/>
    ${[top + 62, top + 90].map(by => `<circle cx="-9" cy="${by}" r="3" class="rc-btn"/><circle cx="9" cy="${by}" r="3" class="rc-btn"/>`).join('')}
    <circle cx="-18" cy="${top + 22}" r="5" style="fill:${c}" class="rc-badge"/>${arm ? arm(top) : ''}`;
  if (head) rHead(g, 0, top - 22, c, 1, hat);
  return g;
}
const sleeve = d => `<path d="${d}" class="rc-sleeve"/>`;
const paw = (x, y) => `<circle cx="${x}" cy="${y}" r="8" class="rc-dark"/>`;
function bubble(p, x, y, w, h, tx, ty, lines) {
  const g = svg('g', { class: 'rc-bubble' }, p);
  g.innerHTML = `<path d="M${x + 18} ${y + h}L${tx} ${ty}L${x + 42} ${y + h}Z"/><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="12"/><rect x="${x + 16}" y="${y + h - 3}" width="30" height="6" class="mend"/>
    ${lines.map(([t, cls, attrs], i) => `<text x="${x + 14}" y="${y + 24 + i * 20}" class="${cls || ''}" ${attrs || ''}>${esc(t)}</text>`).join('')}`;
  return g;
}

function paintJob() {
  const host = $('#job-scene');
  const W = 1400, H = 860, FLOOR = 800, SX = 850, SY = 410, SR = 330;
  const root = svg('svg', { viewBox: `0 0 ${W} ${H}`, role: 'img', 'aria-label': 'The five crews as raccoons in trench coats, working a giant safe marked PASS' });
  const u = k => `var(--u-${k})`;
  const best = Math.max(0, ...LIVE.map(p => gatesOf(stageOf(p))));
  const pick = DATA.draw?.pick, P = pick && BY[pick.slug];
  const ids = STREAMS.map(s => s.id);
  const nNew = Object.values(DRAWN).filter(f => f.slug.startsWith('discovered/')).length;
  let room = '';
  for (let x = 0; x < W; x += 140) room += `<rect x="${x + 6}" y="20" width="128" height="${FLOOR - 70}" rx="3" class="jb-panel"/>`;
  room += `<rect y="${FLOOR - 40}" width="${W}" height="40" class="jb-skirt"/>`;
  for (let x = 0; x < W; x += 70) room += `<rect x="${x}" y="${FLOOR}" width="70" height="${H - FLOOR}" class="jb-tile${(x / 70) % 2 ? ' alt' : ''}"/>`;
  // The safe.
  let safe = `<defs><radialGradient id="jb-steel" cx="42%" cy="38%" r="70%"><stop offset="0" stop-color="#5d6a73"/><stop offset="1" stop-color="#2a333a"/></radialGradient>
      <radialGradient id="jb-lamp"><stop offset="0" stop-color="#ffd38a"/><stop offset="1" stop-color="#f0884a"/></radialGradient></defs>
    <rect x="${SX - SR - 34}" y="${SY - SR - 34}" width="${SR * 2 + 68}" height="${SR * 2 + 68}" rx="14" class="jb-frame"/>
    <circle cx="${SX}" cy="${SY}" r="${SR}" fill="url(#jb-steel)" class="jb-door"/><circle cx="${SX}" cy="${SY}" r="${SR - 26}" class="jb-ring"/>`;
  for (let i = 0; i < 24; i++) { const a = i / 24 * Math.PI * 2; safe += `<circle cx="${(SX + Math.cos(a) * (SR - 13)).toFixed(1)}" cy="${(SY + Math.sin(a) * (SR - 13)).toFixed(1)}" r="5.5" class="jb-bolt"/>`; }
  for (const y of [SY - 200, SY + 200]) safe += `<rect x="${SX + SR - 6}" y="${y - 34}" width="40" height="68" rx="6" class="jb-hinge"/>`;
  safe += `<rect x="${SX - 110}" y="${SY - 250}" width="220" height="40" rx="4" class="jb-plate"/><text x="${SX}" y="${SY - 224}" class="jb-plate-t">PASS</text>`;
  ['OPEN', 'WORK', 'CLAIM', 'PANEL', 'HELD', 'PASS', 'SIGN'].forEach((g, i) => {
    const a = Math.PI * (1.18 + i * .107), x = SX + Math.cos(a) * 190, y = SY + Math.sin(a) * 190 + 40, on = i < best;
    safe += `${on ? `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="26" class="jb-glow"/>` : ''}<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="15" ${on ? 'fill="url(#jb-lamp)"' : ''} class="jb-lamp${on ? ' on' : ''}"><title>${esc(GATES[i])}: ${on ? 'clicked' : 'not yet'}</title></circle><text x="${x.toFixed(1)}" y="${(y + 32).toFixed(1)}" class="jb-lamp-t">${g}</text>`;
  });
  let ticks = '';
  for (let i = 0; i < 40; i++) { const a = i / 40 * Math.PI * 2; ticks += `<line x1="${(Math.cos(a) * 74).toFixed(1)}" y1="${(Math.sin(a) * 74).toFixed(1)}" x2="${(Math.cos(a) * (i % 10 ? 80 : 86)).toFixed(1)}" y2="${(Math.sin(a) * (i % 10 ? 80 : 86)).toFixed(1)}" class="jb-tick${i % 10 ? '' : ' major'}"/>`; }
  ids.forEach((id, i) => { const a = (i / 4) * Math.PI * 2 - Math.PI / 2; ticks += `<text x="${(Math.cos(a) * 56).toFixed(1)}" y="${(Math.sin(a) * 56).toFixed(1)}" class="jb-dial-t">${esc(id)}</text>`; });
  const pickAngle = -Math.max(0, ids.indexOf(pick?.stream)) * 90;
  safe += `<g transform="translate(${SX} ${SY + 40})"><circle r="104" class="jb-dial-o"/><circle r="86" class="jb-dial-i"/><g class="jb-rot" style="--a:${pickAngle}deg">${ticks}</g><circle r="30" class="jb-knob"/><path d="M0 -112l9 -14h-18Z" class="jb-index"/></g>`;
  safe += `<g transform="translate(${SX + 190} ${SY + 150})">${[0, 1, 2].map(i => { const a = i * Math.PI / 3; return `<line x1="${(Math.cos(a) * -54).toFixed(1)}" y1="${(Math.sin(a) * -54).toFixed(1)}" x2="${(Math.cos(a) * 54).toFixed(1)}" y2="${(Math.sin(a) * 54).toFixed(1)}" class="jb-spoke"/>`; }).join('')}<circle r="14" class="jb-hub"/></g>`;
  root.innerHTML = room + safe;
  const crew = k => svg('g', { class: 'jb-crew', 'data-unit': k, tabindex: 0, role: 'button', 'aria-label': `${UNIT[k].name}: show the crew record` }, root);

  // Pathfinders: in through the vent with a sack of new problems.
  {
    const g = crew('finder'), vx = 150, vy = 110, vw = 180, vh = 110;
    svg('rect', { x: vx, y: vy, width: vw, height: vh, rx: 6, class: 'jb-vent' }, g);
    rHead(g, vx + vw / 2, vy + vh - 26, u('finder'), .86);
    g.insertAdjacentHTML('beforeend', `<rect x="${vx - 4}" y="${vy + vh - 4}" width="${vw + 8}" height="10" rx="3" class="jb-lip"/>${paw(vx + vw / 2 - 34, vy + vh + 2)}${paw(vx + vw / 2 + 34, vy + vh + 2)}
      <line x1="${vx + vw / 2 + 34}" y1="${vy + vh + 6}" x2="${vx + vw / 2 + 50}" y2="${vy + vh + 40}" class="jb-cord"/>
      <path d="M${vx + vw / 2 + 30} ${vy + vh + 40}q22 -8 40 2q14 30 -8 44q-30 6 -40 -16q-4 -18 8 -30Z" class="jb-sack"/><text x="${vx + vw / 2 + 50}" y="${vy + vh + 74}" class="jb-sack-t">+${nNew}</text>
      <g transform="translate(${vx + 10} ${vy + 330}) rotate(-8)"><rect width="120" height="74" rx="4" class="jb-grille"/>${[1, 2, 3, 4, 5].map(i => `<line x1="8" x2="112" y1="${i * 12.3}" y2="${i * 12.3}" class="jb-grille-l"/>`).join('')}</g>`);
  }
  // The Irregulars: three raccoons, one coat, one hat.
  {
    const g = crew('irregular'), x = 104, sc = .95, coatH = 330;
    raccoon(g, { x, y: FLOOR - 4, s: sc, c: u('irregular'), coatH, head: false });
    const my = FLOOR - 4 - coatH * sc * .58;
    g.insertAdjacentHTML('beforeend', `${[-40, 40].map(dx => `<ellipse cx="${x + dx}" cy="${FLOOR - 8}" rx="11" ry="5" class="rc-foot"/>`).join('')}
      <path d="M${x - 22} ${my}Q${x} ${my - 14} ${x + 22} ${my}Q${x} ${my + 12} ${x - 22} ${my}Z" class="rc-dark"/>
      ${[x - 9, x + 9].map(ex => `<circle cx="${ex}" cy="${my}" r="4.5" class="rc-eye"/><circle cx="${ex + 1}" cy="${my + 1}" r="2.2" class="rc-pupil"/>`).join('')}
      <text x="${x}" y="${FLOOR + 40}" class="jb-tag" style="fill:${u('irregular')}">DEFINITELY A HUMAN</text>`);
    rHead(g, x, FLOOR - 4 - (coatH + 8) * sc - 22 * sc, u('irregular'), sc);
  }
  // The Tribunal: three seats, three placards.
  {
    const g = crew('validator');
    [['PARTIAL', 222], ['PARTIAL', 300], ['REFUTE?', 378]].forEach(([word, x], i) => {
      const r = [-5, 4, -3][i], sy = FLOOR - 236;
      g.insertAdjacentHTML('beforeend', `<line x1="${x + 22}" y1="${FLOOR - 100}" x2="${x + 22}" y2="${sy + 40}" class="jb-stick"/>
        <g transform="rotate(${r} ${x + 22} ${sy + 20})"><rect x="${x - 20}" y="${sy}" width="84" height="40" rx="3" class="jb-sign"/><text x="${x + 22}" y="${sy + 25}" class="jb-sign-t${i === 2 ? ' refute' : ''}">${word}</text></g>`);
      raccoon(g, { x, y: FLOOR + 20, s: .66, c: u('validator'), coatH: 118, arm: t => sleeve(`M20 ${t + 40}Q34 ${t + 20} 33 ${t - 6}`) + paw(33, t - 8) });
    });
  }
  // The Breakers: ear to the door, stethoscope on the dial.
  {
    const g = crew('breaker');
    raccoon(g, { x: 470, y: FLOOR - 4, s: 1.25, c: u('breaker'), coatH: 170 });
    g.insertAdjacentHTML('beforeend', `<path d="M478 ${FLOOR - 270}C520 ${FLOOR - 250} 520 ${FLOOR - 360} 560 ${FLOOR - 370}C620 ${FLOOR - 380} 700 ${FLOOR - 360} ${SX - 100} ${SY + 40}" class="jb-steth"/><circle cx="${SX - 100}" cy="${SY + 40}" r="11" class="jb-steth-h"/>`);
    if (P) { bubble(g, 390, 190, 280, 86, 486, 470, [[`Shh. Stream ${pick.stream}.`, 'b1'], [clip(boardName(P), 30), 'b2'], ['next firing in', 'b2']]); g.insertAdjacentHTML('beforeend', `<text x="528" y="254" class="rc-cd" data-countdown="breaker">--:--:--</text>`); }
  }
  // Overwatch: up the ladder, binoculars on the room.
  {
    const g = crew('orchestrator'), lx = 1270;
    let ladder = '';
    for (const dx of [-30, 30]) ladder += `<line x1="${lx + dx}" y1="${FLOOR}" x2="${lx + dx * .6}" y2="330" class="jb-ladder"/>`;
    for (let y = FLOOR - 40; y > 340; y -= 52) { const k = (FLOOR - y) / (FLOOR - 330) * 12; ladder += `<line x1="${lx - 30 + k}" x2="${lx + 30 - k}" y1="${y}" y2="${y}" class="jb-ladder"/>`; }
    g.insertAdjacentHTML('beforeend', ladder);
    raccoon(g, { x: lx, y: 340, s: .9, c: u('orchestrator'), coatH: 130, flip: true });
    const by = 340 - (130 + 8) * .9 - 22 * .9;
    g.insertAdjacentHTML('beforeend', `<rect x="${lx - 36}" y="${by - 12}" width="30" height="22" rx="7" class="jb-bino"/><rect x="${lx - 4}" y="${by - 12}" width="30" height="22" rx="7" class="jb-bino"/><circle cx="${lx - 21}" cy="${by - 1}" r="6" class="jb-lens"/><circle cx="${lx + 11}" cy="${by - 1}" r="6" class="jb-lens"/>`);
    const owed = DATA.draw?.overwatch?.length || 0;
    bubble(g, 1040, 70, 220, 66, 1210, 170, [['Overwatch here.', 'b1'], [`${owed} panel${owed === 1 ? '' : 's'} owed.`, 'b2']]);
  }
  host.appendChild(root);
  // The dial turns to the stream the next firing takes, once, when the scene comes into view.
  new IntersectionObserver(([e], o) => { if (e.isIntersecting) { root.classList.add('turned'); o.disconnect(); } }, { threshold: .3 }).observe(root);
  // A crew's record: tap or hover a raccoon.
  const record = k => {
    const acts = DATA.activity.filter(a => (a.unit === 'irregular' ? 'irregular' : a.role) === k);
    const wk = acts.filter(a => ageDays(a.date) <= 7).length, last = acts[0];
    return `<b>${esc(UNIT[k].name)}</b><br>${acts.length} commits in the log · ${wk} this week${last ? `<span class="tip-next">Last job, ${esc(rel(last.date))}: ${esc(last.subject)}</span>` : ''}`;
  };
  root.addEventListener('pointermove', e => { const c = e.target.closest('.jb-crew'); if (!c) return untip(); tip(record(c.dataset.unit), { left: e.clientX - 1, width: 2, top: e.clientY - 1, bottom: e.clientY + 1 }); });
  root.addEventListener('pointerleave', untip);
  root.addEventListener('click', e => { const c = e.target.closest('.jb-crew'); if (c) $(`.unit-card[data-role="${c.dataset.unit}"]`)?.scrollIntoView({ behavior: REDUCED ? 'auto' : 'smooth', block: 'center' }); });
  root.addEventListener('keydown', e => { if ((e.key === 'Enter' || e.key === ' ') && e.target.closest?.('.jb-crew')) { e.preventDefault(); e.target.closest('.jb-crew').dispatchEvent(new MouseEvent('click', { bubbles: true })); } });
  // On a phone, start the scene on the Breaker at the dial.
  const wrap = host;
  requestAnimationFrame(() => { if (wrap.scrollWidth > wrap.clientWidth) wrap.scrollLeft = (wrap.scrollWidth - wrap.clientWidth) * .32; });
}

// Departures and arrivals: the unit's timetable, on split-flap.
const FLAP = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
const flaps = (text, n) => {
  const s = String(text).toUpperCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^A-Z0-9 :·\-/×]/g, ' ').padEnd(n).slice(0, n);
  return `<span class="flaps" aria-label="${esc(String(text))}">${[...s].map(c => `<span class="f" data-c="${c === ' ' ? '' : esc(c)}" aria-hidden="true">${c === ' ' ? '&nbsp;' : esc(c)}</span>`).join('')}</span>`;
};
const hhmm = t => new Date(t).toISOString().slice(11, 16);
function firings(key, n) {
  const r = (DATA.routines || []).find(x => x.key === key); if (!r) return [];
  const out = []; let from = Date.now();
  while (out.length < n) { const t = nextFire(r.rule, from); if (!t) break; out.push(t); from = t + 1000; }
  return out;
}
let FLAP_W = 0;
function destWidth(timeChars) {
  const box = $('.fb-scroll'), probe = $('#flapboards .f');
  const cw = (probe ? probe.getBoundingClientRect().width : 16) + 1.5;
  const wide = innerWidth >= 720;
  const fixed = timeChars + (wide ? 11 : 0) + 1 + 8;
  const extra = (wide ? 5 : 4) * 8 + (wide ? 13 : 0) + 6;
  return Math.max(8, Math.min(24, Math.floor(((box?.clientWidth || 600) - extra) / cw) - fixed));
}
function paintFlapBoard(animate = false) {
  const narrow = innerWidth < 720;
  FLAP_W = innerWidth;
  const dw = destWidth(5), aw = destWidth(narrow ? 5 : 12);
  const ids = STREAMS.map(s => s.id), start = Math.max(0, ids.indexOf(DATA.draw?.pick?.stream));
  const dep = firings('breaker', 4).map((t, i) => {
    const sid = ids[(start + i) % ids.length], s = STREAMS.find(x => x.id === sid);
    const slug = i === 0 ? DATA.draw.pick.slug : s?.lead;
    return { t, unit: 'breaker', gate: sid || '·', dest: slug ? boardName(BY[slug]) : '—', slug };
  });
  dep.push(...firings('orchestrator', 1).map(t => ({ t, unit: 'orchestrator', gate: '·', dest: `Board pass · ${DATA.draw?.overwatch?.length || 0} panels` })));
  dep.push(...firings('finder', 1).map(t => ({ t, unit: 'finder', gate: '·', dest: 'Four new problems' })));
  dep.sort((a, b) => a.t - b.t);
  const status = r => { const m = (r.t - Date.now()) / 6e4; return m < 30 ? ['Boarding', 'boarding'] : m < 1440 ? ['On time', 'ontime'] : [dm(new Date(r.t).toISOString()), 'ontime']; };
  const unitName = k => UNIT[k].name.replace('The ', '');
  const head = cols => `<tr>${cols.map(c => `<th${c[1] ? ` class="${c[1]}"` : ''}>${c[0]}</th>`).join('')}</tr>`;
  $('#dep').innerHTML = head([['Time'], ['Unit', 'wide'], ['Gate'], ['Destination'], ['Status']]) + dep.map(r => {
    const [st, cls] = status(r);
    return `<tr${r.slug ? ` ${tipAttrs(r.slug)} class="go"` : ''}><td>${flaps(hhmm(r.t), 5)}</td><td class="wide"><i class="ud" style="background:var(--u-${r.unit})"></i>${flaps(unitName(r.unit), 11)}</td><td>${flaps(r.gate, 1)}</td><td>${flaps(r.dest, dw)}</td><td class="st-${cls}">${flaps(st, 8)}</td></tr>`;
  }).join('');
  const arr = DATA.activity.filter(a => a.problems?.length && BY[a.problems[0]] && ['breaker', 'validator', 'finder', 'orchestrator'].includes(a.role)).slice(0, 8).map(a => {
    const p = BY[a.problems[0]], st = stageOf(p), k = a.unit === 'irregular' ? 'irregular' : a.role;
    const s = st === 'blocked' ? ['Parked', 'parked'] : st === 'held' ? ['Held', 'held'] : k === 'finder' ? ['Filed', 'landed'] : ['Landed', 'landed'];
    return { a, p, k, s };
  });
  $('#arr').innerHTML = head([['Time'], ['Unit', 'wide'], ['Gate'], ['From'], ['Status']]) + arr.map(({ a, p, k, s }) =>
    `<tr ${tipAttrs(p.slug)} class="go"><td>${flaps(narrow ? hhmm(a.date) : `${dm(a.date)} ${hhmm(a.date)}`, narrow ? 5 : 12)}</td><td class="wide"><i class="ud" style="background:var(--u-${k})"></i>${flaps(unitName(k), 11)}</td><td>${flaps(DRAWN[p.slug]?.stream || '·', 1)}</td><td>${flaps(boardName(p), aw)}</td><td class="st-${s[1]}">${flaps(s[0], 8)}</td></tr>`).join('');
  if (animate && !REDUCED) $$('#flapboards .f').forEach((c, i) => {
    const final = c.dataset.c; if (!final) return;
    let n = 3 + (i % 6);
    const step = () => {
      c.classList.remove('flip'); void c.offsetWidth; c.classList.add('flip');
      if (--n <= 0) { c.textContent = final; return; }
      c.textContent = FLAP[(Math.random() * FLAP.length) | 0];
      setTimeout(step, 55);
    };
    setTimeout(step, 120 + (i % 24) * 22);
  });
}
function wireFlapBoard() {
  paintFlapBoard();
  new IntersectionObserver(([e], o) => { if (e.isIntersecting) { paintFlapBoard(true); o.disconnect(); } }, { threshold: .25 }).observe($('#flapboards'));
  // Re-letter when the layout crosses the phone breakpoint, and each minute so departed rows leave the board.
  addEventListener('resize', () => { if (Math.abs(innerWidth - FLAP_W) > 30) paintFlapBoard(); });
  setInterval(() => paintFlapBoard(), 60000);
}

// ---- V. Case files -------------------------------------------------------

const state = { domain: 'all', stage: 'all', q: '' };
const BOARD_ORDER = ['solved', 'pass', 'held', 'panel', 'working', 'unworked', 'blocked', 'method', 'withdrawn'];
const byStage = (a, b) => BOARD_ORDER.indexOf(stageOf(a)) - BOARD_ORDER.indexOf(stageOf(b)) || (b.commits30d - a.commits30d) || nameOf(a).localeCompare(nameOf(b));
let VISIBLE = [];

function paintControls() {
  const drawers = [{ key: 'all', label: 'All drawers', n: LIVE.length }, ...DATA.domains.map(d => ({ key: d.key, label: `${DOMAIN[d.key].drawer} · ${DOMAIN[d.key].short}`, n: LIVE.filter(p => p.domain === d.key).length }))];
  $('#drawers').innerHTML = drawers.map(d => `<button type="button" role="tab" data-domain="${d.key}" aria-selected="${d.key === 'all'}">${esc(d.label)}<span class="mono">${d.n}</span></button>`).join('');
  const stages = ['all', ...BOARD_ORDER].filter(k => k === 'all' || count(k));
  $('#stage-filter').innerHTML = stages.map(k => `<button type="button" class="chip${k === 'all' ? '' : ` s-${k}`}" data-stage="${k}" aria-pressed="${k === 'all'}">${k === 'all' ? 'Every stage' : esc(STAGES[k].label)}<span class="mono">${k === 'all' ? LIVE.length : count(k)}</span></button>`).join('');
  $('#drawers').addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; state.domain = b.dataset.domain; $$('#drawers button').forEach(x => x.setAttribute('aria-selected', x === b)); paintCabinet(); });
  $('#stage-filter').addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; state.stage = b.dataset.stage; $$('#stage-filter button').forEach(x => x.setAttribute('aria-pressed', x === b)); paintCabinet(); });
  let t; $('#search').addEventListener('input', e => { clearTimeout(t); t = setTimeout(() => { state.q = e.target.value.trim().toLowerCase(); paintCabinet(); }, 60); });
}

function matches(p) {
  if (state.domain !== 'all' && p.domain !== state.domain) return false;
  if (state.stage !== 'all' && stageOf(p) !== state.stage) return false;
  if (!state.q) return true;
  const hay = [nameOf(p), p.title, p.slug, CASE[p.slug], p.statusRow?.status, p.statusRow?.notes, p.lede, STAGES[stageOf(p)].label].join(' ').toLowerCase();
  return state.q.split(/\s+/).every(w => hay.includes(w));
}

function folder(p, i) {
  const st = p.statusRow?.status;
  const tilt = ((hash(p.id) % 7) - 3) * 0.9;
  return `
  <article class="folder paper s-${stageOf(p)}" data-slug="${esc(p.slug)}" tabindex="0" role="button" style="--tab:${(i % 3) * 30}%" aria-label="${esc(CASE[p.slug])} ${esc(nameOf(p))}, ${esc(STAGES[stageOf(p)].label)}">
    <span class="f-tab mono">${esc(CASE[p.slug])}</span>
    <header class="f-head typed"><span>${esc(DOMAIN[p.domain].short)}</span><span>${p.firstTouch ? `opened ${esc(dm(p.firstTouch))}` : ''}</span></header>
    <h4 class="f-title">${esc(nameOf(p))}</h4>
    <p class="f-status typed">${st ? md(st) : p.domain === 'discovered' ? 'Proposal, not yet promoted.' : 'No STATUS.md row.'}</p>
    <span class="rubber s-${stageOf(p)} f-stamp" style="--t:${tilt}deg">${esc(STAGES[stageOf(p)].stamp)}</span>
    ${FLAGS[p.slug].length ? `<span class="f-flag typed" title="${esc(FLAGS[p.slug].join(' '))}">⚑ ${FLAGS[p.slug].length === 1 ? 'Flag' : FLAGS[p.slug].length + ' flags'}</span>` : ''}
    <footer class="f-foot">${strip(p.commitDates90d, SPAN, 120, 18, 'ink')}${marks(p, 'sm')}<span class="typed">${esc(rel(p.lastTouch))}</span></footer>
  </article>`;
}

function paintCabinet() {
  const list = LIVE.filter(matches);
  VISIBLE = [];
  let html = '';
  for (const d of DATA.domains) {
    const rows = list.filter(p => p.domain === d.key).sort(byStage);
    if (!rows.length) continue;
    VISIBLE.push(...rows);
    html += `<div class="drawer"><h3 class="drawer-h"><span class="mono">Drawer ${DOMAIN[d.key].drawer}</span>${esc(d.label)}<span class="mono dim">${rows.length} file${rows.length === 1 ? '' : 's'}</span></h3>
      <div class="folders">${rows.map(folder).join('')}</div></div>`;
  }
  $('#cabinet').innerHTML = html || `<p class="empty">No file matches.</p>`;
  const keep = new Set(list.map(p => p.slug));
  $$('#scope-mini .blip').forEach(b => b.classList.toggle('dim', !keep.has(b.dataset.slug)));
  $('#mini-cap').textContent = `${list.length} of ${LIVE.length} files · the scope dims what the filter hides`;
}

function linkHover() {
  const hot = slug => $$('.blip').forEach(b => b.classList.toggle('hot', b.dataset.slug === slug));
  $('#cabinet').addEventListener('pointerover', e => { const r = e.target.closest('.folder'); hot(r ? r.dataset.slug : null); });
  $('#cabinet').addEventListener('pointerleave', () => hot(null));
  $('#cabinet').addEventListener('focusin', e => { const r = e.target.closest('.folder'); if (r) hot(r.dataset.slug); });
}

// ---- The open file --------------------------------------------------------

const SIGNALS = [['PROBLEM.md', 'hasProblem'], ['PROGRESS.md', 'hasProgress'], ['HANDOVER.md', 'hasHandover'], ['SOURCES.md', 'hasSources'],
  ['FREEZE.md', 'hasFreeze'], ['RESULTS.md', 'hasResults'], ['SOLUTION.md', 'hasSolution'], ['CLAIM.md', 'hasClaim'],
  ['analysis/', 'hasAnalysis'], ['code/', 'hasCode'], ['data/', 'hasData'], ['attempts/', 'hasAttempts']];
let lastFocus = null, current = null, closeTimer = null;

function openFile(slug) {
  const p = BY[slug]; if (!p) return;
  if (!current) lastFocus = document.activeElement;
  current = slug;
  clearTimeout(closeTimer); // a pending hide from a just-closed file must not hide this one
  const d = $('#dossier');
  const order = VISIBLE.length ? VISIBLE : [...LIVE].sort(byStage);
  const i = Math.max(0, order.findIndex(x => x.slug === slug));
  const prev = order[(i - 1 + order.length) % order.length], next = order[(i + 1) % order.length];
  const files = SIGNALS.filter(([, k]) => p.files[k]);
  const related = (DATA.dispatches || []).filter(x => x.problems?.includes(slug)).slice(0, 5);
  const st = stageOf(p);
  const field = (k, v) => `<div><dt>${k}</dt><dd>${v}</dd></div>`;
  d.innerHTML = `
    <div class="ds-bar">
      <span class="mono">File ${i + 1} of ${order.length}</span>
      <span class="ds-nav">
        <button type="button" data-go="${esc(prev?.slug || '')}" aria-label="Previous file">←</button>
        <button type="button" data-go="${esc(next?.slug || '')}" aria-label="Next file">→</button>
        <button type="button" class="ds-close" aria-label="Close file">esc</button>
      </span>
    </div>
    <div class="ds-body">
      <div class="sheet paper">
        <header class="lh">
          <div class="lh-l typed">Cracking Problems Hub<br>Research archive · ${esc(DOMAIN[p.domain].short)}</div>
          <div class="lh-r"><span class="typed">Case file</span><span class="lh-no mono">${esc(CASE[slug] || '—')}</span></div>
        </header>
        ${stampEl(p, 'ds-stamp')}
        <h2 id="dossier-title">${esc(p.title)}</h2>
        <dl class="fields typed">
          ${field('Folder', `<a href="${tree(p.slug)}" target="_blank" rel="noopener">${esc(p.slug)}/</a>`)}
          ${field('Stage', esc(STAGES[st].label) + (p.verdict && !['WORKING', 'PROMOTED'].includes(p.verdict) ? ` · ${esc(p.verdict)}` : ''))}
          ${field('Opened', p.firstTouch ? esc(toDate(p.firstTouch).toISOString().slice(0, 10)) : '—')}
          ${field('Last activity', `${esc(rel(p.lastTouch))} · ${p.commits30d} commits in 30 days`)}
        </dl>
        ${FLAGS[slug]?.length ? `<section class="ds-flags"><h3 class="typed">Flagged</h3><ul>${FLAGS[slug].map(f => `<li class="typed">${esc(f)}</li>`).join('')}</ul></section>` : ''}
        ${p.statusRow?.status ? `<section><h3 class="typed">Status, per STATUS.md</h3><p class="ds-status">${md(p.statusRow.status)}</p></section>` : ''}
        ${p.nextMove ? `<section class="ds-next"><h3 class="typed">Next move, per HANDOVER.md</h3><p class="typed"><mark>${esc(p.nextMove.text)}</mark></p><p class="typed ds-src">From “${esc(p.nextMove.heading)}” · <a href="${blob(p.slug + '/HANDOVER.md')}" target="_blank" rel="noopener">HANDOVER.md</a></p></section>` : ''}
        ${p.claim ? `<section class="ds-claim">
          <h3 class="typed">Validation queue — ${esc(p.claim.claim)}</h3>
          ${st === 'held' ? `<div class="pf-stamps sm">${['Validator', 'Validator', 'Refuter'].map((w, j) => `<span class="rubber partial" style="--t:${[-5, 3, -2][j]}deg">Partial<i>${w}</i></span>`).join('')}</div>` : ''}
          <p class="typed">${md(p.claim.disposition)}</p>
          <h3 class="typed">Action required</h3><p class="pf-check"><mark>${md(p.claim.missingCheck)}</mark></p>
          ${st === 'held' ? `<div class="pf-sign"><span class="typed">Human sign-off</span><span class="line"></span><span class="typed dim-ink">pending</span></div>` : ''}
        </section>` : ''}
        <section><h3 class="typed">${p.statusRow?.notes ? 'Notes, per STATUS.md' : 'Summary, per PROBLEM.md'}</h3>
          <p class="ds-notes">${p.statusRow?.notes ? md(p.statusRow.notes) : esc(p.lede || 'No summary recorded.')}</p></section>
        <section><h3 class="typed">Worked by</h3>${marks(p, 'lg')}
          ${strip(p.commitDates90d, SPAN, 480, 36, 'ink big')}
          ${p.lastSubject ? `<p class="typed ds-last">Last entry: “${esc(p.lastSubject)}”</p>` : ''}</section>
        <section><h3 class="typed">Enclosures</h3><p class="encl typed">${files.map(([n]) => `<a href="${n.endsWith('/') ? tree(p.slug + '/' + n.slice(0, -1)) : blob(p.slug + '/' + n)}" target="_blank" rel="noopener">${esc(n)}</a>`).join('')}</p></section>
        ${(DATA.connections?.[slug] || []).length ? `<section><h3 class="typed">Connected files</h3><p class="typed conn-note">Named in the same board/log entry: the route a method takes between folders.</p><div class="conn">${DATA.connections[slug].filter(([o]) => BY[o] && !BY[o].isStub).slice(0, 8).map(([o, w]) => `<button type="button" data-go="${esc(o)}"><span class="mono">${esc(CASE[o] || '')}</span>${esc(nameOf(BY[o]).replace(/\s*\(.*?\)\s*$/, ''))}<span class="w">×${w}</span></button>`).join('')}</div></section>` : ''}
        ${related.length ? `<section><h3 class="typed">Cross-references</h3><ul class="xref">${related.map(x => `<li><span class="typed">${esc(dm(x.date))}</span><a href="${blob(x.file)}" target="_blank" rel="noopener">${esc(x.title)}</a></li>`).join('')}</ul></section>` : ''}
      </div>
    </div>`;
  const opening = d.hidden;
  d.hidden = false; $('#scrim').hidden = false;
  document.body.classList.add('locked');
  requestAnimationFrame(() => d.classList.add('open'));
  $$('[data-go]', d).forEach(b => b.addEventListener('click', () => b.dataset.go && openFile(b.dataset.go)));
  $('.ds-close', d).addEventListener('click', closeFile);
  if (opening) $('.ds-close', d).focus();
  $('.ds-body', d).scrollTop = 0;
  scramble($('#dossier-title'), { speed: 8, spread: 160 });
  history.replaceState(null, '', `#p/${slug}`);
  $$('.blip').forEach(b => b.classList.toggle('sel', b.dataset.slug === slug));
}

function closeFile() {
  const d = $('#dossier'); if (d.hidden) return;
  d.classList.remove('open'); $('#scrim').hidden = true; document.body.classList.remove('locked');
  closeTimer = setTimeout(() => { d.hidden = true; }, 220);
  history.replaceState(null, '', location.pathname);
  $$('.blip.sel').forEach(b => b.classList.remove('sel'));
  current = null;
  lastFocus?.focus?.();
}

// ---- Palette --------------------------------------------------------------

let palIdx = 0, palList = [];
function openPalette() { $('#palette').hidden = false; $('#scrim').hidden = false; const i = $('#palette-input'); i.value = ''; renderPalette(''); i.focus(); }
function closePalette() { $('#palette').hidden = true; if ($('#dossier').hidden) $('#scrim').hidden = true; }
function renderPalette(q) {
  const t = q.toLowerCase().split(/\s+/).filter(Boolean);
  palList = LIVE.filter(p => { const h = `${nameOf(p)} ${p.slug} ${CASE[p.slug]} ${STAGES[stageOf(p)].label}`.toLowerCase(); return t.every(w => h.includes(w)); }).sort(byStage).slice(0, 9);
  palIdx = 0; paintPal();
}
function paintPal() {
  $('#palette-list').innerHTML = palList.map((p, i) => `<li role="option" aria-selected="${i === palIdx}" data-pi="${i}"><span class="mono pl-no">${esc(CASE[p.slug])}</span><span class="pl-name">${esc(nameOf(p))}</span><span class="badge s-${stageOf(p)}">${esc(STAGES[stageOf(p)].label)}</span></li>`).join('') || '<li class="dim">No file matches.</li>';
}

// ---- Tooltip + wiring -----------------------------------------------------

function tip(html, rect) {
  const t = $('#tip'); t.innerHTML = html; t.hidden = false;
  const r = t.getBoundingClientRect();
  const x = Math.min(innerWidth - r.width - 8, Math.max(8, rect.left + rect.width / 2 - r.width / 2));
  const y = rect.top - r.height - 10 < 60 ? rect.bottom + 10 : rect.top - r.height - 10;
  t.style.transform = `translate(${Math.round(x)}px,${Math.round(y)}px)`;
}
const untip = () => { $('#tip').hidden = true; };

function wire() {
  document.addEventListener('click', e => {
    if (e.target.closest('a')) return;
    const pi = e.target.closest('[data-pi]');
    if (pi) { closePalette(); openFile(palList[+pi.dataset.pi].slug); return; }
    const t = e.target.closest('[data-slug]');
    if (t && !t.closest('.dossier')) openFile(t.dataset.slug);
  });
  document.addEventListener('keydown', e => {
    const palOpen = !$('#palette').hidden;
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); palOpen ? closePalette() : openPalette(); return; }
    if (palOpen) {
      if (e.key === 'Escape') { closePalette(); return; }
      if (e.key === 'ArrowDown' || e.key === 'ArrowUp') { e.preventDefault(); palIdx = (palIdx + (e.key === 'ArrowDown' ? 1 : -1) + palList.length) % Math.max(1, palList.length); paintPal(); return; }
      if (e.key === 'Enter' && palList[palIdx]) { const s = palList[palIdx].slug; closePalette(); openFile(s); }
      return;
    }
    if (e.key === 'Escape') { closeFile(); return; }
    if (current && (e.key === 'ArrowRight' || e.key === 'ArrowLeft')) { $$('[data-go]', $('#dossier'))[e.key === 'ArrowLeft' ? 0 : 1]?.click(); return; }
    if ((e.key === 'Enter' || e.key === ' ') && e.target.closest?.('[data-slug][tabindex]')) { e.preventDefault(); openFile(e.target.closest('[data-slug]').dataset.slug); return; }
    if (e.key === '/' && !e.target.matches('input, textarea')) { e.preventDefault(); openPalette(); }
  });
  $('#palette-input').addEventListener('input', e => renderPalette(e.target.value));
  $('#jump-open').addEventListener('click', openPalette);
  $('#scrim').addEventListener('click', () => { closePalette(); closeFile(); });
  document.addEventListener('pointerover', e => {
    const b = e.target.closest('.blip'); if (!b) return;
    const p = BY[b.dataset.slug];
    tip(`<span class="mono tip-no">${esc(CASE[p.slug])}</span> <b>${esc(nameOf(p))}</b><br><span class="tip-st s-${stageOf(p)}">${esc(STAGES[stageOf(p)].label)}</span> · ${esc(rel(p.lastTouch))}`, b.querySelector('.core').getBoundingClientRect());
  });
  document.addEventListener('pointerout', e => { if (e.target.closest('.blip, .fc, [data-tip]')) untip(); });
  const files = Object.fromEntries((DATA.draw?.streams || []).flatMap(s => s.files).map(f => [f.slug, f]));
  document.addEventListener('pointerover', e => {
    const c = e.target.closest('.fc, [data-tip]'); if (!c || e.pointerType === 'touch') return;
    const f = files[c.dataset.slug]; if (!f) return;
    const p = BY[f.slug];
    tip(`<span class="mono tip-no">${esc(CASE[p.slug])}</span> <b>${esc(nameOf(p))}</b><br><span class="tip-st s-${f.stage}">${esc(STAGES[f.stage].label)}</span> · idle ${idleOf(f)}d · debt ${Math.round(f.debt)}${f.next ? `<span class="tip-next">${esc(f.next.length > 170 ? f.next.slice(0, 168) + '…' : f.next)}</span>` : ''}`, c.getBoundingClientRect());
  });
  $$('[data-scramble]').forEach(h => new IntersectionObserver(([x], o) => { if (x.isIntersecting) { scramble(h); o.disconnect(); } }, { threshold: 0.6 }).observe(h));
  const fromHash = () => { const m = location.hash.match(/^#p\/(.+)$/); if (m && m[1] !== current) openFile(decodeURIComponent(m[1])); };
  addEventListener('hashchange', fromHash);
  fromHash();
}

function paintFoot() {
  const h = DATA.history || {};
  $('#foot-meta').innerHTML = [
    `built ${new Date(DATA.generatedAt).toISOString().replace('T', ' ').slice(0, 16)}Z`,
    h.available ? `${h.commits} commits${h.shallow ? ', shallow clone' : ''}` : 'no git history in this build',
    `${DATA.totals.stubs} MOVED stubs not counted`,
    `<a href="/data.json">data.json</a>`,
    `<a href="${REPO}" target="_blank" rel="noopener">source</a>`,
  ].join('<span class="sep">·</span>');
}

// ---- Boot -----------------------------------------------------------------

paintTicker();
paintHero();
paintFiring();
paintBoard();
paintPriority();
paintAscent();
wireAscent3d();
paintWall();
paintJob();
wireFlapBoard();
paintUnits();
paintControls();
buildScope($('#scope-mini'), { mini: true });
paintCabinet();
linkHover();
paintFoot();
wire();
tick();
setInterval(tick, 1000);
if (!REDUCED) requestAnimationFrame(spin);
