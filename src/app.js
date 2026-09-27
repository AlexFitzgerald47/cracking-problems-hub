// Cracking Problems Hub — situation room.
// Data is inlined at build time in <script id="hub-data">; see scripts/build.mjs
// and scripts/derive.mjs for every field used here.

const DATA = JSON.parse(document.getElementById('hub-data').textContent);
const DAY = 86400000;
const NOW = Date.now();

const $ = (sel, root = document) => root.querySelector(sel);
const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

// Escape first, then a small, safe subset of the markdown STATUS.md uses.
const md = s => esc(s)
  .replace(/`([^`]+)`/g, '<code>$1</code>')
  .replace(/\*\*(.+?)\*\*/g, '<b>$1</b>')
  .replace(/~~(.+?)~~/g, '<s>$1</s>')
  .replace(/(^|[\s(])\*([^*\s][^*]*?)\*(?=[\s).,;:]|$)/g, '$1<em>$2</em>');

const WORDS = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten',
  'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen'];
const TENS = ['', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety'];
const words = n => n < 20 ? WORDS[n] : n < 100 ? TENS[Math.floor(n / 10)] + (n % 10 ? '-' + WORDS[n % 10] : '') : String(n);
const Words = n => { const w = words(n); return w[0].toUpperCase() + w.slice(1); };

const daysSince = iso => iso ? Math.floor((NOW - new Date(iso).getTime()) / DAY) : null;
const rel = iso => {
  if (!iso) return '—';
  const mins = Math.floor((NOW - new Date(iso).getTime()) / 60000);
  if (mins < 60) return `${Math.max(1, mins)}m ago`;
  if (mins < 1440) return `${Math.floor(mins / 60)}h ago`;
  const d = Math.floor(mins / 1440);
  return d < 60 ? `${d}d ago` : new Date(iso).toISOString().slice(0, 10);
};
const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
const dm = iso => { const d = new Date(iso); return `${d.getUTCDate()} ${MONTHS[d.getUTCMonth()]}`; };
const shortSha = s => (s || '').slice(0, 7);
const repoUrl = DATA.repo.url;
const blob = p => `${repoUrl}/blob/main/${p}`;
const tree = p => `${repoUrl}/tree/main/${p}`;

// ---- Vocabulary -----------------------------------------------------------

const STAGES = [
  { key: 'backlog', label: 'Backlog', hint: 'Proposed in discovered/' },
  { key: 'unworked', label: 'Unworked', hint: 'Promoted, no session yet' },
  { key: 'working', label: 'In work', hint: 'Sessions landing' },
  { key: 'blocked', label: 'Blocked', hint: 'Evidence or archive' },
  { key: 'panel', label: 'Panel pending', hint: 'Bounded claim, no verdicts' },
  { key: 'held', label: 'Held', hint: '3 × PARTIAL, awaiting sign-off' },
  { key: 'pass', label: 'PASS', hint: 'Validated by panel' },
  { key: 'solved', label: 'Solved', hint: 'Signed off' },
];
const STAGE = Object.fromEntries(STAGES.map((s, i) => [s.key, { ...s, rank: i }]));
STAGE.withdrawn = { key: 'withdrawn', label: 'Withdrawn', hint: 'Solved elsewhere or retired', rank: -1 };

const DOMAIN_SHORT = {
  'ciphers': 'Ciphers', 'historical-texts': 'Texts', 'historical-controversies': 'Controversies',
  'ireland': 'Ireland', 'discovered': 'Backlog',
};
const ROLES = [
  { key: 'cracker', label: 'Cracker' },
  { key: 'validator', label: 'Validator' },
  { key: 'orchestrator', label: 'Orchestrator' },
  { key: 'finder', label: 'Finder' },
  { key: 'other', label: 'Other' },
];

const LIVE = DATA.problems.filter(p => !p.isStub);
const BY_SLUG = Object.fromEntries(DATA.problems.map(p => [p.slug, p]));
const stageOf = p => STAGE[p.stage] ? p.stage : 'working';
const nameOf = p => p.shortTitle || p.title;
const count = k => LIVE.filter(p => stageOf(p) === k).length;

// ---- Masthead -------------------------------------------------------------

function nextFire(rule, from) {
  const base = new Date(from);
  for (let d = 0; d < 8; d++) {
    const y = base.getUTCFullYear(), m = base.getUTCMonth(), dd = base.getUTCDate() + d;
    const wd = new Date(Date.UTC(y, m, dd)).getUTCDay();
    if (rule.weekdays && !rule.weekdays.includes(wd)) continue;
    for (const h of rule.hours) {
      const t = Date.UTC(y, m, dd, h, rule.minute);
      if (t > from) return t;
    }
  }
  return null;
}
const countdown = ms => {
  const s = Math.max(0, Math.floor(ms / 1000));
  const h = Math.floor(s / 3600), m = Math.floor((s % 3600) / 60);
  return h >= 24 ? `${Math.floor(h / 24)}d ${h % 24}h` : `${h}h ${String(m).padStart(2, '0')}m`;
};
const soonest = () => (DATA.routines || [])
  .map(r => ({ ...r, at: nextFire(r.rule, Date.now()) }))
  .filter(r => r.at).sort((a, b) => a.at - b.at);

function tick() {
  const d = new Date();
  $('#clock').textContent = d.toISOString().slice(11, 19) + ' UTC';
  const next = soonest()[0];
  $('#mast-next').innerHTML = next
    ? `<span class="label-inline">Next</span> ${esc(next.label)} <b>T−${countdown(next.at - Date.now())}</b>` : '';
  $$('[data-countdown]').forEach(el => {
    const r = DATA.routines.find(x => x.key === el.dataset.countdown);
    const at = r && nextFire(r.rule, Date.now());
    if (at) el.textContent = `T−${countdown(at - Date.now())}`;
  });
}

function paintMast() {
  const head = $('#mast-head');
  head.href = `${repoUrl}/commit/${DATA.repo.headSha}`;
  head.innerHTML = `<span class="label-inline">Head</span> ${esc(shortSha(DATA.repo.headSha))}`;
  tick();
  setInterval(tick, 1000);
}

// ---- Situation report -----------------------------------------------------

function paintSitrep() {
  const t = DATA.totals;
  const live = t.live ?? LIVE.length;
  const held = count('held');
  const passed = count('pass') + count('solved');
  const day = DATA.history?.since ? daysSince(DATA.history.since) + 1 : null;
  const built = new Date(DATA.generatedAt);

  $('#sitrep-kicker').innerHTML = [
    'Situation report',
    day ? `Day ${day}` : null,
    `Built ${dm(built.toISOString())} ${built.toISOString().slice(11, 16)} UTC`,
  ].filter(Boolean).map(esc).join('<span class="sep">/</span>');

  const lead = passed === 0
    ? `${Words(live)} problems.${day ? ` ${Words(day)} days.` : ''} No PASS.`
    : `${Words(live)} problems. ${Words(passed)} passed.`;
  const second = held
    ? `<span class="bluf-2"><em>${Words(held)} ${held === 1 ? 'claim is' : 'claims are'} held at 3&thinsp;×&thinsp;PARTIAL</em>, waiting on a human.</span>`
    : `<span class="bluf-2"><em>No claim is waiting on a human.</em></span>`;
  $('#bluf').innerHTML = `<span>${esc(lead)}</span> ${second}`;

  const su = DATA.statusUpdated;
  $('#bluf-sub').innerHTML = su
    ? `<span class="label-inline">Latest pass · ${esc(dm(su.date + 'T00:00:00Z'))}</span> ${esc(su.label)}${su.detail ? ` — ${md(su.detail)}` : ''}.${su.report ? ` <a href="${blob(su.report)}" target="_blank" rel="noopener">Read the report</a>` : ''}`
    : '';

  const kpis = [
    { n: live, label: 'Live problems', href: '#board' },
    { n: held, label: 'Held · 3×PARTIAL', href: '#claims', stage: 'held' },
    { n: count('panel'), label: 'Panels pending', href: '#claims', stage: 'panel' },
    { n: passed, label: 'PASS / solved', href: '#pipeline', stage: 'pass', zero: passed === 0 },
    { n: t.research7d ?? '—', label: 'Research commits · 7d', href: '#tempo' },
    { n: DATA.activeClaims?.length ?? 0, label: 'Claims open now', href: '#dispatches' },
  ];
  $('#kpis').innerHTML = kpis.map(k => `
    <a class="kpi${k.zero ? ' is-zero' : ''}" href="${k.href}"${k.stage ? ` data-stage="${k.stage}"` : ''}>
      <span class="kpi-l">${esc(k.label)}</span><span class="kpi-n mono">${esc(k.n)}</span>
    </a>`).join('');
}

// ---- Strips ---------------------------------------------------------------

// One tick per day; height by commits that day. Neutral ink: colour is for state.
// Default window is the repo's lifetime (pulse length): a 90-day strip on a
// 24-day-old board is two-thirds empty by construction.
const SPAN = Math.max(14, Math.min(90, (DATA.pulse || []).length || 90));
function strip(dates, days = SPAN, w = 180, h = 20) {
  const buckets = new Array(days).fill(0);
  for (const d of dates || []) {
    const age = Math.floor((NOW - new Date(d).getTime()) / DAY);
    if (age >= 0 && age < days) buckets[days - 1 - age]++;
  }
  const max = Math.max(3, ...buckets);
  const step = w / days;
  const bars = buckets.map((v, i) => {
    if (!v) return '';
    const bh = Math.max(3, Math.round((v / max) * (h - 2)));
    return `<rect x="${(i * step).toFixed(2)}" y="${h - bh}" width="${Math.max(1, step - 0.6).toFixed(2)}" height="${bh}" rx="0.5"${i >= days - 7 ? ' class="recent"' : ''}/>`;
  }).join('');
  const total = buckets.reduce((a, b) => a + b, 0);
  return `<svg class="strip" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}" role="img" aria-label="${total} commits in ${days} days"><line x1="0" y1="${h - 0.5}" x2="${w}" y2="${h - 0.5}" class="base"/>${bars}</svg>`;
}

