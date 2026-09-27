// Cracking Problems Hub — the scope.
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
const dm = iso => { const d = new Date(iso.length === 10 ? iso + 'T00:00:00Z' : iso); return `${d.getUTCDate()} ${MON[d.getUTCMonth()]}`; };
const ageDays = iso => iso ? (NOW - new Date(iso.length === 10 ? iso + 'T00:00:00Z' : iso).getTime()) / DAY : Infinity;
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

// Radius is closeness to cracked: 0 is PASS, 1 is the edge of the scope.
const STAGES = {
  solved:    { label: 'Solved',        r: 0.00, order: 0 },
  pass:      { label: 'PASS',          r: 0.00, order: 1 },
  held:      { label: 'Held',          r: 0.27, order: 2, ring: 'Held · 3×PARTIAL' },
  panel:     { label: 'Panel pending', r: 0.41, order: 3, ring: 'Panel pending' },
  working:   { label: 'In work',       r: 0.56, order: 4, ring: 'In work' },
  blocked:   { label: 'Blocked',       r: 0.56, order: 5 },
  unworked:  { label: 'Unworked',      r: 0.71, order: 6, ring: 'Unworked' },
  backlog:   { label: 'Backlog',       r: 0.86, order: 7, ring: 'Backlog' },
  withdrawn: { label: 'Withdrawn',     r: 0.97, order: 8 },
};
const SECTORS = [
  { key: 'ciphers', label: 'Ciphers' },
  { key: 'historical-texts', label: 'Undeciphered texts' },
  { key: 'historical-controversies', label: 'Controversies' },
  { key: 'ireland', label: 'Ireland' },
];
const DOMAIN_SHORT = { 'ciphers': 'Ciphers', 'historical-texts': 'Texts', 'historical-controversies': 'Controversies', 'ireland': 'Ireland', 'discovered': 'Backlog' };
const ROLES = [
  { key: 'cracker', label: 'Cracker' },
  { key: 'validator', label: 'Validator' },
  { key: 'orchestrator', label: 'Orchestrator' },
  { key: 'finder', label: 'Finder' },
];

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

// ---- Decrypt effect -------------------------------------------------------
// Headlines resolve out of ogham, runes and Greek: the scripts this board works on.

const GLYPHS = 'ᚁᚂᚃᚄᚅᚆᚇᚈᚉᚊᚋᚌᚍᚎᚏᚐᚑᚒᚓᚔᚠᚢᚦᚨᚱᚲᚷᚹᚺᚾᛁᛃᛇᛈᛉᛊᛏᛒᛖᛗᛚᛜᛞᛟΔΘΛΞΠΣΦΨ';
function scramble(el, { speed = 16, spread = 260 } = {}) {
  if (REDUCED || el.dataset.done) return;
  el.dataset.done = '1';
  const h = el.getBoundingClientRect().height;
  el.style.minHeight = h + 'px';
  const nodes = [];
  const walk = n => n.nodeType === 3 ? nodes.push(n) : n.childNodes.forEach(walk);
  walk(el);
  let i = 0;
  const items = nodes.map(n => {
    const final = n.nodeValue;
    const at = [...final].map(ch => /\s/.test(ch) ? 0 : (i++) * speed + Math.random() * spread);
    return { n, final, at };
  });
  const t0 = performance.now();
  const end = i * speed + spread;
  const frame = t => {
    const e = t - t0;
    for (const it of items) {
      let s = '';
      const chars = [...it.final];
      for (let k = 0; k < chars.length; k++) {
        s += e >= it.at[k] || /\s/.test(chars[k]) ? chars[k] : GLYPHS[(Math.random() * GLYPHS.length) | 0];
      }
      it.n.nodeValue = s;
    }
    if (e < end) requestAnimationFrame(frame);
    else { items.forEach(it => { it.n.nodeValue = it.final; }); el.style.minHeight = ''; }
  };
  requestAnimationFrame(frame);
}

// ---- Masthead -------------------------------------------------------------

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
  if (next) $('#mast-next').innerHTML = `<span class="dim">${esc(next.label)} fires in</span> ${cd(next.at - now)}`;
  $$('[data-countdown]').forEach(el => {
    const r = DATA.routines.find(x => x.key === el.dataset.countdown);
    const at = r && nextFire(r.rule, now);
    if (at) el.textContent = cd(at - now);
  });
}

