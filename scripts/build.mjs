#!/usr/bin/env node
// Build the Hub site. Reads the repo, git history, and (if $GITHUB_TOKEN is set)
// live GitHub state, then emits dist/ with data.json inlined into index.html.

import { execSync } from 'node:child_process';
import { promises as fs } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { derive } from './derive.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const SRC = path.join(ROOT, 'src');
const DIST = path.join(ROOT, 'dist');

const DOMAINS = [
  { key: 'ciphers', label: 'Ciphers', accent: 'cyan' },
  { key: 'historical-texts', label: 'Undeciphered Texts', accent: 'purple' },
  { key: 'historical-controversies', label: 'Controversies', accent: 'orange' },
  { key: 'ireland', label: 'Ireland', accent: 'green' },
  { key: 'discovered', label: 'Discovered (Backlog)', accent: 'yellow' },
];

const OWNER = 'AlexFitzgerald47';
const REPO = 'cracking-problems-hub';

const sh = (cmd, opts = {}) => execSync(cmd, { encoding: 'utf8', cwd: ROOT, ...opts }).trim();

async function readFileSafe(p) {
  try { return await fs.readFile(p, 'utf8'); } catch { return null; }
}

async function listDir(p) {
  try { return await fs.readdir(p, { withFileTypes: true }); } catch { return []; }
}

