"""How much of the survival is just the test running out of power?

97 periods were tested. Most 'surviving' periods survive because at that period
almost no two crib characters share a residue class, so there is nothing to
contradict. This computes the global expectation under the null and isolates the
periods where the test actually had teeth.
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
import k4, crib_constraints as cc

R = os.path.join(os.path.dirname(__file__), '..', 'results')


def main():
    res = json.load(open(os.path.join(R, 'crib_results.json')))
    rows = res['periods']
    obs = sum(1 for r in rows if r['survives_general'])
    exp = sum(r['null_survival_rate_general'] for r in rows)
    obs_v = sum(1 for r in rows if r['survives_vigenere'])
    exp_v = sum(r['null_survival_rate_vigenere'] for r in rows)

    powered = [r for r in rows if r['null_survival_rate_general'] < 0.10]
    powered_surv = [r for r in powered if r['survives_general']]
    powered_v = [r for r in rows if r['null_survival_rate_vigenere'] < 0.10]
    powered_v_surv = [r for r in powered_v if r['survives_vigenere']]

    out = {
        'general': {'observed_survivors': obs, 'expected_under_null': exp,
                    'powered_periods': [r['period'] for r in powered],
                    'powered_survivors': [r['period'] for r in powered_surv],
                    'expected_powered_survivors_under_null':
                        sum(r['null_survival_rate_general'] for r in powered)},
        'vigenere': {'observed_survivors': obs_v, 'expected_under_null': exp_v,
                     'powered_periods': [r['period'] for r in powered_v],
                     'powered_survivors': [r['period'] for r in powered_v_surv],
                     'expected_powered_survivors_under_null':
                         sum(r['null_survival_rate_vigenere'] for r in powered_v)},
    }

    d = k4.load()
    ct, known = d['ciphertext'], d['known']
    for p in out['general']['powered_survivors']:
        cls = {}
        for i, pt in sorted(known.items()):
            cls.setdefault(i % p, []).append((i, pt, ct[i]))
        out.setdefault('surviving_period_detail', {})[str(p)] = {
            str(r): [{'pos0': i, 'pt': pt, 'ct': c} for i, pt, c in v]
            for r, v in sorted(cls.items()) if len(v) > 1}

    with open(os.path.join(R, 'power_check.json'), 'w') as fh:
        json.dump(out, fh, indent=1)

    for name in ('general', 'vigenere'):
        o = out[name]
        print('%s:' % name)
        print('  survivors observed %d, expected under null %.1f' %
              (o['observed_survivors'], o['expected_under_null']))
        print('  periods where the test had power (null survival <10%%): %d -> %s'
              % (len(o['powered_periods']), o['powered_periods']))
        print('  of those, K4 survives: %s (expected under null %.2f)'
              % (o['powered_survivors'], o['expected_powered_survivors_under_null']))
        print()
    print('constraint detail for surviving powered periods:')
    print(json.dumps(out.get('surviving_period_detail', {}), indent=1)[:1200])


if __name__ == '__main__':
    main()
