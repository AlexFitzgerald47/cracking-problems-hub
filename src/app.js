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
const blob = p => `${REPO}/blob/main/${p}`;
const tree = p => `${REPO}/tree/main/${p}`;

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
  backlog:   { label: 'Backlog',       stamp: 'Proposed',   r: 0.86, order: 7, ring: 'Backlog' },
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
  'discovered': { short: 'Backlog', drawer: 'E', prefix: 'P' },
};

// The unit. Callsigns are this site's; creeds and models are quoted from the
// repository (_roles/*.md, board/SCHEDULE.md) at build time.
const UNITS = [
  { key: 'cracker', no: '01', name: 'The Breakers', role: 'Cracker', orders: 'Takes an unclaimed problem, or advances a held one, and works it against primary evidence.' },
  { key: 'validator', no: '02', name: 'The Tribunal', role: 'Validator', orders: 'Three seats, one of them the refuter. Convened by Overwatch whenever a solve-claim is waiting.' },
  { key: 'orchestrator', no: '03', name: 'Overwatch', role: 'Orchestrator', orders: 'Reads the whole board, breaks silos between folders, keeps STATUS.md honest.' },
  { key: 'finder', no: '04', name: 'Pathfinders', role: 'Finder', orders: 'Brings back four verified problems a run, and checks nobody solved them first.' },
  { key: 'irregular', no: '05', name: 'The Irregulars', role: 'Outside the routines', orders: 'Sessions run by hand: the Codex lane and the human. Not configured from this repository.' },
];
const UNIT = Object.fromEntries(UNITS.map(u => [u.key, u]));

// Insignia: one geometric idea per unit, drawn on a 64-unit grid.
const SIGIL = {
  cracker: '<circle cx="32" cy="32" r="15"/><path d="M33 13l-5 9 7 6-6 8 5 6-3 9"/><path d="M20 44l-6 6M44 20l6-6"/>',
  validator: '<path d="M16 24L32 14l16 10z"/><path d="M22 27v17M32 27v17M42 27v17M15 47h34"/>',
  orchestrator: '<circle cx="32" cy="32" r="16"/><circle cx="32" cy="32" r="7"/><circle cx="32" cy="32" r="1.6" class="fill"/><path d="M32 10v6M32 48v6M10 32h6M48 32h6M32 32l11-11"/>',
  finder: '<path d="M32 11l4.5 16.5L53 32l-16.5 4.5L32 53l-4.5-16.5L11 32l16.5-4.5z"/><path d="M32 18v8"/>',
  irregular: '<path d="M32 12l17 10v20L32 52 15 42V22z" stroke-dasharray="4 4"/><path d="M32 24l7 8-7 8-7-8z"/>',
};
const sigil = (k, cls = '') => `<svg class="sigil ${cls}" viewBox="0 0 64 64" aria-hidden="true">${SIGIL[k] || ''}</svg>`;

