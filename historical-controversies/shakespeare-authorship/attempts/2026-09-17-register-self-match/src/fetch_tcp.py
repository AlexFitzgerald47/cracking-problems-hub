"""Fetches the EEBO-TCP catalogue and every XML file this attempt needs.

Each EEBO-TCP text is its own GitHub repository under the textcreationpartnership
organisation, so a text is one raw file fetch. The catalogue TCP.csv (29 MB,
61,315 rows) carries author, date, title and free/restricted status.

    python fetch_tcp.py            # ~2 minutes, ~100 MB into $TCP_XML_DIR
"""
import os, re, csv, json, subprocess, sys, time
import concurrent.futures as cf

DIR = os.environ.get('TCP_XML_DIR', '/tmp/w/xml')
CAT = os.path.join(os.path.dirname(DIR.rstrip('/')), 'TCP.csv')
RAW = 'https://raw.githubusercontent.com/textcreationpartnership/%s/master/%s.xml'
CATALOGUE = 'https://raw.githubusercontent.com/textcreationpartnership/Texts/master/TCP.csv'

AUTHORS = [
    'Jonson, Ben, 1573?-1637.', 'Chapman, George, 1559?-1634.',
    'Dekker, Thomas, ca. 1572-1632.', 'Greene, Robert, 1558?-1592.',
    'Lyly, John, 1554?-1606.', 'Middleton, Thomas, d. 1627.',
    'Marston, John, 1575?-1634.', 'Heywood, Thomas, d. 1641.',
]


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
    os.makedirs(DIR, exist_ok=True)
    if not os.path.exists(CAT):
        print('fetching catalogue ...')
        subprocess.run(['curl', '-sSL', '--max-time', '600', '-o', CAT, CATALOGUE], check=True)
    rows = list(csv.DictReader(open(CAT, encoding='utf-8', errors='replace')))
    want = set(r['TCP'] for r in rows if r['Author'] in AUTHORS and r['Status'] == 'Free')
    want.add('A04632')                       # the 1616 Jonson folio Workes
    idx = open('/home/user/dracor-org/engdracor/index.xml').read()
    # engdracor `sourceid` attributes ARE TCP ids; suffixed ones (A04632_07) are
    # engdracor's own split of a multi-play volume and have no separate TCP file.
    want |= set(i for i in re.findall(r'sourceid="([^"]+)"', idx) if '_' not in i)
    print('fetching %d TCP texts into %s' % (len(want), DIR))
    with cf.ThreadPoolExecutor(8) as ex:
        res = list(ex.map(get, sorted(want)))
    bad = [r for r in res if r[1] == 'FAIL']
    print('done: %d ok, %d failed' % (len(res) - len(bad), len(bad)))
    for b in bad:
        print('  FAIL', b[0])


if __name__ == '__main__':
    main()
