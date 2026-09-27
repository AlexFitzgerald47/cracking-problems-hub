// Cracking Problems Hub — client-side interactivity.
// Data is inlined at build time in <script id="hub-data">.

const DATA = JSON.parse(document.getElementById('hub-data').textContent);

const $ = (sel, root = document) => root.querySelector(sel);
const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));
const fmtDate = iso => {
  if (!iso) return '—';
  const d = new Date(iso);
  const now = Date.now();
  const days = Math.floor((now - d.getTime()) / 86400000);
  if (days === 0) return 'today';
  if (days === 1) return 'yesterday';
  if (days < 30) return `${days}d ago`;
  if (days < 365) return `${Math.round(days / 30)}mo ago`;
  return d.toISOString().slice(0, 10);
};
const shortSha = s => s ? s.slice(0, 7) : '';

const STATE_LABELS = {
  solved: 'SOLVED', validated: 'PASS', held: 'HELD',
  frozen: 'FROZEN', active: 'ACTIVE', quiet: 'QUIET',
  proposed: 'BACKLOG', closed: 'CLOSED', withdrawn: 'WITHDRAWN',
};

const STATE_ORDER = ['solved','validated','held','frozen','active','quiet','proposed','closed','withdrawn'];

// ---- Hero + top-level ----
function paintHero() {
  const { repo, generatedAt, activity, prs, totals } = DATA;
  $('#hero-branch').textContent = repo.branch || 'main';
  $('#hero-generated').textContent = `updated ${fmtDate(generatedAt)}`;
  $('#hero-sha').textContent = shortSha(repo.headSha);
  const lastCommit = activity[0];
  $('#hero-last-subject').textContent = lastCommit ? lastCommit.subject : '';
  const open = prs.filter(p => p.state === 'open').length;
  $('#hero-open-prs').textContent = open;
  $('#hero-open-prs-sub').textContent = open === 0
    ? 'Empty queue — sixth consecutive pass'
    : `${open} awaiting review`;

  $('#repo-link').href = repo.url;
  $('#foot-repo').href = repo.url;
  $('#foot-generated').textContent = `generated ${new Date(generatedAt).toISOString().replace('T',' ').slice(0,16)} UTC`;

  $('#m-total').textContent = totals.problems;
  $('#m-active').textContent = totals.active;
  $('#m-held').textContent = totals.held;
  $('#m-frozen').textContent = totals.frozen;
  $('#m-validated').textContent = totals.validated;
  $('#m-proposed').textContent = totals.proposed;
}

// ---- Ring SVG ----
function ringHtml(pct, state) {
  const r = 18, c = 2 * Math.PI * r;
  const off = c * (1 - pct / 100);
  return `
    <div class="ring" data-state="${state}" style="--p:${pct}">
      <svg width="46" height="46" viewBox="0 0 46 46">
        <circle class="track" cx="23" cy="23" r="${r}" fill="none" stroke-width="3.5"/>
        <circle class="fill" cx="23" cy="23" r="${r}" fill="none" stroke-width="3.5"
                stroke-dasharray="${c}" stroke-dashoffset="${off}" stroke-linecap="round"/>
      </svg>
      <span class="label">${pct}</span>
    </div>`;
}

function sparkHtml(dates) {
  // 30 buckets, one per day
  const buckets = new Array(30).fill(0);
  const now = Date.now();
  for (const d of dates) {
    const days = Math.floor((now - new Date(d).getTime()) / 86400000);
    if (days >= 0 && days < 30) buckets[29 - days] += 1;
  }
  const max = Math.max(1, ...buckets);
  return `<span class="spark" aria-hidden="true">${buckets.map(v => {
    const h = Math.round((v / max) * 22);
    return `<i class="${v > 0 ? 'hot' : ''}" style="height:${Math.max(2, h)}px"></i>`;
  }).join('')}</span>`;
}