const LIVE = DATA.problems.filter(p => !p.isStub);
const BY = Object.fromEntries(DATA.problems.map(p => [p.slug, p]));
const stageOf = p => STAGES[p.stage] ? p.stage : 'working';
const nameOf = p => p.shortTitle || p.title;
const count = k => LIVE.filter(p => stageOf(p) === k).length;
const hash = s => [...s].reduce((h, c) => (h * 31 + c.charCodeAt(0)) >>> 0, 7);
const sectorOf = p => {
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
  if (st === 'unworked' && (p.roleTouches?.cracker || 0) > 0) f.push(`STATUS.md says never worked, but cracker sessions have committed here ${p.roleTouches.cracker} time${p.roleTouches.cracker === 1 ? '' : 's'}.`);
  if (st === 'working' && ageDays(p.lastTouch) > 14) f.push(`Listed as in work, but no commit for ${Math.floor(ageDays(p.lastTouch))} days.`);
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
    `<a href="${REPO}/commit/${DATA.repo.headSha}" target="_blank" rel="noopener">${esc(sha7(DATA.repo.headSha))}</a>`]
    .filter(Boolean).join('<span class="sep">·</span>');
  const lead = passed === 0
    ? `${Words(live)} problems.${day ? ` ${Words(day)} days.` : ''} Nothing cracked.`
    : `${Words(live)} problems. ${Words(passed)} cracked.`;
  $('#bluf').innerHTML = `<span class="l1">${esc(lead)}</span>` +
    (held ? `<span class="l2"><em>${Words(held)} ${held === 1 ? 'claim sits' : 'claims sit'} one signature out.</em></span>` : '');
  const su = DATA.statusUpdated;
  if (su) $('#bluf-sub').innerHTML = `The latest pass, ${esc(dm(su.date))}: ${esc(su.label)}${su.detail ? ` — ${md(su.detail)}` : ''}.${su.report ? ` <a href="${blob(su.report)}" target="_blank" rel="noopener">Read it</a>.` : ''}`;
  const k = [
    { n: live, l: 'live problems' },
    { n: held, l: 'held at 3×PARTIAL', c: 'held' },
    { n: count('panel'), l: 'awaiting a panel', c: 'panel' },
    { n: passed, l: 'passed', c: passed ? 'pass' : 'zero' },
    { n: DATA.totals.research7d ?? '—', l: 'research commits, 7 days' },
    { n: LIVE.filter(p => !['backlog', 'withdrawn'].includes(stageOf(p)) && ageDays(p.lastTouch) > 7).length, l: 'gone cold, 7+ days untouched', c: 'cold' },
  ];
  $('#kpis').innerHTML = k.map(x => `<div class="kpi" ${x.c ? `data-c="${x.c}"` : ''}><span class="kpi-n mono">${esc(x.n)}</span><span class="kpi-l">${esc(x.l)}</span></div>`).join('');
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
    if (!mini) {
      const n = k === 'working' ? count('working') + count('blocked') : count(k);
      svg('text', { x: 8, y: -s.r * R - 6, class: 'ring-label' }, face).textContent = `${s.ring.toUpperCase()}  ${n}`;
    }
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
    const n = LIVE.filter(p => sectorOf(p) === s.key).length;
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
    svg('circle', { r: Math.max(size * 2.2, 16), class: 'hit' }, g);
    const idle = ageDays(p.lastTouch);
    const expected = !['backlog', 'withdrawn'].includes(st);
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
  const last = DATA.lastByRole?.cracker;
  const target = !mini && last?.problems?.map(s => nodes.find(n => n.p.slug === s)).find(Boolean);
  if (target) {
    const { x, y, size } = target, o = size + 9, l = 7;
    mark = svg('g', { class: 'sortie', transform: `translate(${x.toFixed(1)} ${y.toFixed(1)})` }, root);
    for (const [sx, sy] of [[-1, -1], [1, -1], [1, 1], [-1, 1]]) {
      svg('path', { d: `M${sx * o} ${sy * (o - l)}V${sy * o}H${sx * (o - l)}` }, mark);
    }
    const right = x < 150;
    svg('text', { x: right ? o + 10 : -o - 10, y: 4, 'text-anchor': right ? 'start' : 'end' }, mark).textContent = `LAST SORTIE · ${rel(last.date).toUpperCase()}`;
  }

  host.appendChild(root);
  const scope = { mini, R, root, sweep, nodes, by: Object.fromEntries(nodes.map(n => [n.p.slug, n])), links, pulses, agentLayer, visible: true };
  nodes.forEach(n => n.g.style.setProperty('--g', REDUCED ? n.base + 0.2 : n.base));
  scopes.push(scope);
  new IntersectionObserver(([e]) => { scope.visible = e.isIntersecting; }).observe(host);
  return scope;
}

// ---- Scope modes: live, replay, neglect -------------------------------------

