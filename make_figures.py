"""Figure: TabPFN vs the best of 18 published methods, one panel per species.

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
    fig, axes = plt.subplots(2, 3, figsize=(13, 6.6), sharex=True, facecolor=SURFACE)

    for ax, species in zip(axes.flat, SPECIES):
        g = d[d.species == species].reset_index(drop=True)
        ax.set_facecolor(SURFACE)
        for i, row in g.iterrows():
            y = len(g) - 1 - i
            win = row.tabpfn_r > row.best_published_r
            # TabPFN: mean with corrected 95% interval, just above the row center
            ax.hlines(y + 0.14, row.tabpfn_ci95_low, row.tabpfn_ci95_high, color=TABPFN, lw=2)
            ax.plot(row.tabpfn_r, y + 0.14, "o", ms=8, color=TABPFN, mec=SURFACE, mew=2, zorder=3)
            # Best published method, just below, labeled with its name
            ax.plot(row.best_published_r, y - 0.14, "o", ms=8, color=BEST, mec=SURFACE, mew=2,
                    zorder=3)
            ax.annotate(row.best_published, (row.best_published_r, y - 0.14), xytext=(7, 0),
                        textcoords="offset points", va="center", fontsize=8, color=TEXT_2)
            ax.text(-0.01, y, ("★ " if win else "") + row.trait, transform=ax.get_yaxis_transform(),
                    ha="right", va="center", fontsize=9.5,
                    fontweight="bold" if win else "normal", color=TEXT)
        ax.set_yticks([])
        ax.set_ylim(-0.6, len(g) - 0.4)
        ax.set_xlim(0.15, 1.0)
        ax.grid(axis="x", color=GRID, lw=0.8)
        ax.set_axisbelow(True)
        for side in ["top", "right", "left"]:
            ax.spines[side].set_visible(False)
        ax.spines["bottom"].set_color(GRID)
        n_test = int(g.n_test.iloc[0])
        ax.set_title(f"{g.input.iloc[0]}  ·  {n_test} test lines", loc="left", fontsize=8.5,
                     color=TEXT_2, pad=6)
        ax.text(0, 1.13, species, transform=ax.transAxes, fontsize=12, fontweight="bold",
                color=TEXT)

    fig.supxlabel("Prediction accuracy (Pearson r between observed and predicted trait values)",
                  fontsize=10, color=TEXT_2)

    handles = [plt.Line2D([], [], marker="o", ls="-", color=TABPFN, ms=8, lw=2,
                          label="TabPFN-3.5 (mean of 10 splits, 95% interval)"),
               plt.Line2D([], [], marker="o", ls="", color=BEST, ms=8,
                          label="Best of 18 published methods (Azodi et al. 2019)")]
    fig.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.01, 0.995), ncol=2,
               frameon=False, fontsize=9.5)
    fig.text(0.99, 0.975, "★ = TabPFN ranks first of 19 methods", ha="right", fontsize=9.5,
             color=TEXT_2)
    fig.tight_layout(rect=(0.03, 0, 1, 0.93), w_pad=3, h_pad=2.5)

    FIG_DIR.mkdir(exist_ok=True)
    out = FIG_DIR / "tabpfn_vs_best.png"
    fig.savefig(out, dpi=200, facecolor=SURFACE, bbox_inches="tight", pad_inches=0.2)
    print(out)


if __name__ == "__main__":
    main()
