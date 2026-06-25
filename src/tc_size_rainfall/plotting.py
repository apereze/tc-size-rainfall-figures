from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns


def set_paper_style() -> None:
    """Apply a consistent plotting style for manuscript figures."""
    sns.set_theme(
        context="paper",
        style="whitegrid",
        font_scale=1.0,
        rc={
            "figure.dpi": 150,
            "savefig.dpi": 300,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.titleweight": "bold",
        },
    )


def save_figure(fig: plt.Figure, path: str | Path) -> None:
    """Save a figure with publication-oriented defaults."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    fig.savefig(path, bbox_inches="tight", dpi=300)
    fig.savefig(path.with_suffix(".pdf"), bbox_inches="tight")
