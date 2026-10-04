"""TabPFN regression on 10 replicate 80/20 holdouts (same splits as rrblup_holdout.R).

Replicate i uses column cv_i of the CVFs file; lines in fold TEST_FOLD are the test set.
Markers are passed to TabPFN as-is (coded -1/0/1), with no tuning on the training set.

Usage: python tabpfn_holdout.py <species> [--reps N] [--traits HT ...] [--test-fold K]
"""

import argparse
import time
from pathlib import Path

import numpy as np
import pandas as pd
from tabpfn import TabPFNRegressor

DATA_DIR = Path(__file__).resolve().parent / "data"
OUT_DIR = Path(__file__).resolve().parent / "results"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("species")
    ap.add_argument("--reps", type=int, default=10)
    ap.add_argument("--traits", nargs="+", default=None)
    ap.add_argument("--test-fold", type=int, default=1)
    ap.add_argument("--tag", default="TabPFN")
    args = ap.parse_args()

    X = pd.read_csv(DATA_DIR / f"{args.species}_geno.csv", index_col=0)
    Y = pd.read_csv(DATA_DIR / f"{args.species}_pheno.csv", index_col=0)
    cvs = pd.read_csv(DATA_DIR / f"{args.species}_CVFs.csv", index_col=0)
    assert X.index.equals(Y.index) and X.index.equals(cvs.index)
    X = X.to_numpy(dtype=np.float32)
    traits = args.traits or list(Y.columns)

    OUT_DIR.mkdir(exist_ok=True)
    out_path = OUT_DIR / f"{args.species}_{args.tag}.csv"
    # Resume: keep finished fits and skip them
    rows = pd.read_csv(out_path).to_dict("records") if out_path.exists() else []
    done = {(r["trait"], r["rep"]) for r in rows}
    for trait in traits:
        y = Y[trait].to_numpy()
        for rep in range(1, args.reps + 1):
            if (trait, rep) in done:
                continue
            test =cvs[f"cv_{rep}"].to_numpy() == args.test_fold
            t0 = time.time()
            model = TabPFNRegressor(random_state=rep)
            model.fit(X[~test], y[~test])
            yhat = model.predict(X[test])
            secs = time.time() - t0
            r = np.corrcoef(y[test], yhat)[0, 1]
            rows.append(dict(species=args.species, trait=trait, rep=rep, model=args.tag,
                             n_train=int((~test).sum()), n_test=int(test.sum()),
                             r=r, seconds=secs))
            print(f"{args.species} {trait} rep{rep} r={r:.4f} ({secs:.1f}s)", flush=True)
            # Write after every fit so a crash keeps finished results
            pd.DataFrame(rows).to_csv(out_path, index=False)


if __name__ == "__main__":
    main()
