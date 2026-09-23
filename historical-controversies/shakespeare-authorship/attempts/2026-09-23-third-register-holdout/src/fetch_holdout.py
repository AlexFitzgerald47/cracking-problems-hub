"""Fetch the holdout candidates' TCP XML into the same cache the 2026-09-17 build uses."""
import os, sys, time, subprocess
import concurrent.futures as cf
import pool

DIR = os.environ.get('TCP_XML_DIR', '/tmp/w/xml')
RAW = 'https://raw.githubusercontent.com/textcreationpartnership/%s/master/%s.xml'


def get(tcp_id):
    p = os.path.join(DIR, tcp_id + '.xml')
    if os.path.exists(p) and os.path.getsize(p) > 2000:
        return tcp_id, 'cached'
    for attempt in range(4):
        r = subprocess.run(['curl', '-sSL', '--max-time', '120', '-o', p,
                            RAW % (tcp_id, tcp_id)], capture_output=True)
        if r.returncode == 0 and os.path.exists(p) and os.path.getsize(p) > 2000:
            return tcp_id, 'ok'
        time.sleep(2 ** attempt)
    return tcp_id, 'FAIL'


def main():
    canon, want = pool.pool()
    ids = sorted(set(r['TCP'] for a, rs in want.items() if a not in pool.HAS_ND for r in rs))
    print('fetching %d holdout TCP texts' % len(ids))
    with cf.ThreadPoolExecutor(8) as ex:
        res = list(ex.map(get, ids))
    bad = [r[0] for r in res if r[1] == 'FAIL']
    print('done: %d ok/cached, %d failed' % (len(res) - len(bad), len(bad)))
    for b in bad:
        print('  FAIL', b)


if __name__ == '__main__':
    main()