const badge = p => {
  const s = STAGE[stageOf(p)];
  return `<span class="badge" data-stage="${s.key}">${esc(s.label)}</span>`;
};

// ---- 01 Claims ------------------------------------------------------------

function paintClaims() {
  const held = LIVE.filter(p => stageOf(p) === 'held')
    .sort((a, b) => (a.claim?.since || '9').localeCompare(b.claim?.since || '9'));
  $('#held-grid').innerHTML = held.map(p => {
    const c = p.claim;
    const heldDays = c?.since ? daysSince(c.since + 'T00:00:00Z') : null;
    return `
      <article class="held" data-slug="${esc(p.slug)}" tabindex="0" role="button" aria-label="Open dossier: ${esc(nameOf(p))}">
        <header class="held-top">
          <span class="label">${esc(DOMAIN_SHORT[p.domain] || p.domain)}</span>
          <span class="mono held-days">${heldDays !== null ? `Held ${heldDays}d` : 'Held'}</span>
        </header>
        <h3 class="held-title">${esc(nameOf(p))}</h3>
        <div class="verdicts" aria-label="Three validator verdicts, all PARTIAL">
          <span class="v"><i></i>V1</span><span class="v"><i></i>V2</span><span class="v"><i></i>Refuter</span>
          <span class="v-sum mono">3 × PARTIAL</span>
        </div>
        <p class="label">Decisive missing check</p>
        <p class="held-check">${c ? md(c.missingCheck) : '<span class="dim">No validation-queue row names this folder. See its dossier.</span>'}</p>
        <footer class="held-foot">
          ${strip(p.commitDates90d || p.commitDates30d, SPAN, 200, 22)}
          <span class="mono dim">${esc(rel(p.lastTouch))}</span>
        </footer>
      </article>`;
  }).join('') || `<p class="empty">No claim is held.</p>`;

  const panel = LIVE.filter(p => stageOf(p) === 'panel');
  $('#panel-queue').innerHTML = panel.length ? `
    <h3 class="label">Awaiting a panel · no verdicts yet</h3>
    <ul class="pq">${panel.map(p => {
      const since = p.claim?.since;
      return `
      <li data-slug="${esc(p.slug)}" tabindex="0" role="button">
        <span class="pq-name">${esc(nameOf(p))}</span>
        <span class="pq-check">${md(p.claim?.missingCheck || '')}</span>
        <span class="mono dim">${since ? `since ${esc(dm(since + 'T00:00:00Z'))}` : esc(rel(p.lastTouch))}</span>
      </li>`;
    }).join('')}</ul>` : '';
}