let MODE = 'live', HERO = null;
const PERIOD = 9000;
let lastT = 0;
function spin(t) {
  const dt = Math.min(64, t - (lastT || t)); lastT = t;
  const a = (t % PERIOD) / PERIOD * 360;
  for (const s of scopes) {
    if (!s.visible) continue;
    const neglect = MODE === 'neglect' && !s.mini;
    s.sweep.style.display = neglect ? 'none' : '';
    s.sweep.setAttribute('transform', `rotate(${a.toFixed(2)})`);
    for (const n of s.nodes) {
      if (neglect) { n.g.style.setProperty('--g', n.neglect.toFixed(3)); continue; }
      const behind = (a - n.deg + 360) % 360;
      const glow = behind < 320 ? Math.exp(-behind / 50) : 0;
      n.g.style.setProperty('--g', Math.min(1, n.base + glow * 0.9).toFixed(3));
    }
  }
  if (HERO?.visible) { stepAgents(t, dt); stepPulses(t); if (MODE === 'replay') stepReplay(dt); }
  if (!document.hidden) requestAnimationFrame(spin);
}
document.addEventListener('visibilitychange', () => { if (!document.hidden && !REDUCED) { lastT = 0; requestAnimationFrame(spin); } });

// Agents: one marker per sortie, in its unit's colour. They fly in from the
// rim, circle the file they are working, and leave when the work is done.
let agents = [], pulseList = [];
const unitOf = a => a.unit === 'irregular' ? 'irregular' : a.role;
function spawnAgent(role, slug, { dwell = 1600, refuter = false, delay = 0 } = {}) {
  const n = HERO?.by[slug];
  if (!n || REDUCED) return;
  const [sx, sy] = polar(Math.random() * 360, HERO.R * 1.2);
  const g = svg('g', { class: 'agent', 'data-role': role }, HERO.agentLayer);
  const trail = svg('polyline', { class: 'trail' }, g);
  const body = svg('g', {}, g);
  svg('path', { d: 'M0 -10L7.5 7L0 3.5L-7.5 7Z', class: 'body' }, body);
  if (refuter) svg('circle', { r: 13, class: 'refuter' }, body);
  agents.push({ g, trail, body, n, x: sx, y: sy, pts: [], phase: 'wait', t0: performance.now() + delay, dwell, orbit: Math.random() * 6.28, dir: Math.random() < .5 ? 1 : -1 });
}
function pulse(n, cls = '', max = 46) {
  if (REDUCED || !HERO) return;
  const c = svg('circle', { cx: n ? n.x : 0, cy: n ? n.y : 0, r: n ? n.size : 10, class: `pulse ${cls}` }, HERO.pulses);
  if (n) c.setAttribute('data-stage', stageOf(n.p));
  pulseList.push({ c, r0: n ? n.size : 10, max, t0: performance.now(), dur: n ? 900 : 1600 });
}
function stepPulses(t) {
  pulseList = pulseList.filter(p => {
    const k = (t - p.t0) / p.dur;
    if (k >= 1) { p.c.remove(); return false; }
    p.c.setAttribute('r', (p.r0 + (p.max) * k).toFixed(1));
    p.c.style.opacity = (1 - k) * 0.8;
    return true;
  });
}
function stepAgents(t, dt) {
  agents = agents.filter(a => {
    if (a.phase === 'wait') { if (t < a.t0) return true; a.phase = 'travel'; }
    const n = a.n;
    let hx = 0, hy = -1;
    if (a.phase === 'travel') {
      const dx = n.x - a.x, dy = n.y - a.y, d = Math.hypot(dx, dy);
      const reach = n.size + 18;
      if (d <= reach + 2) { a.phase = 'work'; a.t0 = t; pulse(n); }
      else { const v = Math.min(d - reach, 0.75 * dt); a.x += dx / d * v; a.y += dy / d * v; hx = dx; hy = dy; }
    }
    if (a.phase === 'work') {
      a.orbit += 0.0022 * dt * a.dir;
      const r = n.size + 18;
      const nx = n.x + Math.cos(a.orbit) * r, ny = n.y + Math.sin(a.orbit) * r;
      hx = nx - a.x; hy = ny - a.y; a.x = nx; a.y = ny;
      if (t - a.t0 > a.dwell) { a.phase = 'leave'; a.t0 = t; }
    }
    if (a.phase === 'leave') {
      const k = (t - a.t0) / 900;
      if (k >= 1) { a.g.remove(); return false; }
      const d = Math.hypot(a.x, a.y) || 1;
      a.x += a.x / d * 0.5 * dt; a.y += a.y / d * 0.5 * dt; hx = a.x; hy = a.y;
      a.g.style.opacity = 1 - k;
    }
    a.pts.push(`${a.x.toFixed(1)},${a.y.toFixed(1)}`);
    if (a.pts.length > 10) a.pts.shift();
    a.trail.setAttribute('points', a.pts.join(' '));
    const h = Math.atan2(hy, hx) * 180 / Math.PI + 90;
    a.body.setAttribute('transform', `translate(${a.x.toFixed(1)} ${a.y.toFixed(1)}) rotate(${h.toFixed(0)})`);
    return true;
  });
}
function clearAgents() { agents.forEach(a => a.g.remove()); agents = []; pulseList.forEach(p => p.c.remove()); pulseList = []; }

