"""Which features carry the date signal, and which carry the author signal?

For each of the 500 features: R^2 of the z-scored feature regressed on year
(date-loading), and an author F-ratio computed on the *date residual*
(author signal that is not date). Printed sorted by date-loading.
"""
import numpy as np, collections, json, os
import shared

plays = shared.load()
y = np.array([p['author'] for p in plays])
yr = np.array([float(p['year']) for p in plays])
vocab = shared.vocabulary(plays)
X = shared.vectors(plays, vocab)
Z = (X - X.mean(0)) / np.where(X.std(0) == 0, 1, X.std(0))

# date-loading: R^2 of linear regression on year (centred)
t = (yr - yr.mean()) / yr.std()
beta = (Z * t[:, None]).sum(0) / (t ** 2).sum()
fit = beta[None, :] * t[:, None]
ss_tot = (Z ** 2).sum(0)
r2_date = 1 - ((Z - fit) ** 2).sum(0) / ss_tot

# author F on the date residual
R = Z - fit
authors = sorted(set(y))
grand = R.mean(0)
between = np.zeros(R.shape[1]); within = np.zeros(R.shape[1])
for a in authors:
    m = y == a
    ma = R[m].mean(0)
    between += m.sum() * (ma - grand) ** 2
    within += ((R[m] - ma) ** 2).sum(0)
F = (between / (len(authors) - 1)) / (within / (len(plays) - len(authors)))

order = np.argsort(-r2_date)
print('%-12s %8s %8s   %s' % ('word', 'R2_date', 'F_auth', 'slope'))
for i in order[:35]:
    print('%-12s %8.3f %8.2f   %+.2f' % (vocab[i], r2_date[i], F[i], beta[i]))
print('\n--- lowest date-loading, top author-F among them ---')
low = order[-150:]
for i in low[np.argsort(-F[low])][:20]:
    print('%-12s %8.3f %8.2f' % (vocab[i], r2_date[i], F[i]))
print('\nmean R2_date = %.3f ; total date variance share = %.3f'
      % (r2_date.mean(), r2_date.mean()))
json.dump({'vocab': vocab, 'r2_date': r2_date.tolist(), 'F_author_resid': F.tolist(),
           'slope': beta.tolist()},
          open(os.path.join(os.path.dirname(__file__), '..', 'results', 'date_loading.json'), 'w'), indent=1)
