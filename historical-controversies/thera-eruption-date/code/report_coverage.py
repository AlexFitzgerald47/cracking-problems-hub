import json, sys, numpy as np
d = json.load(open('data/coverage_sim.json'))
for name, blk in d.items():
    print('\n=== design %s  (n=%d determinations, real 1-sigma errors, %d replicates each)'
          % (name, blk['n'], blk['nrep']))
    print(' true T | recovered median  | bias  | coverage of the nominal')
    print('  (BCE) |   mean      sd    | (yr)  |  68.3%    95.4%')
    for r in blk['rows']:
        print('  %5d | %7.1f  %6.1f   | %+5.1f |  %.3f    %.3f' %
              (r['T'], r['med_mean'], r['med_sd'], r['med_mean'] - r['T'],
               r['cov68'], r['cov95']))
    c68 = np.array([r['cov68'] for r in blk['rows']])
    c95 = np.array([r['cov95'] for r in blk['rows']])
    T = np.array([r['T'] for r in blk['rows']])
    inplat = (T <= 1610) & (T >= 1540)
    print('  nominal 68.3%%: mean actual coverage %.3f overall, %.3f inside the '
          '1610-1540 plateau, range [%.3f, %.3f]'
          % (c68.mean(), c68[inplat].mean(), c68.min(), c68.max()))
    print('  nominal 95.4%%: mean actual coverage %.3f overall, %.3f inside the '
          'plateau, range [%.3f, %.3f]'
          % (c95.mean(), c95[inplat].mean(), c95.min(), c95.max()))
    # calibrated likelihood: invert the sampling distribution of the median
    print('\n  Bias-corrected inference. For each assumed true year, the sampling')
    print('  distribution of the recovered posterior median is known from the')
    print('  simulation; evaluating it at the value the REAL data gave turns the')
    print('  observed median into a likelihood for T.')
    obs = {'b_akrotiri_vdl': 1592, 'a_non_thera': 1575}[name]
    ll = []
    for r in blk['rows']:
        m = np.array(r['meds'])
        # kernel density of the simulated medians at the observed value
        h = 1.06 * m.std() * len(m) ** -0.2
        dens = np.exp(-0.5 * ((obs - m) / h) ** 2).mean() / h
        ll.append((r['T'], dens))
    tot = sum(x[1] for x in ll)
    print('  observed median for this design = %d BCE' % obs)
    print('   T     relative support')
    cum = 0
    srt = sorted(ll, key=lambda x: -x[1])
    keep = set()
    for T_, dd in srt:
        cum += dd / tot; keep.add(T_)
        if cum >= 0.954:
            break
    for T_, dd in ll:
        bar = '#' * int(round(30 * dd / max(x[1] for x in ll)))
        print('  %5d  %6.3f %s %s' % (T_, dd / tot, bar, '<- in 95.4% support set' if T_ in keep else ''))
