"""
plotting.py — line-plot rendering for the web app's Daily Summary nutrient
plot. Trimmed from GeTIpy's tools/plotutil.py (that copy also has point/
histogram plots, CSV/YAML/CLI input modes, error bars, and fit lines, none
of which numa's date-series use needs) — see
Obsidian-vault/_sync/GeTIpy/tools/plotutil.py for the full utility. This is
a hand-vendored copy, not an import: re-sync by hand if plotutil.py's
line_plot core changes.
Docs: README-numa-documentation.md
"""
import io
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Cap on how many x-axis date labels are shown at once — beyond this, every
# date's label starts touching its neighbors' when rotated. Thinning always
# leaves at least one skipped date between the labels that remain shown
# (never a bare 1-date step), since a 1-step is exactly the crowded case
# this exists to avoid.
MAX_X_LABELS = 18

# Same fixed categorical color order as plotutil.py, so a chart built here
# reads consistently with any GeTIpy plot the same data might also appear in.
CATEGORICAL_COLORS = [
    "#2a78d6",  # blue
    "#1baf7a",  # aqua
    "#eda100",  # yellow
    "#008300",  # green
    "#4a3aa7",  # violet
    "#e34948",  # red
    "#e87ba4",  # magenta
    "#eb6834",  # orange
]
MAX_SERIES = len(CATEGORICAL_COLORS)

# Dash patterns cycled for non-highlighted series in grayscale mode (solid
# is reserved for the highlighted series, so it's the one line that's
# unambiguous at a glance even before you've matched legend to line).
LINESTYLES = ["--", ":", "-.", (0, (3, 1, 1, 1, 1, 1)), (0, (5, 1)), (0, (1, 1)), (0, (4, 2, 1, 2))]

GRID_COLOR = "#CCCCCC"
GRAYSCALE_COLOR = "#222222"
FIGSIZE = (9, 4.5)
DPI = 150


def line_plot_image(series: list[dict], xlabel: str, ylabel: str, title: str = "",
                     image_format: str = "png", grayscale: bool = False,
                     hide_y_values: bool = False) -> bytes:
    """Render a line plot to image bytes (PNG or SVG). Each series dict:
    {"x": [...], "y": [...], "label": str, "color": str (optional),
    "highlight": bool (optional)}. All series share the same x (a date
    string list); a missing value should be passed as float("nan") so the
    line breaks instead of interpolating across the gap.

    hide_y_values: when different nutrients on the chart are on different
    per-series scale factors, no single number on a shared y-axis means
    the same thing for every line — printing it (or a "Value" title) would
    just be misleading. Set True to drop the axis title and tick numbers
    entirely (gridlines stay, for relative up/down comparison); each
    line's real values are only found via its own legend entry.

    Color mode (grayscale=False): a series with an explicit "color" always
    draws in that color; others cycle through the categorical palette,
    skipping any colors an explicit-color series already claimed. All lines
    are solid.

    Grayscale mode (grayscale=True): every line is the same dark gray —
    the "highlight" series (if any) draws solid, every other series cycles
    through distinct dash patterns instead of colors, so the chart still
    reads correctly printed on a non-color printer.

    The legend is drawn below the plot, wrapped horizontally rather than
    stacked vertically, so it never overlaps a data line and stays
    print-friendly. Drawn only when there's more than one series."""
    fig, ax = plt.subplots(figsize=FIGSIZE)
    n = len(series)
    claimed = {s["color"] for s in series if s.get("color")}
    auto_colors = [c for c in CATEGORICAL_COLORS if c not in claimed] or CATEGORICAL_COLORS
    auto_i = 0
    dash_i = 0
    for i, s in enumerate(series):
        is_highlight = bool(s.get("highlight"))
        if grayscale:
            color = GRAYSCALE_COLOR
            if is_highlight:
                linestyle = "-"
            else:
                linestyle = LINESTYLES[dash_i % len(LINESTYLES)]
                dash_i += 1
        else:
            color = s.get("color")
            if not color:
                color = auto_colors[auto_i % len(auto_colors)]
                auto_i += 1
            linestyle = "-"
        ax.plot(s["x"], s["y"], color=color, linestyle=linestyle, linewidth=1,
                 marker="o", markersize=3, label=s.get("label") or f"Series {i + 1}")
    ax.set_xlabel(xlabel)
    if hide_y_values:
        ax.set_yticklabels([])
    else:
        ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)
    ax.grid(True, color=GRID_COLOR, linewidth=0.6)
    ax.set_axisbelow(True)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    if n > 1:
        ncol = min(n, 4)
        ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.28), ncol=ncol)

    n_dates = len(series[0]["x"]) if series else 0
    if n_dates > MAX_X_LABELS:
        step = max(2, math.ceil(n_dates / MAX_X_LABELS))
        ax.set_xticks(list(range(0, n_dates, step)))
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

    buf = io.BytesIO()
    fig.savefig(buf, format=image_format, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    return buf.getvalue()