// A sortie is one commit by one unit against one or more files.
function deploy(ev, dwell) {
  const role = unitOf(ev);
  if (role === 'orchestrator') {
    pulse(null, 'overwatch', HERO.R);
    ev.problems.slice(0, 4).forEach(s => HERO.by[s] && pulse(HERO.by[s]));
    return;
  }
  ev.problems.slice(0, 3).forEach((s, i) => {
    if (role === 'validator') {
      [0, 1, 2].forEach(j => spawnAgent('validator', s, { dwell, refuter: j === 2, delay: j * 160 }));
    } else spawnAgent(role, s, { dwell, delay: i * 120 });
  });
}

const EVENTS = DATA.activity
  .filter(a => ['cracker', 'validator', 'finder', 'orchestrator'].includes(a.role) && (a.problems?.length || a.role === 'orchestrator'))
  .slice().reverse();
let rIdx = 0, rPlaying = false, rAcc = 0;
const R_STEP = 420;

function setUnborn(dateIso) {
  for (const n of HERO.nodes) {
    const unborn = dateIso && n.p.firstTouch && n.p.firstTouch > dateIso;
    n.g.classList.toggle('unborn', !!unborn);
  }
}
function showEvent(i) {
  const ev = EVENTS[Math.max(0, i - 1)];
  $('#t-range').value = i;
  if (!ev) { $('#t-stamp').textContent = ''; return; }
  const who = UNIT[unitOf(ev)]?.name || ev.role;
  const d = new Date(ev.date).toISOString();
  $('#t-stamp').innerHTML = `<b>${esc(dm(d))} ${d.slice(11, 16)}Z</b> <span data-role="${esc(unitOf(ev))}"><i></i>${esc(who)}</span> ${esc(ev.subject)}`;
  setUnborn(ev.date);
}
function stepReplay(dt) {
  if (!rPlaying) return;
  rAcc += dt;
  if (rAcc < R_STEP) return;
  rAcc = 0;
  if (rIdx >= EVENTS.length) { rPlaying = false; $('#t-play').textContent = '▶'; return; }
  deploy(EVENTS[rIdx], 900);
  rIdx++;
  showEvent(rIdx);
}

function spawnLive() {
  // Units that went out in the last 72 hours are shown still at work.
  const seen = new Set();
  const recent = DATA.activity.filter(a => ['cracker', 'validator', 'finder'].includes(a.role) && a.problems?.length && ageDays(a.date) < 3);
  let k = 0;
  for (const ev of recent) {
    const s = ev.problems[0];
    if (seen.has(s) || k >= 8) continue;
    seen.add(s);
    const role = unitOf(ev);
    if (role === 'validator') [0, 1, 2].forEach(j => spawnAgent('validator', s, { dwell: Infinity, refuter: j === 2, delay: k * 500 + j * 160 }));
    else spawnAgent(role, s, { dwell: Infinity, delay: k * 500 });
    k++;
  }
  return k;
}

