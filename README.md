# Tabular genomic prediction with TabPFN-3.5

**TL;DR:** We fed genetic marker data straight into TabPFN-3.5, with no tuning and no
genetics-specific modeling, and tested it against 18 established genomic prediction methods on a
standard published benchmark (6 crop and tree species, 18 traits). **TabPFN was the most accurate
method on 11 of the 18 tests and had the best median rank among all methods**,
beating models built specifically for genomic prediction. Wherever the data fit
within TabPFN-3.5's 20,000-feature limit, it won every time. In breeding, the rate of genetic
improvement rises in proportion to prediction accuracy, so even gains of a few percent compound
into substantial value across a breeding program. These are gains TabPFN could deliver in
breeding programs today.

*An entry to the Prior Labs TabPFN-3.5 Hackathon (2026).*

## Genomic Prediction

**Genomic prediction** is widely used in modern plant and animal breeding to predict an individual's phenotypic performance (traits like yield, disease resistance, growth rate, milk production, or meat quality) from its genetic markers (DNA sequence information). A model is trained on individuals with both genotype and phenotype data, then used to predict the performance of new individuals from genotype alone.

Genomic prediction is valuable because genotyping is extremely fast and inexpensive relative to phenotyping. Breeders can screen thousands or millions of individuals genetically and select the most promising ones without collecting expensive phenotypes, enabling earlier identification of elite individuals and accelerating breeding progress.