function paintTicker() {
  const pool = DATA.activity.filter(a => a.role !== 'merge' && a.role !== 'infra' && a.role !== 'other');
  const rows = [...pool.filter(a => a.role !== 'orchestrator').slice(0, 12), ...pool.filter(a => a.role === 'orchestrator').slice(0, 4)]
    .sort((a, b) => b.date.localeCompare(a.date));
  if (!rows.length) { $('.ticker').hidden = true; return; }
  const item = a => `<span class="tk" data-role="${esc(a.role || 'other')}"><i></i><b>${esc(a.role || 'commit')}</b> ${esc(rel(a.date))} <span>${esc(a.subject)}</span></span>`;
  const run = rows.map(item).join('');
  const track = $('#ticker');
  track.innerHTML = `<div class="tk-run">${run}</div><div class="tk-run" aria-hidden="true">${run}</div>`;
  requestAnimationFrame(() => {
    const w = $('.tk-run', track).scrollWidth;
    track.style.setProperty('--tk-dur', `${Math.round(w / 42)}s`);
  });
}

// ---- Hero -----------------------------------------------------------------

function paintHero() {
  const live = LIVE.length, held = count('held'), passed = count('pass') + count('solved');
  const day = DATA.history?.since ? Math.floor(ageDays(DATA.history.since)) + 1 : null;
  const built = new Date(DATA.generatedAt).toISOString();
  $('#kicker').innerHTML = [
    day ? `Day ${day}` : null,
    `${dm(built)} ${built.slice(11, 16)}Z`,
    `<a href="${REPO}/commit/${DATA.repo.headSha}" target="_blank" rel="noopener">${esc(sha7(DATA.repo.headSha))}</a>`,
  ].filter(Boolean).join('<span class="sep">·</span>');

  const lead = passed === 0
    ? `${Words(live)} problems.${day ? ` ${Words(day)} days.` : ''} Nothing cracked.`
    : `${Words(live)} problems. ${Words(passed)} cracked.`;
  $('#bluf').innerHTML = `<span class="l1">${esc(lead)}</span>` + (held
    ? `<span class="l2"><em>${Words(held)} ${held === 1 ? 'claim sits' : 'claims sit'} one signature out.</em></span>`
    : '');

  const su = DATA.statusUpdated;
  if (su) $('#bluf-sub').innerHTML = `The latest pass, ${esc(dm(su.date))}: ${esc(su.label)}${su.detail ? ` — ${md(su.detail)}` : ''}.${su.report ? ` <a href="${blob(su.report)}" target="_blank" rel="noopener">Read it</a>.` : ''}`;

  const k = [
    { n: live, l: 'live problems' },
    { n: held, l: 'held at 3×PARTIAL', c: 'held' },
    { n: count('panel'), l: 'awaiting a panel', c: 'panel' },
    { n: passed, l: 'passed', c: passed ? 'pass' : 'zero' },
    { n: DATA.totals.research7d ?? '—', l: 'research commits, 7 days' },
    { n: DATA.activeClaims?.length ?? 0, l: 'sessions holding a claim' },
  ];
  $('#kpis').innerHTML = k.map(x => `<div class="kpi" ${x.c ? `data-c="${x.c}"` : ''}><span class="kpi-n mono">${esc(x.n)}</span><span class="kpi-l">${esc(x.l)}</span></div>`).join('');

  $('#scope-cap').innerHTML = `Distance from centre is distance from cracked. The centre is <b>PASS</b>. The sweep brightens each problem by how recently a session touched it.`;
  requestAnimationFrame(() => scramble($('#bluf'), { speed: 14, spread: 320 }));
}

// ---- The scope ------------------------------------------------------------

const el = (tag, attrs = {}, parent) => {
  const n = document.createElementNS(SVGNS, tag);
  for (const [k, v] of Object.entries(attrs)) n.setAttribute(k, v);
  if (parent) parent.appendChild(n);
  return n;
};
const polar = (deg, r) => { const a = deg * Math.PI / 180; return [r * Math.sin(a), -r * Math.cos(a)]; };
const arc = (a1, a2, r, sweep = 1) => { const [x1, y1] = polar(a1, r), [x2, y2] = polar(a2, r); return `M${x1} ${y1}A${r} ${r} 0 0 ${sweep} ${x2} ${y2}`; };

function layout(R) {
  const groups = {};
  for (const p of LIVE) {
    const st = stageOf(p);
    const ring = st === 'blocked' ? 'working' : st;
    const key = `${sectorOf(p)}|${ring}`;
    (groups[key] ||= []).push(p);
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
      const r = (STAGES[ring].r + stagger) * R;
      const [x, y] = polar(deg, r);
      pts.push({ p, deg, x, y });
    });
  }
  return pts;
}

