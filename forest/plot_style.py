"""Shared look for every figure the project saves to disk.

Figures are sized for a Word page (about 16 cm of text width), so the font
sizes below are the sizes the reader actually sees in the document.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # figures are saved to files, never shown in a window

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


# Series colours (fixed order: first series blue, second orange, third aqua).
BLUE = "#2a78d6"
ORANGE = "#eb6834"
AQUA = "#1baf7a"
RED = "#e34948"

# Text and chart furniture.
INK = "#0b0b0b"
INK_SECONDARY = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
AXIS = "#c3c2b7"
CONTEXT_GRAY = "#d3d2cb"

# Text width of an A4 page with 2.5 cm margins, in inches.
PAGE_WIDTH = 6.3

# One hue, light to dark: used when colour means "how much".
SEQUENTIAL_BLUE = LinearSegmentedColormap.from_list(
    "sequential_blue",
    ["#ffffff", "#cde2fb", "#86b6ef", "#3987e5", "#1c5cab", "#0d366b"],
)

# Two opposite hues around a neutral grey: used when colour means "above/below".
DIVERGING_BLUE_RED = LinearSegmentedColormap.from_list(
    "diverging_blue_red",
    ["#104281", "#3987e5", "#9ec5f4", "#f0efec", "#f2a9a8", "#e34948", "#9c2423"],
)


def apply_style() -> None:
    """Set the matplotlib defaults shared by all project figures."""
    plt.rcParams.update({
        "font.family": ["Segoe UI", "DejaVu Sans"],
        "font.size": 8.5,
        "axes.titlesize": 9.5,
        "axes.titleweight": "bold",
        "axes.titlelocation": "left",
        "axes.labelsize": 8.5,
        "axes.labelcolor": INK_SECONDARY,
        "axes.edgecolor": AXIS,
        "axes.linewidth": 0.8,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "axes.axisbelow": True,
        "grid.color": GRID,
        "grid.linewidth": 0.6,
        "grid.linestyle": "-",
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "xtick.labelcolor": INK_SECONDARY,
        "ytick.labelcolor": INK_SECONDARY,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "xtick.major.size": 0,
        "ytick.major.size": 0,
        "legend.frameon": False,
        "legend.fontsize": 8.5,
        "lines.linewidth": 1.8,
        "text.color": INK,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "savefig.facecolor": "white",
    })


def save_figure(fig: plt.Figure, output_path: Path) -> None:
    """Write one figure as a PNG and close it."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=220, bbox_inches="tight")
    plt.close(fig)
    print(f"Figure saved: {output_path}")