const CAPTIONS = {
  live: () => `Distance from centre is distance from cracked; the centre is <b>PASS</b>. The sweep is Overwatch: it brightens each file by how recently a session touched it. Markers circling a file are units that went in during the last 72 hours.`,
  replay: () => `The board's history, commit by commit. Files appear on the scope when their folder was opened; stages shown are today's, not those at the time.`,
  neglect: () => `Brightness is time since a session last touched the file; the six coldest files that should be moving are labelled. Backlog proposals are dimmed because nobody is meant to be working them.`,
};
function setMode(m) {
  MODE = m;
  $$('.scope-modes button').forEach(b => b.setAttribute('aria-pressed', b.dataset.mode === m));
  $('#transport').hidden = m !== 'replay';
  HERO.root.classList.toggle('m-neglect', m === 'neglect');
  HERO.root.classList.toggle('m-replay', m === 'replay');
  clearAgents();
  rPlaying = false; $('#t-play').textContent = '▶';
  setUnborn(null);
  if (m === 'live') spawnLive();
  if (m === 'replay') { rIdx = 0; rAcc = 0; showEvent(0); setUnborn('0'); rPlaying = true; $('#t-play').textContent = '❚❚'; }
  if (m === 'neglect' && REDUCED) HERO.nodes.forEach(n => n.g.style.setProperty('--g', n.neglect));
  $('#scope-cap').innerHTML = CAPTIONS[m]();
}

function wireScope() {
  $('.scope-modes').addEventListener('click', e => { const b = e.target.closest('button'); if (b) setMode(b.dataset.mode); });
  const range = $('#t-range');
  range.max = EVENTS.length;
  range.addEventListener('input', () => { rPlaying = false; $('#t-play').textContent = '▶'; clearAgents(); rIdx = +range.value; showEvent(rIdx); });
  $('#t-play').addEventListener('click', () => {
    if (rIdx >= EVENTS.length) { rIdx = 0; clearAgents(); showEvent(0); setUnborn('0'); }
    rPlaying = !rPlaying; $('#t-play').textContent = rPlaying ? '❚❚' : '▶';
  });
  // Hovering a file draws the board's own links: files named in the same dispatch.
  const draw = slug => {
    HERO.links.innerHTML = '';
    HERO.nodes.forEach(n => n.g.classList.remove('linked'));
    if (!slug) return;
    const from = HERO.by[slug]; if (!from) return;
    for (const [other, w] of (DATA.connections?.[slug] || []).slice(0, 12)) {
      const to = HERO.by[other]; if (!to || to.g.classList.contains('unborn')) continue;
      svg('line', { x1: from.x, y1: from.y, x2: to.x, y2: to.y, class: 'link', 'stroke-width': Math.min(4, 0.8 + w * 0.7) }, HERO.links);
      to.g.classList.add('linked');
    }
  };
  HERO.root.addEventListener('pointerover', e => { const b = e.target.closest('.blip'); if (b) draw(b.dataset.slug); });
  HERO.root.addEventListener('pointerleave', () => draw(null));
  HERO.root.addEventListener('focusin', e => { const b = e.target.closest('.blip'); if (b) draw(b.dataset.slug); });
}

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

// ---- II. The Unit ---------------------------------------------------------

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
      <div class="uc-last">${l ? `<span class="label">Last sortie · ${esc(rel(l.date))}</span><a href="${REPO}/commit/${l.sha}" target="_blank" rel="noopener">${esc(l.subject)}</a>${l.problems?.length ? `<div class="pchips">${chips(l.problems)}</div>` : ''}` : '<span class="label">No sortie in window</span>'}</div>
    </article>`;
  }).join('');
}

// ---- III. Case files ------------------------------------------------------

const state = { domain: 'all', stage: 'all', q: '' };
const BOARD_ORDER = ['solved', 'pass', 'held', 'panel', 'working', 'unworked', 'blocked', 'backlog', 'withdrawn'];
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
let lastFocus = null, current = null;

function openFile(slug) {
  const p = BY[slug]; if (!p) return;
  if (!current) lastFocus = document.activeElement;
  current = slug;
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
  setTimeout(() => { d.hidden = true; }, 220);
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
  document.addEventListener('pointerout', e => { if (e.target.closest('.blip')) untip(); });
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
HERO = buildScope($('#scope'));
wireScope();
paintPriority();
paintUnits();
paintControls();
buildScope($('#scope-mini'), { mini: true });
paintCabinet();
linkHover();
paintFoot();
wire();
tick();
setInterval(tick, 1000);
setMode('live');
if (!REDUCED) requestAnimationFrame(spin);