function parseTitle(md, fallback) {
  if (!md) return fallback;
  const m = md.match(/^\s*#\s+(.+?)\s*$/m);
  return m ? m[1].replace(/[`*_]/g, '').trim() : fallback;
}

function parseLede(md) {
  if (!md) return '';
  // First non-heading, non-blank paragraph
  const lines = md.split('\n');
  let started = false;
  let buf = [];
  for (const line of lines) {
    if (/^#/.test(line)) { if (started) break; continue; }
    if (/^\s*$/.test(line)) { if (started) break; continue; }
    started = true;
    buf.push(line.trim());
    if (buf.join(' ').length > 260) break;
  }
  return buf.join(' ').replace(/\s+/g, ' ').slice(0, 260);
}

async function gitCommitsForPath(rel, days = 90) {
  try {
    const since = new Date(Date.now() - days * 86400_000).toISOString().slice(0, 10);
    const out = sh(`git log --since=${since} --pretty=format:%cI --no-renames -- ${JSON.stringify(rel)}`);
    return out ? out.split('\n').filter(Boolean) : [];
  } catch { return []; }
}

async function gitLastTouch(rel) {
  try {
    const out = sh(`git log -1 --pretty=format:%cI --no-renames -- ${JSON.stringify(rel)}`);
    return out || null;
  } catch { return null; }
}

async function gitLastSubject(rel) {
  try {
    const out = sh(`git log -1 --pretty=format:%s --no-renames -- ${JSON.stringify(rel)}`);
    return out || '';
  } catch { return ''; }
}

// Small allowlist of problems STATUS.md explicitly names as HELD 3×PARTIAL
// claims. This is versioned in code intentionally — STATUS.md's prose changes
// weekly and regex-parsing it produced too many false verdicts. When STATUS
// promotes another claim, update this list in the same commit.
const HELD_PARTIAL = new Set([
  'ennis-ogham-amber-bead',
  'mesha-stele-line31',
  'venona-brown-braun',
  'chinese-gold-bar-cipher',
]);

// Externally solved / withdrawn (not a live target any more).
const WITHDRAWN = new Set([
  'ormonde-maltravers-1634-cipher',
]);

// Crack-progress heuristic: 0-100. Purely from file signals + git activity.
// Not a truth claim — a visual index of motion. Curated verdicts (SOLVED /
// PASS / HELD) come from STATUS.md and are surfaced via the excerpt in the
// detail drawer, not by regex-scraping.
function computeCrackScore(problem) {
  let s = 0;
  const flags = problem.files;
  if (flags.hasProblem) s += 6;
  if (flags.hasProgress) s += 10;
  if (flags.hasHandover) s += 8;
  if (flags.hasSources) s += 4;
  if (flags.hasFreeze) s += 20;
  if (flags.hasResults) s += 20;
  if (flags.hasSolution) s += 25;
  if (flags.hasAnalysis) s += 5;
  if (flags.hasCode) s += 6;
  if (flags.hasData) s += 5;
  if (flags.hasAttempts) s += 5;
  if (problem.commits30d >= 5) s += 6;
  else if (problem.commits30d >= 2) s += 3;

  const id = problem.id;
  if (WITHDRAWN.has(id)) { problem.verdict = 'WITHDRAWN'; return Math.min(30, s); }
  if (HELD_PARTIAL.has(id)) { problem.verdict = '3×PARTIAL'; return Math.max(s, 78); }
  if (flags.hasSolution && flags.hasFreeze && flags.hasResults) { problem.verdict = 'SOLVE-CLAIMED'; return Math.max(s, 88); }
  if (flags.hasFreeze && flags.hasResults) { problem.verdict = 'FROZEN'; return Math.max(s, 72); }
  if (flags.hasFreeze) { problem.verdict = 'FROZEN'; return Math.max(s, 60); }
  if (flags.hasResults) { problem.verdict = 'RESULTS'; return Math.max(s, 62); }
  if (flags.hasHandover && problem.commits30d > 0) { problem.verdict = 'WORKING'; }
  return Math.min(100, Math.max(0, Math.round(s)));
}

function extractContextAround(text, id, span) {
  if (!text || !id) return '';
  const rx = new RegExp('`' + id + '`');
  const m = rx.exec(text);
  if (!m) return '';
  const i = m.index;
  return text.slice(Math.max(0, i - span), Math.min(text.length, i + span));
}

function stateFromScore(problem) {
  const v = problem.verdict;
  if (v === 'SOLVED') return 'solved';
  if (v === 'SOLVE-CLAIMED') return 'validated';
  if (v === 'WITHDRAWN') return 'withdrawn';
  if (v === '3×PARTIAL' || v === 'PARTIAL' || v === 'HELD') return 'held';
  if (v === 'FROZEN' || v === 'RESULTS') return 'frozen';
  if (problem.commits30d > 0) return 'active';
  if (problem.domain === 'discovered') return 'proposed';
  return 'quiet';
}

async function scanProblem(domain, id, statusText) {
  const rel = `${domain}/${id}`;
  const abs = path.join(ROOT, rel);
  const entries = await listDir(abs);
  if (!entries.length) return null;
  const names = new Set(entries.map(e => e.name));

  const problemMd = await readFileSafe(path.join(abs, 'PROBLEM.md'));
  const files = {
    hasProblem: names.has('PROBLEM.md'),
    hasProgress: names.has('PROGRESS.md'),
    hasHandover: names.has('HANDOVER.md'),
    hasSources: names.has('SOURCES.md'),
    hasFreeze: names.has('FREEZE.md') || names.has('FREEZE'),
    hasResults: names.has('RESULTS.md'),
    hasSolution: names.has('SOLUTION.md'),
    hasClaim: names.has('CLAIM.md'),
    hasMoved: names.has('MOVED.md'),
    hasAnalysis: entries.some(e => e.isDirectory() && /^(analysis|analyses)$/i.test(e.name)),
    hasCode: entries.some(e => e.isDirectory() && /^(code|src|scripts)$/i.test(e.name)),
    hasData: entries.some(e => e.isDirectory() && /^(data|corpus|corpora)$/i.test(e.name)),
    hasAttempts: entries.some(e => e.isDirectory() && /^attempts?$/i.test(e.name)),
  };

  const commits30 = await gitCommitsForPath(rel, 30);
  const commits90 = await gitCommitsForPath(rel, 90);
  const lastTouch = await gitLastTouch(rel);
  const lastSubject = await gitLastSubject(rel);

  const problem = {
    id,
    domain,
    slug: `${domain}/${id}`,
    title: parseTitle(problemMd, id.replace(/-/g, ' ')),
    lede: parseLede(problemMd),
    files,
    commits30d: commits30.length,
    commits90d: commits90.length,
    commitDates30d: commits30,
    lastTouch,
    lastSubject: lastSubject.slice(0, 140),
    verdict: null,
    contextExcerpt: '',
  };
  // A discovered/ folder with a MOVED.md is a stub pointing at the promoted
  // copy elsewhere. It must not inherit the promoted problem's STATUS verdict
  // or the frontier fills up with pointers.
  if (files.hasMoved) {
    problem.verdict = 'PROMOTED';
    problem.state = 'proposed';
    problem.crackScore = 8;
    return problem;
  }

  problem.crackScore = computeCrackScore(problem);
  problem.state = stateFromScore(problem);
  problem.contextExcerpt = extractContextAround(statusText, id, 260);
  return problem;
}

async function collectProblems(statusText) {
  const out = [];
  for (const d of DOMAINS) {
    const entries = await listDir(path.join(ROOT, d.key));
    for (const e of entries) {
      if (!e.isDirectory()) continue;
      if (e.name.startsWith('_') || e.name.startsWith('.')) continue;
      const p = await scanProblem(d.key, e.name, statusText);
      if (p) out.push(p);
    }
  }
  return out;
}

// Recent orchestrator/cracker/finder commits by parsing subjects
async function collectActivity() {
  try {
    const out = sh(`git log --since=60.days.ago --pretty=format:%cI%x1f%h%x1f%s --no-renames`);
    const lines = out.split('\n').filter(Boolean).map(row => {
      const [date, sha, subject] = row.split('\x1f');
      let kind = 'commit';
      const s = subject.toLowerCase();
      if (s.startsWith('orchestrator')) kind = 'orchestrator';
      else if (s.startsWith('cracker') || / crack | claim /.test(' ' + s + ' ')) kind = 'cracker';
      else if (s.startsWith('finder') || / discovery /.test(' ' + s + ' ')) kind = 'finder';
      else if (s.startsWith('merge')) kind = 'merge';
      return { date, sha, subject, kind };
    });
    return lines.slice(0, 400);
  } catch { return []; }
}

async function fetchGithubPRs() {
  const token = process.env.GITHUB_TOKEN;
  const url = `https://api.github.com/repos/${OWNER}/${REPO}/pulls?state=all&per_page=30&sort=updated&direction=desc`;
  try {
    const res = await fetch(url, {
      headers: {
        'Accept': 'application/vnd.github+json',
        'User-Agent': 'cracking-problems-hub-build',
        ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
      },
    });
    if (!res.ok) return [];
    const arr = await res.json();
    return arr.map(pr => ({
      number: pr.number,
      title: pr.title,
      state: pr.merged_at ? 'merged' : pr.state,
      url: pr.html_url,
      user: pr.user?.login,
      created: pr.created_at,
      updated: pr.updated_at,
      merged: pr.merged_at,
      draft: pr.draft,
    }));
  } catch { return []; }
}

async function fetchGithubBranches() {
  const token = process.env.GITHUB_TOKEN;
  const url = `https://api.github.com/repos/${OWNER}/${REPO}/branches?per_page=100`;
  try {
    const res = await fetch(url, {
      headers: {
        'Accept': 'application/vnd.github+json',
        'User-Agent': 'cracking-problems-hub-build',
        ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
      },
    });
    if (!res.ok) return [];
    const arr = await res.json();
    return arr.map(b => ({ name: b.name, sha: b.commit?.sha })).filter(b => b.name !== 'main');
  } catch { return []; }
}

async function copyStatic() {
  await fs.mkdir(DIST, { recursive: true });
  for (const f of ['style.css', 'app.js']) {
    await fs.copyFile(path.join(SRC, f), path.join(DIST, f));
  }
}

async function buildHtml(data) {
  const template = await fs.readFile(path.join(SRC, 'index.html'), 'utf8');
  const injected = template.replace(
    '<!--DATA-->',
    `<script id="hub-data" type="application/json">${JSON.stringify(data).replace(/</g, '\\u003c')}</script>`
  );
  await fs.writeFile(path.join(DIST, 'index.html'), injected);
}

async function main() {
  console.log('[build] scanning repo…');
  const statusText = (await readFileSafe(path.join(ROOT, 'STATUS.md'))) || '';
  const targetsText = (await readFileSafe(path.join(ROOT, 'board/TARGETS.md'))) || '';
  const problems = await collectProblems(statusText);
  const activity = await collectActivity();
  const [prs, branches] = await Promise.all([fetchGithubPRs(), fetchGithubBranches()]);

  const headSha = (() => { try { return sh('git rev-parse HEAD'); } catch { return null; } })();
  const branch = (() => { try { return sh('git rev-parse --abbrev-ref HEAD'); } catch { return null; } })();

  const totals = {
    problems: problems.length,
    active: problems.filter(p => p.state === 'active').length,
    frozen: problems.filter(p => p.state === 'frozen').length,
    held: problems.filter(p => p.state === 'held').length,
    validated: problems.filter(p => p.state === 'validated' || p.state === 'solved').length,
    withdrawn: problems.filter(p => p.state === 'withdrawn').length,
    closed: problems.filter(p => p.state === 'closed').length,
    quiet: problems.filter(p => p.state === 'quiet').length,
    proposed: problems.filter(p => p.state === 'proposed').length,
  };

  const extra = await derive({ ROOT, statusText, problems, activity, domains: DOMAINS });
  Object.assign(totals, extra.totalsExtra);

  const data = {
    generatedAt: new Date().toISOString(),
    repo: { owner: OWNER, name: REPO, branch, headSha, url: `https://github.com/${OWNER}/${REPO}` },
    domains: DOMAINS,
    problems,
    activity,
    prs,
    branches,
    totals,
    statusHead: statusText.split('\n').slice(0, 40).join('\n'),
    targetsHead: targetsText.split('\n').slice(0, 12).join('\n'),
    history: extra.history,
    statusUpdated: extra.statusUpdated,
    validationQueue: extra.validationQueue,
    dispatches: extra.dispatches,
    activeClaims: extra.activeClaims,
    routines: extra.routines,
    pulse: extra.pulse,
    lastByRole: extra.lastByRole,
  };

  await copyStatic();
  await buildHtml(data);
  await fs.writeFile(path.join(DIST, 'data.json'), JSON.stringify(data, null, 2));
  console.log(`[build] wrote dist/ — ${problems.length} problems, ${activity.length} activity rows, ${prs.length} PRs`);
}

main().catch(err => { console.error(err); process.exit(1); });
