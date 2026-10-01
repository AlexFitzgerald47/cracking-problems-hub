// Framework page: the live parts are read from /data.json, the same draw that
// `npm run draw` prints, so the page can never describe a different rule.

const $ = s => document.querySelector(s);
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const NS = 'http://www.w3.org/2000/svg';
const el = (t, a = {}, p) => { const n = document.createElementNS(NS, t); for (const [k, v] of Object.entries(a)) n.setAttribute(k, v); p?.appendChild(n); return n; };
const rel = iso => { const m = Math.floor((Date.now() - new Date(iso)) / 60000); return m < 60 ? `${Math.max(1, m)}m ago` : m < 1440 ? `${Math.floor(m / 60)}h ago` : `${Math.floor(m / 1440)}d ago`; };
const STAGE = { held: 'Held', panel: 'Panel pending', working: 'In work', unworked: 'Unworked', blocked: 'Blocked' };

setInterval(() => { $('#clock').textContent = new Date().toISOString().slice(11, 19) + 'Z'; }, 1000);

const data = await fetch('/data.json').then(r => r.json()).catch(() => null);
const d = data?.draw;
if (!d) {
  $('#live').innerHTML = '<p class="empty">The draw is not available in this build.</p>';
} else {
  const by = Object.fromEntries(data.problems.map(p => [p.slug, p]));
  const name = s => (by[s]?.shortTitle || by[s]?.title || s).replace(/\s*\(.*?\)\s*$/, '');
  const L = d.rotation.last, P = d.pick;

  // The rotor: four stream sectors, the last one worked, the next one drawn.
  const svg = $('#rotor');
  d.streams.forEach((s, i) => {
    const a0 = (i * 90 - 90 + 4) * Math.PI / 180, a1 = ((i + 1) * 90 - 90 - 4) * Math.PI / 180;
    const R = 190, r = 96;
    const p = (a, rr) => `${(rr * Math.cos(a)).toFixed(1)} ${(rr * Math.sin(a)).toFixed(1)}`;
    const cls = s.id === P?.stream ? 'next' : s.id === L?.stream ? 'last' : '';
    el('path', { d: `M${p(a0, r)}L${p(a0, R)}A${R} ${R} 0 0 1 ${p(a1, R)}L${p(a1, r)}A${r} ${r} 0 0 0 ${p(a0, r)}Z`, class: `sec ${cls}` }, svg);
    const mid = (i * 90 - 45) * Math.PI / 180;
    const t = el('text', { x: (143 * Math.cos(mid)).toFixed(1), y: (143 * Math.sin(mid) - 6).toFixed(1), class: `sid ${cls}` }, svg);
    t.textContent = s.id;
    const t2 = el('text', { x: (143 * Math.cos(mid)).toFixed(1), y: (143 * Math.sin(mid) + 14).toFixed(1), class: 'slabel' }, svg);
    t2.textContent = s.label.replace('Undeciphered texts', 'Texts').toUpperCase();
  });
  // Rotation arrows on the outer rim.
  for (let i = 0; i < 4; i++) {
    const a = (i * 90 - 90 + 45 + 45) * Math.PI / 180;
    const x = 205 * Math.cos(a), y = 205 * Math.sin(a);
    el('path', { d: 'M-6 -5L6 0L-6 5Z', class: 'arrow', transform: `translate(${x.toFixed(1)} ${y.toFixed(1)}) rotate(${(i * 90 + 90)})` }, svg);
  }
  el('circle', { r: 78, class: 'hub' }, svg);
  const c1 = el('text', { y: -8, class: 'hub-l' }, svg); c1.textContent = 'NEXT FIRING';
  const c2 = el('text', { y: 22, class: 'hub-n' }, svg); c2.textContent = P ? `Stream ${P.stream}` : '—';

  const f = P && d.streams.flatMap(s => s.files).find(x => x.slug === P.slug);
  $('#live').innerHTML = `
    ${L ? `<p class="lv-last"><span class="mono">Last Breaker session</span> Stream ${esc(L.stream)} · ${esc(name(L.slug))} · ${esc(rel(L.date))}</p>` : ''}
    ${P ? `<p class="lv-pick-l mono">The pick · stream ${esc(P.stream)}${P.skipped ? ` (skipped ${P.skipped} with nothing movable)` : ''}</p>
    <h2 class="lv-pick"><a href="/#p/${esc(P.slug)}">${esc(name(P.slug))}</a></h2>
    <p class="lv-why">${esc(STAGE[f.stage] || f.stage)} · idle ${Math.floor(f.idle)} days · debt ${Math.round(f.debt)} — ${esc(P.reason)}.</p>
    ${f.next ? `<p class="lv-next"><span class="mono">Next move</span>${esc(f.next)}</p>` : '<p class="lv-next warn">No next move written yet.</p>'}` : '<p>Nothing is drawable right now.</p>'}
    ${d.overwatch?.length ? `<p class="lv-ow"><span class="mono">Owed to Overwatch</span>${d.overwatch.map(s => esc(name(s))).join(', ')} — panels no Breaker can convene.</p>` : ''}
    <p class="lv-cta"><a href="/#draw">See the board →</a></p>`;

  // Weights, drawn to scale, and the arithmetic on today's pick.
  const W = d.weights, maxW = Math.max(...Object.values(W));
  $('#weights').innerHTML = Object.entries(W).filter(([k]) => k !== 'panel').map(([k, v]) => `
    <div class="w-row s-${k}"><span class="w-name">${esc(STAGE[k] || k)}</span><span class="w-bar"><i style="width:${(v / maxW * 100).toFixed(0)}%"></i></span><span class="mono">× ${v.toFixed(1)}</span></div>`).join('')
    + `<div class="w-row s-panel dim"><span class="w-name">Panel pending</span><span class="w-bar"></span><span class="mono">owed to Overwatch</span></div>`;
  if (f) $('#worked').innerHTML = `Today's pick: <b>${esc(name(P.slug))}</b> has gone <b>${Math.floor(f.idle)} days</b> without a working session and is <b>${esc((STAGE[f.stage] || f.stage).toLowerCase())}</b> (× ${W[f.stage]}), so its debt is ${f.idle.toFixed(1)} × ${W[f.stage]} = <b>${Math.round(f.debt)}</b>${f.pickup ? ` — and as a held claim idle past ${d.pickupDays} days it jumps the queue under the pick-up rule.` : `, the highest in stream ${esc(P.stream)} that nobody holds.`} Blocked files rank but never lead; a held claim idle past ${d.pickupDays} days jumps the queue.`;

  const REPO = data.repo.url;
  $('#src').innerHTML = [
    ['_roles/README.md', 'The rules, under “The draw”'],
    ['_roles/BREAKER.md', 'How a Breaker chooses, and the release rule'],
    ['_roles/ORCHESTRATOR.md', 'What Overwatch owes the draw each pass'],
    ['board/streams/README.md', 'The four stream briefs'],
    ['board/SCHEDULE.md', 'The routine prompts that enforce it'],
    ['scripts/derive.mjs', 'The computation itself (computeDraw)'],
    ['board/log/2026-09-27-the-draw.md', 'Why these rules, and what the first draw found'],
  ].map(([p, what]) => `<li><a class="mono" href="${REPO}/blob/main/${p}" target="_blank" rel="noopener">${esc(p)}</a><span>${esc(what)}</span></li>`).join('');
}
