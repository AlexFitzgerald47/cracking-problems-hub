// Derived fields for the situation-room UI. Everything here is additive: it
// reads STATUS.md's tables, board/log, board/active and git history, and adds
// new keys to problems/activity. Existing fields (verdict, state, crackScore…)
// are never rewritten.
//
// Why parse STATUS.md at all, given build.mjs avoids it: the *prose* is
// unreliable to regex, but the Active Problems / Validation queue tables are
// structured — one row per folder, keyed by a backticked path. That is the
// curated disposition, and the war room should show it verbatim.

import { execSync } from 'node:child_process';
import { promises as fs } from 'node:fs';
import path from 'node:path';

const DAY = 86400_000;

function sectionOf(md, heading) {
  const i = md.search(new RegExp(`^##\\s+${heading}`, 'm'));
  if (i < 0) return '';
  const rest = md.slice(i + 1);
  const j = rest.search(/^##\s+/m);
  return j < 0 ? rest : rest.slice(0, j);
}

function tableRows(md) {
  return md.split('\n')
    .filter(l => /^\|/.test(l) && !/^\|\s*-{3,}/.test(l))
    .map(l => l.replace(/^\|/, '').replace(/\|\s*$/, '').split(/\s\|\s/).map(c => c.trim()));
}

const stripMd = s => (s || '').replace(/~~(.+?)~~/g, '$1').replace(/\*\*(.+?)\*\*/g, '$1')
  .replace(/\*(.+?)\*/g, '$1').replace(/`([^`]+)`/g, '$1').trim();

const firstDate = s => (s.match(/20\d\d-\d\d-\d\d/) || [null])[0];

// { 'ciphers/kryptos': { name, status, notes, suggestedDomain } }
function parseStatusRows(statusText, domainKeys) {
  const out = {};
  const scope = sectionOf(statusText, 'Active Problems') + '\n' + sectionOf(statusText, 'Recently Proposed');
  for (const cells of tableRows(scope)) {
    if (cells.length < 3) continue;
    const m = cells[1].match(/^`([a-z0-9-]+\/[a-z0-9-]+)\/?`$/);
    if (!m) continue;
    const slug = m[1];
    const third = stripMd(cells[2]);
    const isDomain = domainKeys.includes(third);
    out[slug] = {
      name: stripMd(cells[0]),
      status: isDomain ? '' : cells[2],
      notes: cells.slice(3).join(' | '),
      suggestedDomain: isDomain ? third : null,
    };
  }
  return out;
}

function parseValidationQueue(statusText) {
  return tableRows(sectionOf(statusText, 'Validation queue'))
    .filter(c => c.length >= 3 && !/^Claim$/i.test(c[0]))
    .map(c => ({ claim: stripMd(c[0]), disposition: c[1], missingCheck: c.slice(2).join(' | ') }));
}

// Match a validation row to a problem by the first word of the claim against
// the first word of the STATUS row name ("Chinese", "Mesha", "Ennis", "VENONA",
// "Linear", "Byblos"). Only an unambiguous single match is accepted.
function matchClaim(row, rows) {
  const key = row.claim.split(/\s+/)[0].toLowerCase();
  const hits = Object.entries(rows).filter(([slug, r]) =>
    !slug.startsWith('discovered/') && r.name.split(/\s+/)[0].toLowerCase() === key);
  if (hits.length === 1) return hits[0][0];
  const held = hits.filter(([, r]) => /\bHELD\b/.test(r.status));
  return held.length === 1 ? held[0][0] : null;
}

// Pipeline stage. Verdict-bearing stages (held, withdrawn, solved, pass) come
// only from the versioned verdict build.mjs already assigns — never from the
// STATUS table — so the curated HELD_PARTIAL / WITHDRAWN sets stay the single
// authority. The table only refines the non-verdict stages.
function stageOf(p, row, claim) {
  if (p.files.hasMoved) return 'stub';
  const st = row?.status || '';
  // 'validated' (SOLVE-CLAIMED) is a file-signal guess, not a panel verdict, so it
  // never maps to pass; nothing in the build yet emits a real PASS.
  if (p.verdict === 'WITHDRAWN') return 'withdrawn';
  if (p.verdict === 'SOLVED') return 'solved';
  if (p.verdict === '3×PARTIAL') return 'held';
  if (claim && /panel pending/i.test(claim.disposition)) return 'panel';
  if (/CLOSED|blocked/i.test(st)) return 'blocked';
  if (p.domain === 'discovered') return 'backlog';
  if (/never worked/i.test(st)) return 'unworked';
  if (!row && !(p.files.hasHandover || p.files.hasAttempts || p.files.hasAnalysis)) return 'unworked';
  return 'working';
}

const INFRA = /^(src\/|scripts\/|server\.mjs|Dockerfile|package(-lock)?\.json|railway\.toml|nixpacks\.toml|\.dockerignore|\.gitignore)/;
const PROBLEM_PATH = /^(ciphers|historical-texts|historical-controversies|ireland|discovered)\/([^/_.][^/]*)\//;

function roleOf(subject, files) {
  const s = subject.toLowerCase();
  if (/^merge /.test(s)) return 'merge';
  if (files.length && files.every(f => INFRA.test(f))) return 'infra';
  // Squash-merged human PRs ("… (#13)") are not a routine firing.
  if (/\(#\d+\)\s*$/.test(subject)) return 'other';
  if (/orchestrator|reconcil|^status:/.test(s)) return 'orchestrator';
  if (/validator|\bpanel\b|verdict/.test(s)) return 'validator';
  if (/finder|discovery|^propos/.test(s)) return 'finder';
  const probs = files.map(f => f.match(PROBLEM_PATH)).filter(Boolean);
  if (probs.length && probs.every(m => m[1] === 'discovered')) return 'finder';
  if (probs.length || /^claim|^release|cracker/.test(s)) return 'cracker';
  if (files.some(f => /^(STATUS\.md|board\/)/.test(f))) return 'orchestrator';
  return 'other';
}

function readGitLog(ROOT, days) {
  try {
    const out = execSync(
      `git log --since=${days}.days.ago --name-only --no-renames --pretty=format:'%x1e%H%x1f%cI%x1f%s%x1f%an%x1f%(trailers:key=Co-Authored-By,valueonly,separator=;)'`,
      { encoding: 'utf8', cwd: ROOT, maxBuffer: 64 * 1024 * 1024 });
    return out.split('\x1e').filter(Boolean).map(block => {
      const [head, ...rest] = block.split('\n');
      const [sha, date, subject, author = '', coauth = ''] = head.split('\x1f');
      // A Claude author or co-author trailer marks a routine session; anything
      // else was run outside the routines (the Codex lane, or the human).
      const unit = /claude/i.test(author + ' ' + coauth) ? 'claude' : 'irregular';
      return { sha, date, subject, unit, files: rest.map(s => s.trim()).filter(Boolean) };
    });
  } catch { return []; }
}

function historyInfo(ROOT) {
  const run = cmd => { try { return execSync(cmd, { encoding: 'utf8', cwd: ROOT, stdio: ['ignore', 'pipe', 'ignore'] }).trim(); } catch { return null; } };
  const shallow = run('git rev-parse --is-shallow-repository');
  if (shallow === null) return { available: false, shallow: false, commits: 0, since: null };
  // Reported, not repaired: a shallow clone truncates activity and the UI says so.
  return {
    available: true,
    shallow: shallow === 'true',
    commits: Number(run('git rev-list --count HEAD') || 0),
    since: run('git log --reverse --pretty=format:%cI | head -1') || null,
  };
}

function parseLastUpdated(statusText) {
  const m = statusText.match(/^\*\*Last updated:\*\*\s*(\d{4}-\d\d-\d\d),\s*(.+)$/m);
  if (!m) return null;
  // First clause only: "<date>, **label** (detail). Full report: …"
  const firstClause = m[2].split(/\.\s+Full report:/)[0];
  const label = (firstClause.match(/\*\*(.+?)\*\*/) || [null, ''])[1];
  const detail = (firstClause.match(/\((.+)\)\s*$/) || [null, ''])[1];
  const report = (m[2].match(/Full report:\s*`([^`]+)`/) || [null, null])[1];
  return { date: m[1], label, detail, report };
}

