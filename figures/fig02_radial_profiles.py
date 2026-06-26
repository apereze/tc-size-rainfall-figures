import matplotlib.pyplot as plt
import pandas as pd

from tc_size_rainfall.config import FIGURE_DIR, FIGURE_INPUT_DIR
from tc_size_rainfall.plotting import save_figure, set_paper_style

set_paper_style()

QUADRANT_ORDER = ["RNE", "RNW", "RSW", "RSE"]
CATEGORY_ORDER = ["TD", "TS", "MIN HUR", "MAJ HUR"]

QUADRANT_COLORS = {
    "RNE": "#1b9e77",
    "RNW": "#d95f02",
    "RSW": "#7570b3",
    "RSE": "#e7298a",
}

CATEGORY_COLORS = {
    "TD": "#66a61e",
    "TS": "#e6ab02",
    "MIN HUR": "#a6761d",
    "MAJ HUR": "#666666",
}

CATEGORY_LABELS = {
    "TD": "TD",
    "TS": "TS",
    "MIN HUR": "Minor hurricane",
    "MAJ HUR": "Major hurricane",
}


def load_profile(name: str) -> pd.DataFrame:
    path = FIGURE_INPUT_DIR / name
    df = pd.read_csv(path)
    expected = {"x", "rain", "basin"}
    missing = expected.difference(df.columns)
    if missing:
        raise ValueError(f"{path} is missing columns: {sorted(missing)}")
    return df


def plot_profiles(ax, df, *, order, colors, labels=None, title):
    for group in order:
        subset = df[df["basin"] == group].sort_values("x")
        if subset.empty:
            continue
        ax.plot(
            subset["x"],
            subset["rain"],
            label=(labels or {}).get(group, group),
            color=colors[group],
            linewidth=1.8,
        )

    ax.set_title(title)
    ax.set_xlabel("Distance from TC center (km)")
    ax.set_ylabel("Rainfall (mm)")
    ax.set_xlim(0, 2000)
    ax.legend(frameon=False, fontsize=8)


def main():
    na_quadrants = load_profile("NAQ.csv")
    ep_quadrants = load_profile("EPQ.csv")
    na_categories = load_profile("NAcat.csv")
    ep_categories = load_profile("EPcat.csv")

    fig, axes = plt.subplots(2, 2, figsize=(10, 6), sharex=True, sharey=True)

    plot_profiles(
        axes[0, 0],
        na_quadrants,
        order=QUADRANT_ORDER,
        colors=QUADRANT_COLORS,
        title="North Atlantic by quadrant",
    )
    plot_profiles(
        axes[0, 1],
        ep_quadrants,
        order=QUADRANT_ORDER,
        colors=QUADRANT_COLORS,
        title="Eastern Pacific by quadrant",
    )
    plot_profiles(
        axes[1, 0],
        na_categories,
        order=CATEGORY_ORDER,
        colors=CATEGORY_COLORS,
        labels=CATEGORY_LABELS,
        title="North Atlantic by intensity",
    )
    plot_profiles(
        axes[1, 1],
        ep_categories,
        order=CATEGORY_ORDER,
        colors=CATEGORY_COLORS,
        labels=CATEGORY_LABELS,
        title="Eastern Pacific by intensity",
    )

    fig.tight_layout()
    save_figure(fig, FIGURE_DIR / "fig02_radial_profiles.png")


if __name__ == "__main__":
    main()