// ---- 02 Pipeline ----------------------------------------------------------

function paintLadder() {
  const withdrawn = LIVE.filter(p => stageOf(p) === 'withdrawn');
  $('#ladder').innerHTML = STAGES.map(s => {
    const items = LIVE.filter(p => stageOf(p) === s.key)
      .sort((a, b) => (b.commits30d - a.commits30d) || nameOf(a).localeCompare(nameOf(b)));
    const terminal = s.key === 'pass' || s.key === 'solved';
    return `
      <div class="rung${terminal ? ' terminal' : ''}${items.length ? '' : ' empty'}" data-stage="${s.key}" role="listitem">
        <div class="rung-n mono">${items.length}</div>
        <div class="rung-label">${esc(s.label)}</div>
        <div class="rung-hint">${esc(s.hint)}</div>
        <div class="units">${items.length
          ? items.map(p => `<button type="button" class="unit" data-slug="${esc(p.slug)}" data-tip="${esc(nameOf(p))}" aria-label="${esc(nameOf(p))}"></button>`).join('')
          : terminal ? '<span class="void">Nothing here yet</span>' : ''}</div>
      </div>`;
  }).join('');
  const notes = [];
  if (withdrawn.length) notes.push(`Withdrawn and off the ladder: ${withdrawn.map(p => esc(nameOf(p))).join(', ')}.`);
  if (DATA.totals.stubs) notes.push(`${DATA.totals.stubs} <code>MOVED.md</code> stubs in <code>discovered/</code> point at promoted folders and are not counted.`);
  $('#ladder-note').innerHTML = notes.join(' ');
}