Genomic prediction has been used for roughly 20 years and is now foundational to breeding programs in maize, soybean, wheat, cattle, pigs, chickens, and many other crops and livestock we all depend on. It underpins breeding industries worth billions of dollars, with genomic prediction in U.S. dairy cattle alone estimated to have returned about $4 billion since its adoption in 2009 ([Rexroad et al. 2019](https://doi.org/10.3389/fgene.2019.00327)). Because genetic gains accumulate across generations, even modest improvements in selection accuracy can translate into substantial additional economic gains over the course of a breeding program. This makes genomic prediction an especially valuable target for developing better prediction methods.

### Why TabPFN and why now?

A typical genomic prediction dataset consists of an $N \times M$ matrix of genetic markers ($N$ individuals, $M$ markers) and an $N \times P$ matrix of phenotypic measurements, potentially accompanied by covariates. In this formulation it is a **supervised learning problem**. Individuals with known genotypes and phenotypes are used to learn a mapping from genotype to phenotype, and subsequently predict phenotypes from individuals with only genotype data.

Numerous specialized methods exist for genomic prediction, including mixed models, Bayesian models, kernel methods, and machine learning approaches. Most are designed around genetic relationships, marker effects, or assumptions about how genetic variation affects phenotypes rather than treating the problem as generic tabular learning. [The Bitter Lesson](http://www.incompleteideas.net/IncIdeas/BitterLesson.html) suggests that there should be value in taking the opposite approach: abandon domain-specific assumptions and let compute and increasingly capable general-purpose learning systems do the heavy lifting.

Here we take that Bitter Lesson approach. **We treat genomic prediction as a tabular regression problem and feed raw genetic marker data straight into TabPFN-3.5**, with minimal human curation of markers, no assumptions about how genes affect traits, and no tuning. TabPFN has appeared in genomic prediction before, but only as a component of a larger ensemble trained on a curated set of genetic markers ([TRXB, 2025](https://link.springer.com/article/10.1007/s44412-025-00005-3)). We go the other way. As Sutton puts it, "we want AI agents that can discover like we can, not which contain what we have discovered." To our knowledge, this is the first benchmark of TabPFN learning genomic prediction directly from raw marker data, with minimal human curation.

This is particularly interesting because we have strong biological reason to expect non-linear effects and interactions between genetic variants. TabPFN's in-context learning and ability to model complex relationships offer a way to capture these patterns without explicitly specifying them. More broadly, TabPFN makes it possible to approach genomic prediction with little dataset-specific model selection or hyperparameter tuning.

Recent improvements in TabPFN's input capacity make this approach substantially more practical. TabPFN-3.5 accepts up to **20,000 features**, 10× more than earlier versions, which is enough to use raw marker data for many genomic datasets. This is an important unlock for genomic data, where tens of thousands of genetic markers per individual are common.

The central question is simple:

> **How well can a general-purpose tabular foundation model perform on genomic prediction, without the specialized machinery traditionally built around this problem?**

## Results

We benchmarked TabPFN-3.5 on the six-species, 18-trait dataset of
[Azodi et al. (2019)](https://doi.org/10.1534/g3.119.400498), who compared 18 established genomic
prediction methods: mixed models (rrBLUP), Bayesian regressions (BayesA, BayesB, Bayesian LASSO,
Bayesian ridge regression), elastic nets, support vector machines, random forests, gradient
boosting and neural networks. For each trait we ran TabPFN on 10 random 80/20 splits of the lines
and report the mean prediction accuracy: the Pearson correlation between predicted and observed
trait values in the held-out 20%, the same measure the paper uses.

![TabPFN-3.5 vs the best of 18 published methods for each species and trait](figures/fig1_tabpfn_vs_best.png)

**TabPFN-3.5 is the best of 19 methods on 11 of the 18 tests**, and in the top three on 12.
Ranking all 19 methods on every test, TabPFN's median rank is 1st. The next best is the paper's
own overall winner, an elastic net (EN11), at 3.5:

| Method | Median rank (of 19) | Tests where best |
|---|---|---|
| **TabPFN-3.5** | **1** | **11** |
| EN11 (elastic net) | 3.5 | 2 |
| BayesA | 5 | 0 |
| EN5 (elastic net) | 5.5 | 0 |
| BRR (Bayesian ridge regression) | 6 | 2 |
| rrBLUP (the standard mixed model) | 6 | 0 |

TabPFN does best where it can see every marker. Soy (4,234 markers) and spruce (6,930) fit
within TabPFN-3.5's 20,000-feature limit, and there TabPFN ranks first on all 6 tests. On soy,
the dataset with the largest test sets (1,003 lines), it improves on the best published method by
2.5–9% (relative). The other four species have 56,000–245,000 markers, so we give TabPFN a compact
version: the top 100 principal components of all markers (a genome-wide summary of how related
the lines are), plus 19,900 raw markers spaced evenly along the genome. There TabPFN ranks first
on 5 of 12 tests; where it falls short, the gap is mostly within the noise of these test sets.
Per-trait numbers are in [`results/summary_table.csv`](results/summary_table.csv).

A note on comparability: Azodi et al. did not publish their exact train/test splits, so our
splits are different random 80/20 splits. As a check, we re-ran rrBLUP on our
splits for soy and spruce. It lands within 0.003–0.010 of the published rrBLUP on five of six
tests, so our splits are comparable to theirs.

## Methods details

- **Data.** Genotypes, phenotypes and cross-validation folds from Azodi et al. (2019), unchanged
  (see [`data/README.md`](data/README.md)). Markers are coded -1/0/1.
- **Splits.** For each trait, replicate *i* (1–10) holds out the lines in fold 1 of column `cv_i`
  of the published fold file (20% of lines) and trains on the rest. We report the mean Pearson r
  over the 10 replicates, as the paper does.
- **Model.** `TabPFNRegressor` from `tabpfn` 9.1.0 (TabPFN-3.5 weights) with default settings and
  no tuning; `random_state` is the replicate number. The only setting we change is the number of
  ensemble members: TabPFN-3.5 gives each member a random 768 of the input columns, and we use
  enough members that every column is seen at least once.
- **Soy and spruce: raw markers.** All 4,234 (soy) and 6,930 (spruce) markers go in as they are.
- **Rice, sorghum, maize and switchgrass: 100 PCs + thinned markers.** These have 56,000–245,000
  markers, more than TabPFN-3.5 accepts. Each split gets (1) the top 100 principal components of
  all markers, fit on the training lines only, and (2) 19,900 raw markers, chosen evenly along the
  genome after sorting by chromosome and position. TabPFN's `constant_and_balanced` feature
  subsampling puts the 100 components into every ensemble member, so this genome-wide summary
  isn't diluted among the markers. Neither step uses trait values.
- **Other inputs we tried** (all in [`results/all_runs.csv`](results/all_runs.csv)). On the four
  large species, the hybrid beat thinned markers alone on 97 of 120 splits and principal
  components alone on 82 of 120. Going past TabPFN-3.5's limit with all
  57,542 rice markers (`ignore_pretraining_limits`) gained nothing over 20,000 thinned markers
  (better on 10 of 30 splits) at three times the run time: neighboring markers carry largely the
  same information, so thinning loses little.
- **rrBLUP check.** Implemented with the R package `rrBLUP`, following the authors' published
  script ([`rrblup_holdout.R`](rrblup_holdout.R)), on the same splits as TabPFN.

## Reproducing the results

**Requirements:** Python 3.10 or newer (we used 3.14), a GPU, and a
[Prior Labs account](https://ux.priorlabs.ai) to accept the TabPFN-3.5 license. R with the
`rrBLUP` package is needed only for the rrBLUP check.

```
git clone https://github.com/flag0010/tabular-genomic-prediction-tabpfn-hackathon-2026.git
cd tabular-genomic-prediction-tabpfn-hackathon-2026
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python data/prepare_data.py          # unpacks the data mirror and checks it against Dryad
```

The first TabPFN run opens a browser to log in to Prior Labs and accept the license. Without a
browser, accept it at https://ux.priorlabs.ai and set `TABPFN_TOKEN` to your API key.

**Quick check:** rice yield with the hybrid input, 10 splits.

```
python tabpfn_holdout.py rice --features hybrid --n-pcs 100 --n-estimators cover --traits YLD --tag quickstart
```

This writes `results/rice_quickstart.csv`. Its mean r should be about 0.47, matching our saved
run (`results/rice_TabPFN_hybrid100_cover.csv`, trait `YLD`).

**Everything:** `results/` holds our saved results, and the scripts skip fits that are already
saved. To rebuild the tables and figure from them: `./run_all.sh summary`. To rerun
every fit from scratch:

```
rm results/*.csv && ./run_all.sh
```

## License

The code in this repository is Apache-2.0 (see [`LICENSE`](LICENSE)). It does not include the
TabPFN-3.5 model weights, which are licensed by Prior Labs
GmbH under the [TabPFN-3.5 Non-Commercial License](https://huggingface.co/Prior-Labs/tabpfn_3_5/blob/main/LICENSE).