async function readDispatches(ROOT, slugs, addedAt, limit = 14) {
  const dir = path.join(ROOT, 'board/log');
  let names = [];
  try { names = (await fs.readdir(dir)).filter(n => /^\d{4}-\d\d-\d\d-.+\.md$/.test(n)); } catch { return []; }
  names.sort((a, b) => b.slice(0, 10).localeCompare(a.slice(0, 10)) ||
    (addedAt[`board/log/${b}`] || '').localeCompare(addedAt[`board/log/${a}`] || ''));
  const out = [];
  for (const name of names.slice(0, limit)) {
    const md = await fs.readFile(path.join(dir, name), 'utf8').catch(() => '');
    const h1 = (md.match(/^#\s+(.+)$/m) || [null, name])[1];
    const title = stripMd(h1).replace(/^\d{4}-\d\d-\d\d\s*[–—-]\s*/, '');
    let lede = '';
    for (const para of md.split(/\n\s*\n/)) {
      const t = para.trim();
      if (!t || /^#/.test(t) || /^---$/.test(t) || /^(from|type|problems):/m.test(t) ||
          /^\*\*(Posted by|Audience|Sources?):?\*\*/.test(t) || /^\*\*[^*]+\*\*\.?$/.test(t)) continue;
      lede = stripMd(t.replace(/\s+/g, ' ')).replace(/^\*|\*$/g, '');
      break;
    }
    const listed = ((md.match(/^problems:\s*(.+)$/m) || [null, ''])[1]).split(/[;,]\s*/).map(s => s.trim());
    const mentions = [...new Set(slugs.filter(s =>
      md.includes(s + '/') || md.includes(s + '`') || listed.includes(s.split('/')[1])))];
    const roleHint = /orchestrator/i.test(md.slice(0, 400)) ? 'orchestrator'
      : /finder/i.test(md.slice(0, 400)) ? 'finder'
      : /validator/i.test(md.slice(0, 400)) ? 'validator'
      : /cracker|session/i.test(md.slice(0, 400)) ? 'cracker' : 'other';
    out.push({
      date: name.slice(0, 10), file: `board/log/${name}`, title,
      lede: lede.length > 280 ? lede.slice(0, 277).replace(/\s+\S*$/, '') + '…' : lede,
      problems: mentions.slice(0, 5), role: roleHint, addedAt: addedAt[`board/log/${name}`] || null,
    });
  }
  return out;
}

async function readActiveClaims(ROOT) {
  const dir = path.join(ROOT, 'board/active');
  let names = [];
  try { names = (await fs.readdir(dir)).filter(n => !n.startsWith('.')); } catch { return []; }
  const out = [];
  for (const name of names) {
    const md = await fs.readFile(path.join(dir, name), 'utf8').catch(() => '');
    out.push({ file: `board/active/${name}`, problem: name.replace(/\.md$/, ''), excerpt: stripMd(md.slice(0, 240)) });
  }
  return out;
}

// Cadence mirrors board/SCHEDULE.md. The routine prompts live outside the repo,
// so this table is the only machine-readable copy; update both together.
export const ROUTINES = [
  { key: 'orchestrator', label: 'Orchestrator', cadence: 'daily 10:00 UTC', rule: { hours: [10], minute: 0 } },
  { key: 'cracker', label: 'Cracker', cadence: 'every 6h at :32 UTC', rule: { hours: [0, 6, 12, 18], minute: 32 } },
  { key: 'finder', label: 'Finder', cadence: 'Tue & Fri 13:00 UTC', rule: { hours: [13], minute: 0, weekdays: [2, 5] } },
];

// Each role's standing orders, quoted from its own file, and its pinned model
// from board/SCHEDULE.md. Nothing here is written by the site.
async function readRoleProfiles(ROOT) {
  const out = {};
  const sched = await fs.readFile(path.join(ROOT, 'board/SCHEDULE.md'), 'utf8').catch(() => '');
  const models = {};
  for (const cells of tableRows(sectionOf(sched, 'Models'))) {
    const m = cells[0].match(/Hub (\w+)/);
    if (m) models[m[1].toLowerCase()] = stripMd(cells[1]);
  }
  for (const key of ['cracker', 'validator', 'orchestrator', 'finder']) {
    const md = await fs.readFile(path.join(ROOT, `_roles/${key.toUpperCase()}.md`), 'utf8').catch(() => '');
    const para = md.split(/\n\s*\n/).map(x => x.trim()).find(x => x && !x.startsWith('#')) || '';
    const flat = stripMd(para.replace(/\s+/g, ' '));
    const sentences = flat.match(/[^.!?]+[.!?]+/g) || [flat];
    const two = sentences.slice(0, 2).join(' ').replace(/\s+/g, ' ').trim();
    out[key] = { creed: two.length > 170 ? sentences[0].replace(/\s+/g, ' ').trim() : two, model: models[key] || null, file: `_roles/${key.toUpperCase()}.md` };
  }
  return out;
}

export async function derive({ ROOT, statusText, problems, activity, domains }) {
  const history = historyInfo(ROOT);
  const log = readGitLog(ROOT, 120);
  const bySha = Object.fromEntries(log.map(c => [c.sha, c]));

  // First time each path appeared in the window, for dispatch ordering.
  const addedAt = {};
  for (const c of log) for (const f of c.files) if (!addedAt[f] || c.date < addedAt[f]) addedAt[f] = c.date;

  const domainKeys = domains.map(d => d.key);
  const rows = parseStatusRows(statusText, domainKeys);
  const queue = parseValidationQueue(statusText);
  const claimBySlug = {};
  for (const q of queue) {
    const slug = matchClaim(q, rows);
    q.slug = slug;
    q.since = firstDate(q.disposition);
    if (slug) claimBySlug[slug] = q;
  }

  // Per-problem 90-day commit dates from the same log (one git call, not 65).
  const now = Date.now();
  const touches = {};
  for (const c of log) {
    const age = now - new Date(c.date).getTime();
    const slugs = new Set(c.files.map(f => f.match(PROBLEM_PATH)).filter(Boolean).map(m => `${m[1]}/${m[2]}`));
    const role = roleOf(c.subject, c.files);
    for (const s of slugs) (touches[s] ||= []).push({ date: c.date, age, role, unit: c.unit });
  }

  for (const p of problems) {
    const row = rows[p.slug] || null;
    const claim = claimBySlug[p.slug] || null;
    p.isStub = !!p.files.hasMoved;
    p.shortTitle = row?.name || p.title;
    p.statusRow = row ? { status: row.status, notes: row.notes, suggestedDomain: row.suggestedDomain } : null;
    p.claim = claim ? { claim: claim.claim, disposition: claim.disposition, missingCheck: claim.missingCheck, since: claim.since } : null;
    p.stage = stageOf(p, row, claim);
    const t = touches[p.slug] || [];
    p.commitDates90d = t.filter(x => x.age < 90 * DAY).map(x => x.date);
    p.firstTouch = t.length ? t[t.length - 1].date : null;
    p.roleTouches = {};
    for (const x of t) {
      const k = x.unit === 'irregular' && x.role !== 'merge' && x.role !== 'infra' ? 'irregular' : x.role;
      if (k === 'merge' || k === 'infra' || k === 'other') continue;
      p.roleTouches[k] = (p.roleTouches[k] || 0) + 1;
    }
  }

  for (const a of activity) {
    // collectActivity records abbreviated SHAs (%h); match on prefix.
    const c = bySha[a.sha] || log.find(x => x.sha.startsWith(a.sha)) || null;
    const files = c?.files || [];
    a.role = roleOf(a.subject, files);
    a.problems = [...new Set(files.map(f => f.match(PROBLEM_PATH)).filter(Boolean).map(m => `${m[1]}/${m[2]}`))].slice(0, 6);
    a.fileCount = files.length;
    a.unit = c?.unit || null;
  }

  // Board-wide daily pulse by role. Window: repo lifetime, clamped to 14–90 days.
  const firstMs = history.since ? new Date(history.since).getTime() : now - 30 * DAY;
  const spanDays = Math.max(14, Math.min(90, Math.ceil((now - firstMs) / DAY) + 1));
  const start = new Date(now - (spanDays - 1) * DAY); start.setUTCHours(0, 0, 0, 0);
  const pulse = Array.from({ length: spanDays }, (_, i) => ({
    date: new Date(start.getTime() + i * DAY).toISOString().slice(0, 10),
    orchestrator: 0, validator: 0, cracker: 0, finder: 0, other: 0, irregular: 0,
  }));
  const pulseIdx = Object.fromEntries(pulse.map((d, i) => [d.date, i]));
  for (const c of log) {
    const role = roleOf(c.subject, c.files);
    if (role === 'merge' || role === 'infra') continue;
    const i = pulseIdx[new Date(c.date).toISOString().slice(0, 10)];
    if (i === undefined) continue;
    pulse[i][role === 'other' ? 'other' : role] += 1;
    if (c.unit === 'irregular') pulse[i].irregular += 1;
  }

  const lastByRole = {};
  const problemsOf = c => [...new Set(c.files.map(f => f.match(PROBLEM_PATH)).filter(Boolean).map(m => `${m[1]}/${m[2]}`))].slice(0, 4);
  for (const c of log) {
    const r = roleOf(c.subject, c.files);
    if (!lastByRole[r]) lastByRole[r] = { date: c.date, subject: c.subject.slice(0, 140), sha: c.sha, problems: problemsOf(c) };
    if (c.unit === 'irregular' && !['merge', 'infra', 'other'].includes(r) && !lastByRole.irregular) {
      lastByRole.irregular = { date: c.date, subject: c.subject.slice(0, 140), sha: c.sha, problems: problemsOf(c) };
    }
  }

  const live = problems.filter(p => !p.isStub);
  const byStage = {};
  for (const p of live) byStage[p.stage] = (byStage[p.stage] || 0) + 1;
  const weekAgo = now - 7 * DAY;
  const research7d = log.filter(c => new Date(c.date).getTime() > weekAgo &&
    c.files.some(f => PROBLEM_PATH.test(f))).length;

  // Verdict sets in build.mjs vs the STATUS table — logged for a human, not acted on.
  const legacyHeld = problems.filter(p => p.verdict === '3×PARTIAL').map(p => p.slug).sort();
  const tableHeld = Object.entries(rows).filter(([, r]) => /\bHELD\b/.test(r.status)).map(([s]) => s).sort();
  if (legacyHeld.join() !== tableHeld.join()) {
    console.warn(`[build] HELD_PARTIAL disagrees with STATUS.md: set=${legacyHeld.join(',')} table=${tableHeld.join(',')}`);
  }

  return {
    history,
    statusUpdated: parseLastUpdated(statusText),
    validationQueue: queue,
    dispatches: await readDispatches(ROOT, problems.filter(p => !p.isStub).map(p => p.slug), addedAt),
    activeClaims: await readActiveClaims(ROOT),
    routines: ROUTINES,
    roleProfiles: await readRoleProfiles(ROOT),
    pulse,
    lastByRole,
    totalsExtra: { live: live.length, stubs: problems.length - live.length, byStage, research7d },
  };
}
