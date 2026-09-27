#!/usr/bin/env bash
# Cloud-environment setup script for Cracking Problems Hub sessions.
#
# Paste into the environment's "Setup script" field (claude.ai/code -> environment
# selector -> edit -> Setup script). It runs once before Claude starts.
#
# Two jobs: install what the astronomical work needs, and *probe* what the
# session can actually reach, so the agent starts knowing its own constraints
# instead of discovering them an hour in. Never fails the session -- every
# optional step is allowed to fail and is reported.

set -u

REPO="${CLAUDE_PROJECT_DIR:-$(pwd)}"
VENV="$REPO/.venv"
REPORT="$REPO/.session-environment.md"

log() { echo "[setup] $*"; }

# --- Python toolchain ------------------------------------------------------
# pymeeus is the analytic Sun/Moon theory; numpy is only needed to regenerate
# the Delta-T table. Both come from PyPI, which is reachable at every network
# access level because it does not go through the session allowlist.
if [ ! -d "$VENV" ]; then
  python3 -m venv "$VENV" 2>/dev/null && log "created venv at $VENV"
fi
"$VENV/bin/pip" install -q --upgrade pip >/dev/null 2>&1
"$VENV/bin/pip" install -q pymeeus numpy >/dev/null 2>&1 \
  && log "installed pymeeus, numpy" || log "WARNING: pip install failed"

# --- Reference data on GitHub ---------------------------------------------
# Delta-T spline of Stephenson, Morrison & Hohenkerk (2016). GitHub reads work
# through the session's git proxy independently of the network access level.
if [ ! -d "$REPO/../ytliu0/deltat/.git" ] && [ ! -d "$HOME/ytliu0/deltat/.git" ]; then
  GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 -q \
    https://github.com/ytliu0/deltat "$HOME/ytliu0/deltat" 2>/dev/null \
    && log "cloned ytliu0/deltat" || log "note: could not clone ytliu0/deltat"
fi

# --- Probe what this session can actually reach ---------------------------
probe() {
  local host="$1"
  local code
  code=$(curl -sS -o /dev/null -w '%{http_code}' --max-time 12 "https://$host/" 2>/dev/null)
  if [ "$code" = "000" ] || [ -z "$code" ]; then echo "BLOCKED"; else echo "ok ($code)"; fi
}

{
  echo "# Session environment probe"
  echo
  echo "Written by \`bootstrap/setup.sh\` at container start. **Read this before"
  echo "planning work** -- it tells you which problems on this board you can"
  echo "actually start."
  echo
  echo "| Host | Reachable | What it gates |"
  echo "|------|-----------|---------------|"
  printf '| pypi.org | %s | python packages (always reachable) |\n'            "$(probe pypi.org)"
  printf '| raw.githubusercontent.com | %s | corpora hosted on GitHub |\n'      "$(probe raw.githubusercontent.com)"
  printf '| celt.ucc.ie | %s | **the Irish annals, and most of `historical-texts/`** |\n' "$(probe celt.ucc.ie)"
  printf '| archive.org | %s | Hennessy AU 1887, public-domain editions |\n'    "$(probe archive.org)"
  printf '| 1641.tcd.ie | %s | `discovered/1641-depositions-quantitative/` |\n' "$(probe 1641.tcd.ie)"
  printf '| downsurvey.tcd.ie | %s | `discovered/cromwellian-transplantation-compliance/` |\n' "$(probe downsurvey.tcd.ie)"
  printf '| registers.nli.ie | %s | `discovered/famine-parish-register-mortality/` |\n' "$(probe registers.nli.ie)"
  printf '| militaryarchives.ie | %s | `discovered/bmh-mspc-divergence/` |\n'   "$(probe militaryarchives.ie)"
  printf '| en.wikipedia.org | %s | general verification |\n'                   "$(probe en.wikipedia.org)"
  echo
  echo "Python: \`$VENV/bin/python\` (pymeeus, numpy installed)."
  echo
  echo "If the archive hosts are BLOCKED, do not plan a corpus problem. Pick work"
  echo "whose evidence is *computable* rather than downloadable, or build a corpus"
  echo "from what is reachable. See \`board/log/2026-09-05-egress-blocked-corpora.md\`."
} > "$REPORT"

log "wrote $REPORT"
cat "$REPORT"