const scopes = [];
function buildScope(host, { mini = false } = {}) {
  const R = 400;
  const svg = el('svg', { viewBox: '-500 -500 1000 1000', role: 'img', 'aria-label': `Scope of ${LIVE.length} problems by closeness to cracked` });
  const defs = el('defs', {}, svg);
  const face = el('g', { class: 'face' }, svg);
  el('circle', { r: R, class: 'disc' }, face);

  // Rings, with a label and live count on the 12 o'clock axis.
  for (const [k, s] of Object.entries(STAGES)) {
    if (!s.ring) continue;
    el('circle', { r: s.r * R, class: `ring ring-${k}` }, face);
    if (!mini) {
      const n = k === 'working' ? count('working') + count('blocked') : count(k);
      const t = el('text', { x: 8, y: -s.r * R - 6, class: 'ring-label' }, face);
      t.textContent = `${s.ring.toUpperCase()}  ${n}`;
    }
  }
  // Sector boundaries and the bearing scale.
  for (let a = 0; a < 360; a += 90) {
    const [x1, y1] = polar(a, 0.1 * R), [x2, y2] = polar(a, R);
    el('line', { x1, y1, x2, y2, class: 'axis' }, face);
  }
  if (!mini) for (let a = 0; a < 360; a += 2) {
    const long = a % 30 === 0, mid = a % 10 === 0;
    const [x1, y1] = polar(a, R), [x2, y2] = polar(a, R + (long ? 12 : mid ? 7 : 4));
    el('line', { x1, y1, x2, y2, class: long ? 'tick long' : 'tick' }, face);
  }
  // Sector names on arcs, flipped on the lower half so they read upright.
  SECTORS.forEach((s, i) => {
    const lower = i === 1 || i === 2;
    const id = `arc-${mini ? 'm' : 'h'}-${i}`;
    const a1 = i * 90 + 6, a2 = i * 90 + 84;
    el('path', { id, d: lower ? arc(a2, a1, R + (mini ? 44 : 40), 0) : arc(a1, a2, R + (mini ? 22 : 26), 1), fill: 'none' }, defs);
    const t = el('text', { class: 'sector-label' }, face);
    const tp = el('textPath', { href: `#${id}`, startOffset: '50%', 'text-anchor': 'middle' }, t);
    const n = LIVE.filter(p => sectorOf(p) === s.key).length;
    tp.textContent = mini ? s.label.toUpperCase() : `${s.label.toUpperCase()}  ·  ${n}`;
  });

  // The bullseye.
  const passed = count('pass') + count('solved');
  el('circle', { r: 0.1 * R, class: 'bull' + (passed ? ' lit' : '') }, face);
  const bt = el('text', { y: mini ? 10 : -2, class: 'bull-label' }, face);
  bt.textContent = 'PASS';
  if (!mini) { const bn = el('text', { y: 26, class: 'bull-n' }, face); bn.textContent = String(passed); }

  // Sweep: a leading line and a fading wake built from thin wedges.
  const sweep = el('g', { class: 'sweep' }, svg);
  const slices = 14;
  for (let i = 0; i < slices; i++) {
    const a1 = -(i + 1) * 4, a2 = -i * 4;
    const [x1, y1] = polar(a1, R), [x2, y2] = polar(a2, R);
    el('path', { d: `M0 0L${x1} ${y1}A${R} ${R} 0 0 1 ${x2} ${y2}Z`, class: 'wake', style: `opacity:${(0.2 * (1 - i / slices) ** 1.6).toFixed(3)}` }, sweep);
  }
  el('line', { x1: 0, y1: 0, x2: 0, y2: -R, class: 'beam' }, sweep);
  if (REDUCED) sweep.style.display = 'none';

  // Blips.
  const blips = el('g', { class: 'blips' }, svg);
  const pts = layout(R);
  const nodes = pts.map(({ p, deg, x, y }) => {
    const st = stageOf(p);
    const size = (mini ? 7 : 6) + Math.min(9, Math.sqrt(p.commits30d || 0) * 2.1);
    const g = el('g', { class: `blip s-${st}`, transform: `translate(${x.toFixed(1)} ${y.toFixed(1)})`, 'data-slug': p.slug, tabindex: mini ? -1 : 0, role: 'button', 'aria-label': `${nameOf(p)}, ${STAGES[st].label}` }, blips);
    el('circle', { r: size * 1.9, class: 'halo' }, g);
    el('circle', { r: size, class: 'core' }, g);
    el('circle', { r: Math.max(size * 2.2, 16), class: 'hit' }, g);
    const recency = Math.max(0, 1 - ageDays(p.lastTouch) / 21);
    return { g, deg, base: 0.28 + 0.5 * recency };
  });

  host.appendChild(svg);
  const scope = { host, svg, sweep, nodes, visible: true };
  nodes.forEach(n => n.g.style.setProperty('--g', REDUCED ? n.base + 0.2 : n.base));
  scopes.push(scope);
  new IntersectionObserver(([e]) => { scope.visible = e.isIntersecting; }).observe(host);
  return scope;
}

// One clock drives every scope so the sweeps stay in phase.
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

// ---- I. Claims ------------------------------------------------------------

