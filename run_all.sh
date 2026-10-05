#!/usr/bin/env bash
# Run every analysis: 3 traits x 10 replicate 80/20 holdouts per species and setting,
# then build the summary tables and figure.
# Each script saves after every fit and skips finished fits, so rerunning resumes.
#
# Usage: ./run_all.sh [tabpfn|rrblup|summary|all]   (default: all)
set -euo pipefail
cd "$(dirname "$0")"
what="${1:-all}"
LARGE="rice sorghum maize switchgrass"   # more markers than TabPFN-3.5's 20,000-feature limit

if [[ "$what" == tabpfn || "$what" == all ]]; then
  # Raw markers where they fit (soy 4,234; spruce 6,930)
  for sp in soy spruce; do python tabpfn_holdout.py "$sp" --features raw; done
  # Spruce again with enough ensemble members to cover every marker
  python tabpfn_holdout.py spruce --features raw --n-estimators cover
  # PCA of the markers, all species (comparison)
  for sp in soy spruce $LARGE; do python tabpfn_holdout.py "$sp" --features pca; done
  # Large species: markers thinned to 20,000 evenly along the genome
  for sp in $LARGE; do python tabpfn_holdout.py "$sp" --features thin --n-estimators cover; done
  # Large species, main run: 100 PCs given to every ensemble member + 19,900 thinned markers
  for sp in $LARGE; do
    python tabpfn_holdout.py "$sp" --features hybrid --n-pcs 100 --n-estimators cover
  done
fi

if [[ "$what" == rrblup || "$what" == all ]]; then
  # rrBLUP on the same splits as TabPFN, to check our splits against the published results
  for sp in soy spruce; do Rscript rrblup_holdout.R "$sp" 10 1; done
fi

if [[ "$what" == summary || "$what" == all ]]; then
  python summarize_results.py
  python make_figures.py
fi