// ---- Frontier ----
function paintFrontier() {
  const top = [...DATA.problems]
    .filter(p => p.state !== 'proposed' && p.state !== 'quiet')
    .sort((a, b) => b.crackScore - a.crackScore || b.commits30d - a.commits30d)
    .slice(0, 10);
  const list = $('#frontier-list');
  const domainByKey = Object.fromEntries(DATA.domains.map(d => [d.key, d]));
  list.innerHTML = top.map((p, i) => {
    const dom = domainByKey[p.domain];
    const verdict = p.verdict || STATE_LABELS[p.state];
    return `
      <div class="frontier-row" data-state="${p.state}" data-id="${p.slug}">
        <div class="rank">${String(i + 1).padStart(2, '0')}</div>
        <div class="body">
          <h3>${escapeHtml(p.title)}</h3>
          <div class="sub">
            <span class="dom" data-accent="${dom?.accent || ''}">${dom?.label || p.domain}</span>
            <span class="dot">·</span>
            <span>${p.commits30d} commits · 30d</span>
            <span class="dot">·</span>
            <span>${fmtDate(p.lastTouch)}</span>
          </div>
        </div>
        <div class="bar-cell">
          <span class="bar-score">${p.crackScore}</span>
          <div class="bar"><i data-target="${p.crackScore}"></i></div>
        </div>
        <div class="verdict-cell">
          <span class="verdict-badge" data-verdict="${verdict}">${verdict}</span>
        </div>
      </div>`;
  }).join('');
  // Animate bars in
  requestAnimationFrame(() => {
    $$('.frontier-row .bar > i').forEach(el => {
      el.style.width = el.dataset.target + '%';
    });
  });
  $$('.frontier-row').forEach(row => {
    row.addEventListener('click', () => openDetail(row.dataset.id));
  });
}

// ---- Grid ----
let activeDomain = 'all';
let activeState = 'all';
let searchTerm = '';

function paintDomainChips() {
  const box = $('#domain-chips');
  box.innerHTML = [{ key: 'all', label: 'All domains' }, ...DATA.domains]
    .map(d => `<button class="chip ${d.key === 'all' ? 'on' : ''}" data-domain="${d.key}">${d.label}</button>`)
    .join('');
  $$('#domain-chips .chip').forEach(btn => {
    btn.addEventListener('click', () => {
      $$('#domain-chips .chip').forEach(b => b.classList.remove('on'));
      btn.classList.add('on');
      activeDomain = btn.dataset.domain;
      paintGrid();
    });
  });
  $$('#state-chips .chip').forEach(btn => {
    btn.addEventListener('click', () => {
      $$('#state-chips .chip').forEach(b => b.classList.remove('on'));
      btn.classList.add('on');
      activeState = btn.dataset.state;
      paintGrid();
    });
  });
  $$('.metric[data-state]').forEach(m => {
    m.addEventListener('click', () => {
      const s = m.dataset.state;
      $$('#state-chips .chip').forEach(b => b.classList.toggle('on', b.dataset.state === s));
      activeState = s;
      paintGrid();
      $('#board').scrollIntoView({ behavior: 'smooth' });
    });
  });
}

function matchesState(problem) {
  if (activeState === 'all') return true;
  if (activeState === 'validated') return problem.state === 'validated' || problem.state === 'solved';
  if (activeState === 'closed') return problem.state === 'closed' || problem.state === 'withdrawn';
  return problem.state === activeState;
}