function strip(dates, days, w, h, cls = '') {
  const b = new Array(days).fill(0);
  for (const d of dates || []) { const a = Math.floor(ageDays(d)); if (a >= 0 && a < days) b[days - 1 - a]++; }
  const max = Math.max(3, ...b), step = w / days;
  const bars = b.map((v, i) => v ? `<rect x="${(i * step).toFixed(2)}" y="${h - Math.max(3, v / max * (h - 1))}" width="${Math.max(1.2, step - 1).toFixed(2)}" height="${Math.max(3, v / max * (h - 1))}"${i >= days - 7 ? ' class="r"' : ''}/>` : '').join('');
  return `<svg class="strip ${cls}" viewBox="0 0 ${w} ${h}" preserveAspectRatio="none" aria-hidden="true"><line x1="0" x2="${w}" y1="${h - 0.5}" y2="${h - 0.5}"/>${bars}</svg>`;
}
const SPAN = Math.max(14, Math.min(90, (DATA.pulse || []).length || 30));

function paintCases() {
  const held = LIVE.filter(p => stageOf(p) === 'held').sort((a, b) => (a.claim?.since || '9').localeCompare(b.claim?.since || '9'));
  const tilt = [-7, 4, -2, 6, -4];
  $('#cases').innerHTML = held.map((p, i) => {
    const c = p.claim, days = c?.since ? Math.floor(ageDays(c.since)) : null;
    return `
    <article class="case" data-slug="${esc(p.slug)}" tabindex="0" role="button" aria-label="Open case: ${esc(nameOf(p))}">
      <header class="case-top mono"><span>Case ${String(i + 1).padStart(2, '0')}</span><span>${esc(DOMAIN_SHORT[p.domain])}</span></header>
      <h3 class="case-title">${esc(nameOf(p))}</h3>
      <div class="stamps" aria-label="Three validator verdicts, all PARTIAL">
        ${['Validator', 'Validator', 'Refuter'].map((who, j) => `<span class="stamp" style="--t:${tilt[(i + j) % 5]}deg"><b>Partial</b><i>${who}</i></span>`).join('')}
      </div>
      <div class="held-for"><span class="mono">${days ?? '—'}</span><span>days held${c?.since ? ` · panel closed ${esc(dm(c.since))}` : ''}</span></div>
      <p class="label">Standing between this and PASS</p>
      <p class="case-check">${c ? md(c.missingCheck) : '<span class="dim">No validation-queue row names this folder.</span>'}</p>
      <footer class="case-foot">${strip(p.commitDates90d, SPAN, 200, 22)}<span class="mono">${esc(rel(p.lastTouch))}</span></footer>
    </article>`;
  }).join('') || '<p class="empty">No claim is held.</p>';

  const panel = LIVE.filter(p => stageOf(p) === 'panel');
  $('#panel-queue').innerHTML = panel.length ? `
    <h3 class="label">In the anteroom: bounded claims still waiting for their first verdict</h3>
    <ul>${panel.map(p => `<li data-slug="${esc(p.slug)}" tabindex="0" role="button">
      <span class="pq-name">${esc(nameOf(p))}</span><span class="pq-check">${md(p.claim?.missingCheck || '')}</span><span class="mono dim">${esc(rel(p.lastTouch))}</span></li>`).join('')}</ul>` : '';
}

// ---- II. Board ------------------------------------------------------------

const state = { domain: 'all', stage: 'all', q: '' };
const BOARD_ORDER = ['solved', 'pass', 'held', 'panel', 'working', 'unworked', 'blocked', 'backlog', 'withdrawn'];
const byStage = (a, b) => BOARD_ORDER.indexOf(stageOf(a)) - BOARD_ORDER.indexOf(stageOf(b)) || (b.commits30d - a.commits30d) || nameOf(a).localeCompare(nameOf(b));
let VISIBLE = [];

function badge(p) { const s = stageOf(p); return `<span class="badge s-${s}">${esc(STAGES[s].label)}</span>`; }

function paintControls() {
  $('#domain-seg').innerHTML = [{ key: 'all', label: 'All' }, ...DATA.domains.map(d => ({ key: d.key, label: DOMAIN_SHORT[d.key] }))]
    .map(d => `<button type="button" data-domain="${d.key}" aria-pressed="${d.key === 'all'}">${esc(d.label)}</button>`).join('');
  const stages = ['all', ...BOARD_ORDER].filter(k => k === 'all' || count(k));
  $('#stage-filter').innerHTML = stages.map(k => `<button type="button" class="chip${k === 'all' ? '' : ` s-${k}`}" data-stage="${k}" aria-pressed="${k === 'all'}">${k === 'all' ? 'Every stage' : esc(STAGES[k].label)}<span class="mono">${k === 'all' ? LIVE.length : count(k)}</span></button>`).join('');
  $('#domain-seg').addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; state.domain = b.dataset.domain; $$('#domain-seg button').forEach(x => x.setAttribute('aria-pressed', x === b)); paintBoard(); });
  $('#stage-filter').addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; state.stage = b.dataset.stage; $$('#stage-filter button').forEach(x => x.setAttribute('aria-pressed', x === b)); paintBoard(); });
  let t; $('#search').addEventListener('input', e => { clearTimeout(t); t = setTimeout(() => { state.q = e.target.value.trim().toLowerCase(); paintBoard(); }, 60); });
}