// ---- 03 Board -------------------------------------------------------------

const state = { domain: 'all', stage: 'all', sort: 'board', q: '' };

function paintControls() {
  const domains = [{ key: 'all', label: 'All' }, ...DATA.domains.map(d => ({ key: d.key, label: DOMAIN_SHORT[d.key] || d.label }))];
  $('#domain-seg').innerHTML = domains.map(d =>
    `<button type="button" data-domain="${d.key}" aria-pressed="${d.key === state.domain}">${esc(d.label)}</button>`).join('');
  const stages = [{ key: 'all', label: 'All stages' }, ...[...STAGES].reverse(), STAGE.withdrawn]
    .filter(s => s.key === 'all' || count(s.key) > 0);
  $('#stage-filter').innerHTML = stages.map(s => `
    <button type="button" class="chip" data-stage-filter="${s.key}" ${s.key !== 'all' ? `data-stage="${s.key}"` : ''} aria-pressed="${s.key === state.stage}">
      ${s.key !== 'all' ? '<i aria-hidden="true"></i>' : ''}${esc(s.label)}<span class="mono">${s.key === 'all' ? LIVE.length : count(s.key)}</span>
    </button>`).join('');

  $('#domain-seg').addEventListener('click', e => {
    const b = e.target.closest('button'); if (!b) return;
    state.domain = b.dataset.domain;
    $$('#domain-seg button').forEach(x => x.setAttribute('aria-pressed', x === b));
    paintBoard();
  });
  $('#sort-seg').addEventListener('click', e => {
    const b = e.target.closest('button'); if (!b) return;
    state.sort = b.dataset.sort;
    $$('#sort-seg button').forEach(x => x.setAttribute('aria-pressed', x === b));
    paintBoard();
  });
  $('#stage-filter').addEventListener('click', e => {
    const b = e.target.closest('button'); if (!b) return;
    setStage(b.dataset.stageFilter);
  });
  let t;
  $('#search').addEventListener('input', e => {
    clearTimeout(t);
    t = setTimeout(() => { state.q = e.target.value.trim().toLowerCase(); paintBoard(); }, 60);
  });
}

function setStage(key) {
  state.stage = key;
  $$('#stage-filter button').forEach(x => x.setAttribute('aria-pressed', x.dataset.stageFilter === key));
  paintBoard();
}

function matches(p) {
  if (state.domain !== 'all' && p.domain !== state.domain) return false;
  if (state.stage !== 'all' && stageOf(p) !== state.stage) return false;
  if (!state.q) return true;
  const hay = [nameOf(p), p.title, p.slug, p.statusRow?.status, p.statusRow?.notes, p.lede, STAGE[stageOf(p)].label]
    .join(' ').toLowerCase();
  return state.q.split(/\s+/).every(t => hay.includes(t));
}

// Board reading order: what is closest to moving first, dead ends last.
const BOARD_ORDER = ['solved', 'pass', 'held', 'panel', 'working', 'unworked', 'blocked', 'backlog', 'withdrawn'];
const byStage = (a, b) => (BOARD_ORDER.indexOf(stageOf(a)) - BOARD_ORDER.indexOf(stageOf(b))) ||
  (b.commits30d - a.commits30d) || nameOf(a).localeCompare(nameOf(b));

