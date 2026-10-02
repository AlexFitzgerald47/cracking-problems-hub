import json, re, os
HERE=os.path.dirname(os.path.abspath(__file__))
def load(path=None):
    path = path or os.path.join(HERE,'data','LinearAInscriptions.js')
    s=open(path,encoding='utf-8').read()
    start = s.index('new Map(') + len('new Map(')
    end = s.index(']);', start) + 1
    body = s[start:end]
    body = re.sub(r',(\s*[\]\}])', r'\1', body)
    body = re.sub(r'\\u\{([0-9a-fA-F]+)\}', lambda m: chr(int(m.group(1),16)), body)
    return dict(json.loads(body))