function matches(p) {
  if (state.domain !== 'all' && p.domain !== state.domain) return false;
  if (state.stage !== 'all' && stageOf(p) !== state.stage) return false;
  if (!state.q) return true;
  const hay = [nameOf(p), p.title, p.slug, p.statusRow?.status, p.statusRow?.notes, p.lede, STAGES[stageOf(p)].label].join(' ').toLowerCase();
  return state.q.split(/\s+/).every(w => hay.includes(w));
}

function paintBoard() {
  const list = LIVE.filter(matches);
  VISIBLE = [];
  let html = '';
  for (const d of DATA.domains) {
    const rows = list.filter(p => p.domain === d.key).sort(byStage);
    if (!rows.length) continue;
    VISIBLE.push(...rows);
    html += `<div class="bgroup"><h3 class="bgroup-h"><span>${esc(d.label)}</span><span class="mono">${rows.length}</span></h3>${rows.map(p => `
      <div class="brow s-${stageOf(p)}" data-slug="${esc(p.slug)}" tabindex="0" role="button">
        <div class="c-stage">${badge(p)}</div>
        <div class="c-name"><span class="name">${esc(nameOf(p))}</span><span class="slug mono">${esc(p.id)}</span></div>
        <div class="c-status">${p.statusRow?.status ? md(p.statusRow.status) : `<span class="dim">${p.domain === 'discovered' ? 'Proposal, not yet promoted' : 'No STATUS.md row'}</span>`}</div>
        <div class="c-strip">${strip(p.commitDates90d, SPAN, 150, 20)}</div>
        <div class="c-when mono">${esc(rel(p.lastTouch))}</div>
      </div>`).join('')}</div>`;
  }
  $('#board-table').innerHTML = html || `<p class="empty">Nothing matches that filter.</p>`;
  const keep = new Set(list.map(p => p.slug));
  $$('#scope-mini .blip').forEach(b => b.classList.toggle('dim', !keep.has(b.dataset.slug)));
  $('#mini-cap').textContent = `${list.length} of ${LIVE.length} shown · the scope dims what the filter hides`;
}

function linkHover() {
  const hot = slug => $$('.blip').forEach(b => b.classList.toggle('hot', b.dataset.slug === slug));
  $('#board-table').addEventListener('pointerover', e => { const r = e.target.closest('.brow'); if (r) hot(r.dataset.slug); });
  $('#board-table').addEventListener('pointerleave', () => hot(null));
  $('#board-table').addEventListener('focusin', e => { const r = e.target.closest('.brow'); if (r) hot(r.dataset.slug); });
}

// ---- III. Tempo -----------------------------------------------------------

function paintLanes() {
  const days = DATA.pulse || [];
  const host = $('#lanes');
  if (!days.length) { host.innerHTML = '<p class="empty">No git history in this build.</p>'; return; }
  const draw = () => {
    const W = Math.max(320, host.clientWidth), padL = 104, laneH = 46, top = 22;
    const H = top + laneH * ROLES.length + 6;
    const step = (W - padL) / days.length;
    let s = `<svg viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" role="img" aria-label="Commits per day by role">`;
    days.forEach((d, i) => {
      const x = padL + (i + 0.5) * step;
      const wd = new Date(d.date + 'T00:00:00Z').getUTCDay();
      if (wd === 1 || i === 0 || i === days.length - 1) s += `<text x="${x}" y="12" class="lane-date" text-anchor="middle">${i === days.length - 1 ? 'today' : dm(d.date)}</text>`;
      if (wd === 1) s += `<line x1="${x - step / 2}" x2="${x - step / 2}" y1="${top - 4}" y2="${H}" class="week"/>`;
    });
    ROLES.forEach((r, j) => {
      const y = top + laneH * j + laneH / 2;
      s += `<line x1="${padL}" x2="${W}" y1="${y}" y2="${y}" class="lane-line"/>`;
      s += `<text x="0" y="${y + 4}" class="lane-name" data-role="${r.key}">${r.label}</text>`;
      days.forEach((d, i) => {
        const v = d[r.key] || 0;
        const x = padL + (i + 0.5) * step;
        s += v
          ? `<circle cx="${x}" cy="${y}" r="${Math.min(laneH / 2 - 3, 2.5 + Math.sqrt(v) * 3)}" class="dot" data-role="${r.key}" data-i="${i}" data-r="${r.key}"/>`
          : `<circle cx="${x}" cy="${y}" r="1.2" class="nil"/>`;
      });
    });
    host.innerHTML = s + '</svg>';
  };
  draw();
  let rt; addEventListener('resize', () => { clearTimeout(rt); rt = setTimeout(draw, 120); });
  host.addEventListener('pointerover', e => {
    const c = e.target.closest('.dot'); if (!c) return;
    const d = days[+c.dataset.i], role = ROLES.find(r => r.key === c.dataset.r);
    tip(`<b>${esc(role.label)}</b> · ${esc(dm(d.date))}<br>${d[role.key]} commit${d[role.key] === 1 ? '' : 's'}`, c.getBoundingClientRect());
  });
  host.addEventListener('pointerout', e => { if (e.target.closest('.dot')) untip(); });

  const tot = Object.fromEntries(ROLES.map(r => [r.key, days.reduce((a, d) => a + (d[r.key] || 0), 0)]));
  const quiet = days.filter(d => ROLES.every(r => !d[r.key])).length;
  $('#lanes-cap').textContent = `${ROLES.map(r => `${r.label} ${tot[r.key]}`).join(' · ')} commits over ${days.length} days. ${quiet ? `${Words(quiet)} day${quiet === 1 ? '' : 's'} with no research commit at all.` : 'No silent days.'}`;
}