function paintGrid() {
  const domainByKey = Object.fromEntries(DATA.domains.map(d => [d.key, d]));
  const filtered = DATA.problems
    .filter(p => activeDomain === 'all' || p.domain === activeDomain)
    .filter(matchesState)
    .filter(p => {
      if (!searchTerm) return true;
      const t = searchTerm.toLowerCase();
      return p.title.toLowerCase().includes(t) ||
             p.id.toLowerCase().includes(t) ||
             (p.verdict || '').toLowerCase().includes(t) ||
             p.lede.toLowerCase().includes(t);
    })
    .sort((a, b) => {
      const ao = STATE_ORDER.indexOf(a.state);
      const bo = STATE_ORDER.indexOf(b.state);
      if (ao !== bo) return ao - bo;
      return b.crackScore - a.crackScore;
    });

  const grid = $('#grid');
  grid.innerHTML = filtered.map(p => {
    const dom = domainByKey[p.domain];
    const verdict = p.verdict || STATE_LABELS[p.state];
    return `
      <article class="card" data-id="${p.slug}" data-state="${p.state}">
        <div class="card-head">
          ${ringHtml(p.crackScore, p.state)}
          <div style="flex:1; min-width:0;">
            <h3 class="card-title">${escapeHtml(p.title)}</h3>
            <div style="display:flex; gap:8px; margin-top:4px; align-items:center;">
              <span class="dom" data-accent="${dom?.accent || ''}">${dom?.label || p.domain}</span>
              <span class="verdict-badge" data-verdict="${verdict}">${verdict}</span>
            </div>
          </div>
        </div>
        <p class="card-lede">${escapeHtml(p.lede || 'No PROBLEM.md lede yet.')}</p>
        <div class="card-foot">
          <div class="meta">
            <span><span class="n">${p.commits30d}</span>·30d</span>
            <span><span class="n">${p.commits90d}</span>·90d</span>
            <span>${fmtDate(p.lastTouch)}</span>
          </div>
          ${sparkHtml(p.commitDates30d)}
        </div>
      </article>`;
  }).join('');

  $('#grid-empty').hidden = filtered.length > 0;

  // Card hover ripple origin
  $$('.card').forEach(card => {
    card.addEventListener('mousemove', e => {
      const r = card.getBoundingClientRect();
      card.style.setProperty('--mx', `${e.clientX - r.left}px`);
    });
    card.addEventListener('click', () => openDetail(card.dataset.id));
  });
}

// ---- Timeline ----
function paintTimeline() {
  const rows = DATA.activity.slice(0, 80);
  $('#timeline').innerHTML = rows.map(r => `
    <div class="tl-row" data-kind="${r.kind}">
      <span class="date">${new Date(r.date).toISOString().slice(0,10)}</span>
      <span class="dot"></span>
      <span class="subject" title="${escapeAttr(r.subject)}">${escapeHtml(r.subject)}</span>
      <a class="sha" href="${DATA.repo.url}/commit/${r.sha}" target="_blank" rel="noopener">${shortSha(r.sha)}</a>
    </div>
  `).join('');
}

// ---- PRs ----
function paintPRs() {
  const sorted = [...DATA.prs].sort((a, b) => {
    const so = { open: 0, merged: 1, closed: 2 };
    return (so[a.state] ?? 3) - (so[b.state] ?? 3) ||
           new Date(b.updated) - new Date(a.updated);
  });
  const list = $('#pr-list');
  if (sorted.length === 0) {
    list.innerHTML = `<p class="empty">No pull-request data available (either the token is not set on Railway or the queue is empty).</p>`;
    return;
  }
  list.innerHTML = sorted.slice(0, 24).map(pr => `
    <a class="pr" href="${pr.url}" target="_blank" rel="noopener">
      <div class="num">#${pr.number} · ${pr.user || 'unknown'} · ${fmtDate(pr.updated)}</div>
      <div class="title">${escapeHtml(pr.title)}</div>
      <div class="meta">
        <span class="pr-state ${pr.state}">${pr.state}</span>
        ${pr.draft ? '<span class="pr-state closed">draft</span>' : ''}
      </div>
    </a>
  `).join('');
}