function row(p, showDomain) {
  const st = p.statusRow?.status;
  return `
    <div class="brow" role="row" data-slug="${esc(p.slug)}" data-stage="${stageOf(p)}" tabindex="0">
      <div role="cell" class="c-stage">${badge(p)}</div>
      <div role="cell" class="c-name">
        <span class="name">${esc(nameOf(p))}</span>
        <span class="slug mono">${showDomain ? `${esc(DOMAIN_SHORT[p.domain])} · ` : ''}${esc(p.id)}</span>
      </div>
      <div role="cell" class="c-status">${st ? md(st) : `<span class="dim">${p.domain === 'discovered' ? 'Proposal — not yet promoted' : 'No STATUS.md row'}</span>`}</div>
      <div role="cell" class="c-strip">${strip(p.commitDates90d || p.commitDates30d)}</div>
      <div role="cell" class="c-when mono">${esc(rel(p.lastTouch))}</div>
      <div role="cell" class="c-n mono">${p.commits30d || '<span class="dim">0</span>'}</div>
    </div>`;
}

function paintBoard() {
  const list = LIVE.filter(matches);
  const head = `
    <div class="brow bhead" role="row">
      <div role="columnheader">Stage</div><div role="columnheader">Problem</div>
      <div role="columnheader">Status, per STATUS.md</div><div role="columnheader">${SPAN} days</div>
      <div role="columnheader">Touched</div><div role="columnheader" title="Commits in the last 30 days">30d</div>
    </div>`;
  let body = '';
  if (state.sort === 'board') {
    for (const d of DATA.domains) {
      const rows = list.filter(p => p.domain === d.key).sort(byStage);
      if (!rows.length) continue;
      body += `<div class="bgroup" role="rowgroup">
        <div class="bgroup-head" role="row"><span role="cell">${esc(d.label)}</span><span class="mono dim">${rows.length}</span></div>
        ${rows.map(p => row(p, false)).join('')}</div>`;
    }
  } else {
    const sorted = [...list].sort(state.sort === 'recent'
      ? (a, b) => (b.lastTouch || '').localeCompare(a.lastTouch || '')
      : (a, b) => (b.commits30d - a.commits30d) || (b.commits90d - a.commits90d));
    body = `<div class="bgroup" role="rowgroup">${sorted.map(p => row(p, true)).join('')}</div>`;
  }
  $('#board-table').innerHTML = list.length
    ? `<div role="table" aria-label="All live problems">${head}${body}</div>`
    : `<p class="empty">Nothing matches. <button type="button" class="linkish" id="reset">Clear filters</button></p>`;
  $('#result-count').textContent = `${list.length} of ${LIVE.length}`;
  $('#reset')?.addEventListener('click', () => {
    state.q = ''; $('#search').value = '';
    state.domain = 'all'; $$('#domain-seg button').forEach(x => x.setAttribute('aria-pressed', x.dataset.domain === 'all'));
    setStage('all');
  });
}

// ---- 04 Tempo -------------------------------------------------------------

function paintPulse() {
  const days = DATA.pulse || [];
  const box = $('#pulse');
  if (!days.length) { box.innerHTML = `<p class="empty">No git history in this build.</p>`; return; }
  const totals = Object.fromEntries(ROLES.map(r => [r.key, days.reduce((a, d) => a + (d[r.key] || 0), 0)]));
  $('#pulse-legend').innerHTML = ROLES.filter(r => totals[r.key]).map(r =>
    `<span class="lg" data-role="${r.key}"><i></i>${r.label}<span class="mono">${totals[r.key]}</span></span>`).join('');

  renderPulse(days, totals);
  let rt;
  window.addEventListener('resize', () => { clearTimeout(rt); rt = setTimeout(() => renderPulse(days, totals), 120); });

  const tip = $('#tip');
  box.addEventListener('pointermove', e => {
    const h = e.target.closest('.hit');
    if (!h) { tip.hidden = true; return; }
    const d = days[+h.dataset.i];
    const rows = ROLES.filter(r => d[r.key]).map(r => `<div class="tip-row" data-role="${r.key}"><i></i>${r.label}<b>${d[r.key]}</b></div>`).join('');
    tip.innerHTML = `<div class="tip-h">${dm(d.date + 'T00:00:00Z')}</div>${rows || '<div class="dim">No commits</div>'}`;
    showTip(e.clientX, e.clientY);
  });
  box.addEventListener('pointerleave', () => { tip.hidden = true; });
}