function paintRoutines() {
  const last = DATA.lastByRole || {};
  $('#routines').innerHTML = (DATA.routines || []).map(r => `
    <li data-role="${r.key}">
      <div class="rt-top"><span class="rt-name"><i></i>${esc(r.label)}</span><span class="rt-cd mono" data-countdown="${r.key}"></span></div>
      <div class="rt-cad mono">${esc(r.cadence)}</div>
      <p class="rt-last">${last[r.key] ? `Last: <a href="${REPO}/commit/${last[r.key].sha}" target="_blank" rel="noopener">${esc(last[r.key].subject)}</a> <span class="dim">${esc(rel(last[r.key].date))}</span>` : '<span class="dim">Nothing in the window.</span>'}</p>
    </li>`).join('');
}

// ---- IV. Wire -------------------------------------------------------------

function chips(slugs) {
  return (slugs || []).filter(s => BY[s]).map(s => `<button type="button" class="pchip" data-slug="${esc(s)}">${esc(nameOf(BY[s]).replace(/\s*\(.*?\)\s*$/, ''))}</button>`).join('');
}

function paintWire() {
  const ds = DATA.dispatches || [];
  const dateline = d => `<p class="dateline mono"><span data-role="${esc(d.role)}"><i></i>${esc(d.role === 'other' ? 'board' : d.role)}</span> · ${esc(dm(d.date))}</p>`;
  const story = (d, cls) => `
    <article class="story ${cls}">
      ${dateline(d)}
      <h3><a href="${blob(d.file)}" target="_blank" rel="noopener">${esc(d.title)}</a></h3>
      ${d.lede ? `<p class="lede">${esc(d.lede.replace(/[.,;:]…$/, '…'))}</p>` : ''}
      ${d.problems?.length ? `<div class="pchips">${chips(d.problems)}</div>` : ''}
    </article>`;
  if (!ds.length) { $('#broadsheet').innerHTML = '<p class="empty">No dispatches.</p>'; return; }
  $('#broadsheet').innerHTML = `
    <div class="bs-top">${story(ds[0], 'lead')}<div class="bs-rail">${ds.slice(1, 4).map(d => story(d, 'rail')).join('')}</div></div>
    <div class="bs-cols">${ds.slice(4, 13).map(d => story(d, 'col')).join('')}</div>`;

  $('#log').innerHTML = DATA.activity.slice(0, 28).map(a => `
    <li data-role="${esc(a.role || 'other')}"><span class="dim">${esc(rel(a.date))}</span><i></i><span class="subj" title="${esc(a.subject)}">${esc(a.subject)}</span><a href="${REPO}/commit/${a.sha}" target="_blank" rel="noopener">${esc(sha7(a.sha))}</a></li>`).join('');

  const prs = [...DATA.prs].sort((a, b) => ({ open: 0, merged: 1 }[a.state] ?? 2) - ({ open: 0, merged: 1 }[b.state] ?? 2) || new Date(b.updated) - new Date(a.updated)).slice(0, 8);
  $('#prs').innerHTML = prs.length
    ? `<ol class="prs">${prs.map(p => `<li><a href="${p.url}" target="_blank" rel="noopener"><span class="pr-st mono" data-st="${p.state}">${p.draft ? 'draft' : p.state}</span><span>${esc(p.title)}</span><span class="mono dim">#${p.number}</span></a></li>`).join('')}</ol>`
    : `<p class="fine">Nothing in the queue${DATA.prs.length ? '' : ', or this build had no GitHub token'}.</p>`;
}

// ---- Dossier --------------------------------------------------------------