// ---- Detail drawer ----
function openDetail(slug) {
  const p = DATA.problems.find(x => x.slug === slug);
  if (!p) return;
  const dom = DATA.domains.find(d => d.key === p.domain);
  const signals = [
    ['PROBLEM.md', p.files.hasProblem],
    ['PROGRESS.md', p.files.hasProgress],
    ['HANDOVER.md', p.files.hasHandover],
    ['SOURCES.md', p.files.hasSources],
    ['FREEZE.md', p.files.hasFreeze],
    ['RESULTS.md', p.files.hasResults],
    ['SOLUTION.md', p.files.hasSolution],
    ['analysis/', p.files.hasAnalysis],
    ['code/', p.files.hasCode],
    ['data/', p.files.hasData],
    ['attempts/', p.files.hasAttempts],
    ['MOVED.md', p.files.hasMoved],
  ];
  const el = $('#detail');
  const verdict = p.verdict || STATE_LABELS[p.state];
  el.hidden = false;
  el.innerHTML = `
    <button class="close" aria-label="Close">×</button>
    <h2>${escapeHtml(p.title)}</h2>
    <div class="d-sub">
      <span class="dom" data-accent="${dom?.accent || ''}">${dom?.label || p.domain}</span>
      <span class="verdict-badge" data-verdict="${verdict}">${verdict}</span>
      <span>Crack score <b style="color:var(--cyan)">${p.crackScore}</b></span>
      <span>${p.commits30d} commits · 30d</span>
      <span>${p.commits90d} commits · 90d</span>
      <span>Last touched ${fmtDate(p.lastTouch)}</span>
    </div>
    <div class="d-grid">
      <div class="d-block">
        <h4>Lede</h4>
        <p style="margin:0 0 20px; color:var(--muted);">${escapeHtml(p.lede || 'No PROBLEM.md lede recorded.')}</p>
        <h4>Latest commit subject</h4>
        <p style="margin:0 0 20px; font-family:var(--mono); font-size:.86rem; color:var(--muted);">${escapeHtml(p.lastSubject || '—')}</p>
        ${p.contextExcerpt ? `
        <h4>STATUS.md context</h4>
        <div class="excerpt">${escapeHtml(p.contextExcerpt.trim())}</div>` : ''}
      </div>
      <div class="d-block">
        <h4>File signals</h4>
        <div class="signals">
          ${signals.map(([name, on]) => `<div class="signal ${on ? 'on' : ''}">${name}</div>`).join('')}
        </div>
        <h4 style="margin-top:22px;">Repository</h4>
        <p style="margin:0;">
          <a href="${DATA.repo.url}/tree/${DATA.repo.branch}/${p.slug}" target="_blank" rel="noopener"
             style="color:var(--cyan); font-family:var(--mono); font-size:.88rem;">
            ${p.slug}/ ↗
          </a>
        </p>
      </div>
    </div>
  `;
  $('#detail .close').addEventListener('click', () => {
    el.hidden = true;
  });
  el.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

// ---- Utility ----
function escapeHtml(s) {
  return (s || '').replace(/[&<>"']/g, c => ({ '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;' }[c]));
}
function escapeAttr(s) { return escapeHtml(s); }

function wireSearch() {
  let t;
  $('#search').addEventListener('input', e => {
    clearTimeout(t);
    t = setTimeout(() => {
      searchTerm = e.target.value.trim();
      paintGrid();
    }, 80);
  });
}

function wireScrollButtons() {
  $$('[data-scroll]').forEach(b => {
    b.addEventListener('click', () => {
      const target = document.querySelector(b.dataset.scroll);
      target?.scrollIntoView({ behavior: 'smooth' });
    });
  });
}

// ---- Boot ----
paintHero();
paintFrontier();
paintDomainChips();
paintGrid();
paintTimeline();
paintPRs();
wireSearch();
wireScrollButtons();

// Ambient tick — updates the "updated Xd ago" without a rebuild.
setInterval(() => {
  $('#hero-generated').textContent = `updated ${fmtDate(DATA.generatedAt)}`;
}, 60_000);
