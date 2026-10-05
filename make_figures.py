"""Figure: TabPFN vs the best of 18 published methods, one bar-chart panel per species.

Reads results/summary_table.csv (run summarize_results.py first) and writes
figures/tabpfn_vs_best.png.

Usage: python make_figures.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parent
FIG_DIR = ROOT / "figures"

SURFACE = "#fcfcfb"
TEXT = "#0b0b0b"
TEXT_2 = "#52514e"
GRID = "#e4e3df"
TABPFN = "#2a78d6"  # categorical slot 1
BEST = "#eb6834"    # categorical slot 2

SPECIES = ["soy", "spruce", "rice", "sorghum", "maize", "switchgrass"]


def main():
    d = pd.read_csv(ROOT / "results" / "summary_table.csv")
    plt.rcParams.update({"font.size": 10, "text.color": TEXT, "axes.labelcolor": TEXT_2,
                         "xtick.color": TEXT_2, "ytick.color": TEXT})
    fig, axes = plt.subplots(2, 3, figsize=(12, 8), sharey=True, facecolor=SURFACE)

    width = 0.36
    for ax, species in zip(axes.flat, SPECIES):
        g = d[d.species == species].reset_index(drop=True)
        ax.set_facecolor(SURFACE)
        x = range(len(g))
        for i, row in g.iterrows():
            win = row.tabpfn_r > row.best_published_r
            # TabPFN: mean of 10 splits (the 2px edge keeps a gap between bars)
            ax.bar(i - width / 2, row.tabpfn_r, width, color=TABPFN, edgecolor=SURFACE, lw=2)
            if win:
                ax.text(i - width / 2, row.tabpfn_r + 0.02, "★", ha="center",
                        va="bottom", fontsize=11, color=TEXT)
            # Best published method, labeled with its name
            ax.bar(i + width / 2, row.best_published_r, width, color=BEST, edgecolor=SURFACE, lw=2)
            ax.text(i + width / 2, row.best_published_r + 0.02, row.best_published, ha="center",
                    va="bottom", fontsize=7.5, color=TEXT_2, rotation=90)
        ax.set_xticks(list(x), [t.replace(" ", "\n") for t in g.trait], fontsize=9.5)
        ax.tick_params(axis="both", length=0)
        ax.set_ylim(0, 1.12)
        ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
        ax.grid(axis="y", color=GRID, lw=0.8)
        ax.set_axisbelow(True)
        for side in ["top", "right", "left"]:
            ax.spines[side].set_visible(False)
        ax.spines["bottom"].set_color(GRID)
        n_test = int(g.n_test.iloc[0])
        ax.set_title(f"{g.input.iloc[0]}  ·  {n_test} test lines", loc="left", fontsize=8.5,
                     color=TEXT_2, pad=6)
        ax.text(0, 1.11, species, transform=ax.transAxes, fontsize=12, fontweight="bold",
                color=TEXT)

    fig.supylabel("Prediction accuracy (Pearson r between observed and predicted trait values)",
                  fontsize=10, color=TEXT_2)

    handles = [plt.Rectangle((0, 0), 1, 1, color=TABPFN,
                          label="TabPFN-3.5 (mean of 10 splits)"),
               plt.Rectangle((0, 0), 1, 1, color=BEST,
                          label="Best of 18 published methods (Azodi et al. 2019)")]
    fig.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.01, 0.995), ncol=2,
               frameon=False, fontsize=9.5)
    fig.text(0.99, 0.975, "★ = TabPFN ranks first of 19 methods", ha="right", fontsize=9.5,
             color=TEXT_2)
    fig.tight_layout(rect=(0.02, 0, 1, 0.94), w_pad=2, h_pad=3)

    FIG_DIR.mkdir(exist_ok=True)
    out = FIG_DIR / "tabpfn_vs_best.png"
    fig.savefig(out, dpi=200, facecolor=SURFACE, bbox_inches="tight", pad_inches=0.2)
    print(out)


if __name__ == "__main__":
    main()