const SIGNALS = [['PROBLEM.md', 'hasProblem'], ['PROGRESS.md', 'hasProgress'], ['HANDOVER.md', 'hasHandover'], ['SOURCES.md', 'hasSources'],
  ['FREEZE.md', 'hasFreeze'], ['RESULTS.md', 'hasResults'], ['SOLUTION.md', 'hasSolution'], ['CLAIM.md', 'hasClaim'],
  ['analysis/', 'hasAnalysis'], ['code/', 'hasCode'], ['data/', 'hasData'], ['attempts/', 'hasAttempts']];
let lastFocus = null, current = null;

function openDossier(slug) {
  const p = BY[slug]; if (!p) return;
  if (!current) lastFocus = document.activeElement;
  current = slug;
  const d = $('#dossier');
  const order = VISIBLE.length ? VISIBLE : [...LIVE].sort(byStage);
  const i = order.findIndex(x => x.slug === slug);
  const prev = order[(i - 1 + order.length) % order.length], next = order[(i + 1) % order.length];
  const files = SIGNALS.filter(([, k]) => p.files[k]);
  const related = (DATA.dispatches || []).filter(x => x.problems?.includes(slug)).slice(0, 4);
  d.innerHTML = `
    <div class="ds-bar">
      <span class="mono dim">${esc(DOMAIN_SHORT[p.domain])} · file ${i + 1} of ${order.length}</span>
      <span class="ds-nav">
        <button type="button" data-go="${esc(prev?.slug || '')}" aria-label="Previous problem">←</button>
        <button type="button" data-go="${esc(next?.slug || '')}" aria-label="Next problem">→</button>
        <button type="button" class="ds-close" aria-label="Close">esc</button>
      </span>
    </div>
    <div class="ds-body">
      ${badge(p)}
      <h2 id="dossier-title">${esc(p.title)}</h2>
      <p class="ds-slug mono"><a href="${tree(p.slug)}" target="_blank" rel="noopener">${esc(p.slug)}/ ↗</a></p>
      ${p.statusRow?.status ? `<p class="ds-status">${md(p.statusRow.status)}</p>` : ''}
      ${p.claim ? `<section class="ds-claim"><p class="label">Validation queue · ${esc(p.claim.claim)}</p><p>${md(p.claim.disposition)}</p>
        <p class="label">Decisive missing check</p><p class="ds-check">${md(p.claim.missingCheck)}</p></section>` : ''}
      ${p.statusRow?.notes ? `<section><p class="label">From STATUS.md</p><p class="ds-notes">${md(p.statusRow.notes)}</p></section>`
        : `<section><p class="label">From PROBLEM.md</p><p class="ds-notes">${esc(p.lede || 'No lede recorded.')}</p></section>`}
      <section><p class="label">Every day a session touched it · ${SPAN} days</p>${strip(p.commitDates90d, SPAN, 480, 40, 'big')}
        <p class="ds-stats mono"><span><b>${p.commits30d}</b> commits · 30d</span><span><b>${p.commits90d}</b> · 90d</span><span>touched <b>${esc(rel(p.lastTouch))}</b></span></p>
        ${p.lastSubject ? `<p class="ds-last mono">“${esc(p.lastSubject)}”</p>` : ''}</section>
      <section><p class="label">In the folder</p><div class="ds-files mono">${files.map(([n]) => `<a href="${n.endsWith('/') ? tree(p.slug + '/' + n.slice(0, -1)) : blob(p.slug + '/' + n)}" target="_blank" rel="noopener">${esc(n)}</a>`).join('')}</div></section>
      ${related.length ? `<section><p class="label">In dispatches</p><ul class="ds-rel">${related.map(x => `<li><span class="mono dim">${esc(dm(x.date))}</span><a href="${blob(x.file)}" target="_blank" rel="noopener">${esc(x.title)}</a></li>`).join('')}</ul></section>` : ''}
    </div>`;
  const opening = d.hidden;
  d.hidden = false; $('#scrim').hidden = false;
  document.body.classList.add('locked');
  requestAnimationFrame(() => d.classList.add('open'));
  $$('[data-go]', d).forEach(b => b.addEventListener('click', () => b.dataset.go && openDossier(b.dataset.go)));
  $('.ds-close', d).addEventListener('click', closeDossier);
  if (opening) $('.ds-close', d).focus();
  scramble($('#dossier-title'), { speed: 8, spread: 160 });
  history.replaceState(null, '', `#p/${slug}`);
  $$('.blip').forEach(b => b.classList.toggle('sel', b.dataset.slug === slug));
}

function closeDossier() {
  const d = $('#dossier'); if (d.hidden) return;
  d.classList.remove('open'); $('#scrim').hidden = true; document.body.classList.remove('locked');
  setTimeout(() => { d.hidden = true; }, 200);
  history.replaceState(null, '', location.pathname);
  $$('.blip.sel').forEach(b => b.classList.remove('sel'));
  current = null;
  lastFocus?.focus?.();
}

// ---- Palette (⌘K) ---------------------------------------------------------