// Drawn at the container's real pixel width so axis text is never stretched.
function renderPulse(days, totals) {
  const box = $('#pulse');
  const W = Math.max(300, Math.round(box.clientWidth || 760)), H = 200, padL = 26, padB = 20, padT = 8;
  const n = days.length, bw = (W - padL) / n;
  const max = Math.max(4, ...days.map(d => ROLES.reduce((a, r) => a + (d[r.key] || 0), 0)));
  const nice = max <= 5 ? 5 : max <= 10 ? 10 : Math.ceil(max / 10) * 10;
  const y = v => padT + (H - padT - padB) * (1 - v / nice);
  const grid = [0, nice / 2, nice].map(v =>
    `<line x1="${padL}" x2="${W}" y1="${y(v)}" y2="${y(v)}" class="grid"/><text x="${padL - 6}" y="${y(v) + 3}" class="axis" text-anchor="end">${v}</text>`).join('');
  let bars = '', hits = '', ticks = '';
  days.forEach((d, i) => {
    const x = padL + i * bw + 1;
    let acc = 0;
    for (const r of ROLES) {
      const v = d[r.key] || 0;
      if (!v) continue;
      const y0 = y(acc), y1 = y(acc + v);
      bars += `<rect x="${x.toFixed(1)}" y="${(y1 + 1).toFixed(1)}" width="${Math.max(1, bw - 2).toFixed(1)}" height="${Math.max(1, y0 - y1 - 1).toFixed(1)}" data-role="${r.key}"/>`;
      acc += v;
    }
    hits += `<rect class="hit" x="${(padL + i * bw).toFixed(1)}" y="0" width="${bw.toFixed(1)}" height="${H - padB}" data-i="${i}"/>`;
    const dt = new Date(d.date + 'T00:00:00Z');
    if (i === 0 || i === n - 1 || dt.getUTCDay() === 1 && i > 2 && i < n - 3) {
      ticks += `<text x="${(x + bw / 2 - 1).toFixed(1)}" y="${H - 5}" class="axis" text-anchor="middle">${i === n - 1 ? 'Today' : dm(d.date + 'T00:00:00Z')}</text>`;
    }
  });
  box.innerHTML = `<svg viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" role="img" aria-label="Commits per day by role over ${n} days">${grid}${bars}${ticks}${hits}</svg>`;
  const total = Object.values(totals).reduce((a, b) => a + b, 0);
  const busiest = days.reduce((a, d) => { const s = ROLES.reduce((x, r) => x + (d[r.key] || 0), 0); return s > a.s ? { s, d } : a; }, { s: 0, d: null });
  $('#pulse-cap').textContent = `${total} commits over ${n} days${busiest.d ? `; busiest day ${dm(busiest.d.date + 'T00:00:00Z')} with ${busiest.s}` : ''}.${DATA.history?.shallow ? ' History is a shallow clone, so older days read low.' : ''}`;
}

function paintRoutines() {
  const last = DATA.lastByRole || {};
  $('#routines').innerHTML = (DATA.routines || []).map(r => {
    const l = last[r.key];
    return `
      <li>
        <div class="rt-top"><span class="rt-name" data-role="${r.key}"><i></i>${esc(r.label)}</span><span class="mono rt-next" data-countdown="${r.key}"></span></div>
        <div class="rt-cad mono">${esc(r.cadence)}</div>
        <div class="rt-last">${l ? `Last commit ${esc(rel(l.date))}: <a href="${repoUrl}/commit/${l.sha}" target="_blank" rel="noopener">${esc(l.subject)}</a>` : '<span class="dim">No commit in window</span>'}</div>
      </li>`;
  }).join('');
}

// ---- 05 Dispatches --------------------------------------------------------

function chips(slugs) {
  return (slugs || []).filter(s => BY_SLUG[s]).map(s =>
    `<button type="button" class="pchip" data-slug="${esc(s)}">${esc(nameOf(BY_SLUG[s]).replace(/\s*\(.*?\)\s*$/, ''))}</button>`).join('');
}

