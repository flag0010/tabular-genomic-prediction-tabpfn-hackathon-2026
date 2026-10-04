# Tabular genomic prediction with TabPFN-3.5

An entry to the Prior Labs TabPFN-3.5 Hackathon (2026): predicting plant traits from genetic
markers by treating genomic prediction as a plain tabular regression problem, benchmarked
against 18 established methods on six crop and tree species.

## Genomic Prediction

**Genomic prediction** is widely used in modern plant and animal breeding to predict an individual's phenotypic performance (traits like yield, disease resistance, growth rate, milk production, or meat quality) from its genetic markers (genomic DNA sequence information). A model is trained on individuals with both genotype and phenotype data, then used to predict the performance of new individuals from genotype alone.

Genomic prediction is valuable because genotyping is extremely fast and inexpensive relative to phenotyping. Breeders can screen thousands or millions of individuals genetically and select the most promising ones without having to phenotype, enabling earlier identification of elite individuals and accelerating breeding progress.

Genomic prediction has been used for roughly 20 years and is now foundational to breeding programs in maize, soybean, wheat, cattle, pigs, chickens, and many other crops and livestock we all depend on. It underpins breeding industries worth billions of dollars, with genomic selection in U.S. dairy cattle alone estimated to have returned about $4 billion since its adoption in 2009 ([Rexroad et al. 2019](https://doi.org/10.3389/fgene.2019.00327)). Because genetic gains accumulate across generations, even modest improvements in selection accuracy can translate into substantial additional economic gains over the course of a breeding program. This makes genomic prediction an especially valuable target for developing better prediction methods.

### Why TabPFN and why now?

A typical genomic prediction dataset consists of an $N \times M$ matrix of genetic markers and an $N \times P$ matrix of phenotypic measurements, potentially accompanied by covariates. In the simplest formulation, this is a **supervised learning problem**. Individuals with known genotypes and phenotypes are used to learn a mapping from genotype to phenotype, which is then used to predict phenotypes for individuals whose phenotypes have not yet been observed.

The dimensionality is unusual compared with many conventional tabular problems. A dataset might contain 1,000 samples (individuals) and 20,000 features (genetic markers), resulting in 20 million genotype measurements but only 1,000 labeled examples. In other words, genomic prediction often has very large numbers of features relative to the number of individuals.

Numerous specialized methods exist for genomic prediction, including mixed models, Bayesian models, kernel methods, and machine learning approaches. Most are designed around genetic relationships, marker effects, or assumptions about how genetic variation affects phenotypes rather than treating the problem as generic tabular learning. [The Bitter Lesson](http://www.incompleteideas.net/IncIdeas/BitterLesson.html) suggests that there may be value in taking the opposite approach, abandon domain-specific assumptions and let compute and increasingly capable general-purpose learning systems do the heavy lifting.

Here we take that Bitter Lesson approach. **We treat genomic prediction as a tabular regression problem and apply TabPFN directly.**

This is particularly interesting because we have strong biological reason to expect non-linear effects and interactions between genetic variants. TabPFN's in-context learning and ability to model complex relationships offer a way to capture these patterns without explicitly specifying a genetic architecture. More broadly, TabPFN makes it possible to approach genomic prediction with little dataset-specific model selection or hyperparameter tuning.

Recent improvements in TabPFN's input capacity make this approach substantially more practical. TabPFN-3.5 accepts up to **20,000 features**, 10× more than earlier versions, which is enough to use raw marker data for many genomic datasets. This is an important unlock for genomic data, where tens of thousands of genetic markers per individual are common.

The central question is simple:

> **How well can a general-purpose tabular foundation model perform on genomic prediction, without the specialized machinery traditionally built around this problem?**

## Status

Work in progress. Methods, results and instructions for reproducing them are coming.
For the data and how to get it, see [`data/README.md`](data/README.md).

## License

The code in this repository is Apache-2.0 (see [`LICENSE`](LICENSE)). It does not include the
TabPFN-3.5 model weights, which TabPFN downloads on first use and which are licensed by Prior Labs
GmbH under the [TabPFN-3.5 Non-Commercial License](https://huggingface.co/Prior-Labs/tabpfn_3_5/blob/main/LICENSE):
research and evaluation use is free, while commercial or production use needs a license from Prior Labs.