let palIdx = 0, palList = [];
function openPalette() {
  $('#palette').hidden = false; $('#scrim').hidden = false;
  const inp = $('#palette-input'); inp.value = ''; renderPalette(''); inp.focus();
}
function closePalette() { $('#palette').hidden = true; if ($('#dossier').hidden) $('#scrim').hidden = true; }
function renderPalette(q) {
  const t = q.toLowerCase().split(/\s+/).filter(Boolean);
  palList = [...LIVE].filter(p => { const h = `${nameOf(p)} ${p.slug} ${STAGES[stageOf(p)].label}`.toLowerCase(); return t.every(w => h.includes(w)); }).sort(byStage).slice(0, 9);
  palIdx = 0;
  paintPal();
}
function paintPal() {
  $('#palette-list').innerHTML = palList.map((p, i) => `<li role="option" aria-selected="${i === palIdx}" data-pi="${i}">${badge(p)}<span class="pl-name">${esc(nameOf(p))}</span><span class="mono dim">${esc(DOMAIN_SHORT[p.domain])}</span></li>`).join('') || '<li class="dim">No match.</li>';
}

// ---- Tooltip --------------------------------------------------------------

function tip(html, rect) {
  const t = $('#tip'); t.innerHTML = html; t.hidden = false;
  const r = t.getBoundingClientRect();
  const x = Math.min(innerWidth - r.width - 8, Math.max(8, rect.left + rect.width / 2 - r.width / 2));
  const y = rect.top - r.height - 10 < 60 ? rect.bottom + 10 : rect.top - r.height - 10;
  t.style.transform = `translate(${Math.round(x)}px,${Math.round(y)}px)`;
}
const untip = () => { $('#tip').hidden = true; };

// ---- Wiring ---------------------------------------------------------------

function wire() {
  document.addEventListener('click', e => {
    if (e.target.closest('a')) return;
    const pi = e.target.closest('[data-pi]');
    if (pi) { closePalette(); openDossier(palList[+pi.dataset.pi].slug); return; }
    const t = e.target.closest('[data-slug]');
    if (t && !t.closest('.dossier')) openDossier(t.dataset.slug);
  });
  document.addEventListener('keydown', e => {
    const palOpen = !$('#palette').hidden;
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); palOpen ? closePalette() : openPalette(); return; }
    if (palOpen) {
      if (e.key === 'Escape') { closePalette(); return; }
      if (e.key === 'ArrowDown' || e.key === 'ArrowUp') { e.preventDefault(); palIdx = (palIdx + (e.key === 'ArrowDown' ? 1 : -1) + palList.length) % Math.max(1, palList.length); paintPal(); return; }
      if (e.key === 'Enter' && palList[palIdx]) { const s = palList[palIdx].slug; closePalette(); openDossier(s); }
      return;
    }
    if (e.key === 'Escape') { closeDossier(); return; }
    if (current && (e.key === 'ArrowRight' || e.key === 'ArrowLeft')) { $(`[data-go]:nth-child(${e.key === 'ArrowLeft' ? 1 : 2})`, $('#dossier'))?.click(); return; }
    if ((e.key === 'Enter' || e.key === ' ') && e.target.matches('[data-slug][tabindex], .blip')) { e.preventDefault(); openDossier(e.target.dataset.slug || e.target.closest('[data-slug]').dataset.slug); return; }
    if (e.key === '/' && !e.target.matches('input, textarea')) { e.preventDefault(); openPalette(); }
  });
  $('#palette-input').addEventListener('input', e => renderPalette(e.target.value));
  $('#jump-open').addEventListener('click', openPalette);
  $('#scrim').addEventListener('click', () => { closePalette(); closeDossier(); });

  document.addEventListener('pointerover', e => {
    const b = e.target.closest('.blip'); if (!b) return;
    const p = BY[b.dataset.slug];
    tip(`<b>${esc(nameOf(p))}</b><br><span class="tip-st s-${stageOf(p)}">${esc(STAGES[stageOf(p)].label)}</span> · ${esc(rel(p.lastTouch))}`, b.querySelector('.core').getBoundingClientRect());
  });
  document.addEventListener('pointerout', e => { if (e.target.closest('.blip')) untip(); });

  $$('[data-scramble]').forEach(h => new IntersectionObserver(([x], o) => { if (x.isIntersecting) { scramble(h); o.disconnect(); } }, { threshold: 0.6 }).observe(h));

  const m = location.hash.match(/^#p\/(.+)$/);
  if (m) openDossier(decodeURIComponent(m[1]));
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
buildScope($('#scope'));
paintCases();
paintControls();
buildScope($('#scope-mini'), { mini: true });
paintBoard();
linkHover();
paintLanes();
paintRoutines();
paintWire();
paintFoot();
wire();
tick();
setInterval(tick, 1000);
if (!REDUCED) requestAnimationFrame(spin);