function paintDispatches() {
  $('#dispatch-list').innerHTML = (DATA.dispatches || []).map(d => `
    <li class="dispatch">
      <div class="d-meta mono"><span>${esc(dm(d.date + 'T00:00:00Z'))}</span><span class="d-role" data-role="${esc(d.role)}"><i></i>${esc(d.role)}</span></div>
      <h3><a href="${blob(d.file)}" target="_blank" rel="noopener">${esc(d.title)}</a></h3>
      ${d.lede ? `<p>${esc(d.lede)}</p>` : ''}
      ${d.problems?.length ? `<div class="pchips">${chips(d.problems)}</div>` : ''}
    </li>`).join('') || `<li class="empty">No dispatches.</li>`;

  $('#wire').innerHTML = DATA.activity.slice(0, 36).map(a => `
    <li data-role="${esc(a.role || 'other')}">
      <span class="w-when">${esc(rel(a.date))}</span>
      <i aria-hidden="true"></i>
      <span class="w-subj" title="${esc(a.subject)}">${esc(a.subject)}</span>
      <a class="w-sha" href="${repoUrl}/commit/${a.sha}" target="_blank" rel="noopener">${esc(shortSha(a.sha))}</a>
    </li>`).join('') || `<li class="empty">No git history in this build.</li>`;

  const prs = [...DATA.prs].sort((a, b) =>
    ({ open: 0, merged: 1, closed: 2 }[a.state] ?? 3) - ({ open: 0, merged: 1, closed: 2 }[b.state] ?? 3) ||
    new Date(b.updated) - new Date(a.updated)).slice(0, 8);
  $('#prs').innerHTML = prs.length ? `<ol class="pr-list">${prs.map(p => `
    <li><a href="${p.url}" target="_blank" rel="noopener">
      <span class="pr-state mono" data-state="${p.state}">${p.draft ? 'draft' : p.state}</span>
      <span class="pr-title">${esc(p.title)}</span>
      <span class="mono dim">#${p.number} · ${esc(rel(p.updated))}</span></a></li>`).join('')}</ol>`
    : `<p class="fine">Queue empty${DATA.prs.length === 0 ? ' — or no GitHub token on this build' : ''}.</p>`;
}

// ---- Dossier --------------------------------------------------------------

const SIGNALS = [
  ['PROBLEM.md', 'hasProblem'], ['PROGRESS.md', 'hasProgress'], ['HANDOVER.md', 'hasHandover'],
  ['SOURCES.md', 'hasSources'], ['FREEZE.md', 'hasFreeze'], ['RESULTS.md', 'hasResults'],
  ['SOLUTION.md', 'hasSolution'], ['CLAIM.md', 'hasClaim'], ['analysis/', 'hasAnalysis'],
  ['code/', 'hasCode'], ['data/', 'hasData'], ['attempts/', 'hasAttempts'],
];
let lastFocus = null;

function openDossier(slug, push = true) {
  const p = BY_SLUG[slug];
  if (!p) return;
  lastFocus = document.activeElement;
  const el = $('#dossier');
  const files = SIGNALS.filter(([, k]) => p.files[k]);
  const related = (DATA.dispatches || []).filter(d => d.problems?.includes(slug)).slice(0, 4);
  el.innerHTML = `
    <div class="ds-bar">
      <span class="label">${esc(DOMAIN_SHORT[p.domain] || p.domain)} · dossier</span>
      <button type="button" class="ds-close" aria-label="Close dossier">Esc ✕</button>
    </div>
    <div class="ds-body">
      <div class="ds-badges">${badge(p)}${p.verdict && p.verdict !== 'WORKING' ? `<span class="mono dim">${esc(p.verdict)}</span>` : ''}</div>
      <h2 id="dossier-title">${esc(p.title)}</h2>
      <p class="ds-slug mono"><a href="${tree(p.slug)}" target="_blank" rel="noopener">${esc(p.slug)}/</a></p>
      ${p.statusRow?.status ? `<section><h3 class="label">Status · STATUS.md</h3><p class="ds-status">${md(p.statusRow.status)}</p></section>` : ''}
      ${p.claim ? `<section class="ds-claim"><h3 class="label">Validation queue · ${esc(p.claim.claim)}</h3>
        <p>${md(p.claim.disposition)}</p>
        <h3 class="label">Decisive missing check</h3><p>${md(p.claim.missingCheck)}</p></section>` : ''}
      ${p.statusRow?.notes ? `<section><h3 class="label">Notes · STATUS.md</h3><p class="ds-notes">${md(p.statusRow.notes)}</p></section>` : ''}
      ${!p.statusRow ? `<section><h3 class="label">Lede · PROBLEM.md</h3><p class="ds-notes">${esc(p.lede || 'No lede recorded.')}</p></section>` : ''}
      <section class="ds-activity">
        <h3 class="label">Activity · ${SPAN} days</h3>
        ${strip(p.commitDates90d || p.commitDates30d, SPAN, 440, 34)}
        <dl class="ds-stats mono">
          <div><dt>30d</dt><dd>${p.commits30d}</dd></div>
          <div><dt>90d</dt><dd>${p.commits90d}</dd></div>
          <div><dt>Touched</dt><dd>${esc(rel(p.lastTouch))}</dd></div>
        </dl>
        ${p.lastSubject ? `<p class="ds-last mono">${esc(p.lastSubject)}</p>` : ''}
      </section>
      <section>
        <h3 class="label">In the folder</h3>
        <ul class="ds-files mono">${files.map(([name]) => {
          const isDir = name.endsWith('/');
          return `<li><a href="${isDir ? tree(`${p.slug}/${name.slice(0, -1)}`) : blob(`${p.slug}/${name}`)}" target="_blank" rel="noopener">${esc(name)}</a></li>`;
        }).join('')}</ul>
      </section>
      ${related.length ? `<section><h3 class="label">Mentioned in dispatches</h3><ul class="ds-related">${related.map(d =>
        `<li><span class="mono dim">${esc(dm(d.date + 'T00:00:00Z'))}</span> <a href="${blob(d.file)}" target="_blank" rel="noopener">${esc(d.title)}</a></li>`).join('')}</ul></section>` : ''}
    </div>`;
  el.hidden = false; $('#scrim').hidden = false;
  document.body.classList.add('locked');
  requestAnimationFrame(() => el.classList.add('open'));
  $('.ds-close', el).addEventListener('click', () => closeDossier());
  $('.ds-close', el).focus();
  if (push) history.replaceState(null, '', `#p/${slug}`);
}

function closeDossier() {
  const el = $('#dossier');
  if (el.hidden) return;
  el.classList.remove('open');
  $('#scrim').hidden = true;
  document.body.classList.remove('locked');
  setTimeout(() => { el.hidden = true; }, 180);
  if (location.hash.startsWith('#p/')) history.replaceState(null, '', location.pathname);
  lastFocus?.focus?.();
}

function wireGlobal() {
  document.addEventListener('click', e => {
    const t = e.target.closest('[data-slug]');
    if (t && !e.target.closest('a')) openDossier(t.dataset.slug);
  });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') { closeDossier(); return; }
    if ((e.key === 'Enter' || e.key === ' ') && e.target.matches('[data-slug][tabindex]')) {
      e.preventDefault(); openDossier(e.target.dataset.slug); return;
    }
    if (e.key === '/' && !e.target.matches('input, textarea')) {
      e.preventDefault(); $('#search').focus();
      $('#board').scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
    }
  });
  $('#scrim').addEventListener('click', closeDossier);

  const tip = $('#tip');
  document.addEventListener('pointerover', e => {
    const u = e.target.closest('.unit');
    if (!u) return;
    tip.innerHTML = `<div class="tip-h">${esc(u.dataset.tip)}</div>`;
    const r = u.getBoundingClientRect();
    showTip(r.left + r.width / 2, r.top);
  });
  document.addEventListener('pointerout', e => { if (e.target.closest('.unit')) tip.hidden = true; });

  const m = location.hash.match(/^#p\/(.+)$/);
  if (m) openDossier(decodeURIComponent(m[1]), false);
}

function showTip(x, y) {
  const tip = $('#tip');
  tip.hidden = false;
  const r = tip.getBoundingClientRect();
  const left = Math.min(window.innerWidth - r.width - 8, Math.max(8, x - r.width / 2));
  const top = y - r.height - 12 < 8 ? y + 16 : y - r.height - 12;
  tip.style.transform = `translate(${Math.round(left)}px, ${Math.round(top)}px)`;
}

function paintFoot() {
  const h = DATA.history || {};
  const bits = [
    `Generated ${new Date(DATA.generatedAt).toISOString().replace('T', ' ').slice(0, 16)} UTC`,
    `<a href="${repoUrl}/commit/${DATA.repo.headSha}" target="_blank" rel="noopener">${esc(shortSha(DATA.repo.headSha))}</a>`,
    h.available ? `${h.commits} commits${h.shallow ? ' (shallow clone)' : ''}` : 'no git history in this build',
    `<a href="/data.json">data.json</a>`,
    `<a href="${repoUrl}" target="_blank" rel="noopener">source</a>`,
  ];
  $('#foot-meta').innerHTML = bits.join('<span class="sep">/</span>');
}

// ---- Boot -----------------------------------------------------------------

paintMast();
paintSitrep();
paintClaims();
paintLadder();
paintControls();
paintBoard();
paintPulse();
paintRoutines();
paintDispatches();
paintFoot();
wireGlobal();
tick();
