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

# Same fixed categorical color order as plotutil.py, so a plot built here
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

# Legend layout. Wrapping at 4 columns keeps a long nutrient name from being
# squeezed; the two pads (in points) are the vertical room an above-the-plot
# legend needs — a fixed gap plus one row's worth per wrapped row.
LEGEND_MAX_NCOL = 4
LEGEND_POSITIONS = ("auto", "top", "bottom")
LEGEND_TOP_PAD_BASE = 12
LEGEND_TOP_PAD_PER_ROW = 15
# Extra breathing room (points) between an above-the-plot legend and the top
# of the plot frame, on top of the legend's own ~5pt border padding — i.e.
# the gap is half again as wide as matplotlib leaves it. Anchoring the legend
# at exactly 1.0 sat it too close to the frame to read as a separate block.
# The subtitle's pad grows by the same amount, so the legend gains the room
# below it without losing any above.
LEGEND_TOP_EXTRA_GAP_PT = 2.5

GRID_COLOR = "#CCCCCC"
GRAYSCALE_COLOR = "#222222"
FIGSIZE = (9, 4.5)
DPI = 150


def line_plot_image(series: list[dict], xlabel: str, ylabel: str, title: str = "",
                     subtitle: str = "", image_format: str = "png", grayscale: bool = False,
                     hide_y_values: bool = False, legend_pos: str = "auto") -> bytes:
    """Render a line plot to image bytes (PNG or SVG). Each series dict:
    {"x": [...], "y": [...], "label": str, "color": str (optional),
    "highlight": bool (optional), "goal": float (optional), "limit": float
    (optional)}. All series share the same x (a date string list); a
    missing value should be passed as float("nan") so the line breaks
    instead of interpolating across the gap.

    A series with a numeric "goal" gets a horizontal dashed reference line
    drawn across the full plot width, in that series' own color, marking a
    fixed target level (e.g. a profile RDA/optimal target) rather than a
    data point. A numeric "limit" gets the same treatment but dotted, for a
    maximum/upper-limit level — kept visually distinct from "goal" so a
    nutrient with both (e.g. a user-configured max alongside its RDA/optimal
    target) reads as two different kinds of reference line, not a repeat.

    subtitle: an optional smaller line of text under the main title (e.g.
    explaining the goal dashed lines) — rendered as the figure's suptitle
    plus an axes-level title, so it can carry a distinct (smaller) font size
    from `title` itself; ignored if `title` is blank.

    hide_y_values: when different nutrients on the plot are on different
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
    through distinct dash patterns instead of colors, so the plot still
    reads correctly printed on a non-color printer.

    The legend is wrapped horizontally rather than stacked vertically, so
    it never overlaps a data line and stays print-friendly. Drawn only when
    there's more than one series.

    legend_pos: "top" puts the legend between the subtitle and the top of
    the plot frame, "bottom" puts it under the plot, and "auto" (the
    default) picks "top" while the legend still fits on one row and
    "bottom" once it would wrap — a wrapped multi-row block above the plot
    squeezes the plot area and reads as a heavy header, which is exactly
    the case below-the-plot placement handles better. Any unrecognized
    value is treated as "auto". Above-the-plot placement has to reserve its
    own vertical room (the subtitle's pad and the axes' top both shrink by
    the legend's row count) because, unlike the below case, there's no free
    margin there to grow into."""
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
        goal = s.get("goal")
        if goal is not None:
            ax.axhline(y=goal, color=color, linestyle="--", linewidth=1)
        limit = s.get("limit")
        if limit is not None:
            ax.axhline(y=limit, color=color, linestyle=":", linewidth=1)
    ax.set_xlabel(xlabel)
    if hide_y_values:
        ax.set_yticklabels([])
    else:
        ax.set_ylabel(ylabel)
    # Worked out before the titles are drawn: an above-the-plot legend sits
    # in space the title/subtitle would otherwise occupy, so how far to push
    # them up depends on how many rows the legend wraps to.
    legend_ncol = min(n, LEGEND_MAX_NCOL)
    legend_rows = math.ceil(n / legend_ncol) if n > 1 else 0
    if legend_pos not in LEGEND_POSITIONS:
        legend_pos = "auto"
    if legend_pos == "auto":
        legend_pos = "top" if legend_rows <= 1 else "bottom"
    legend_above = n > 1 and legend_pos == "top"
    title_pad = (LEGEND_TOP_PAD_BASE + LEGEND_TOP_PAD_PER_ROW * legend_rows
                 + LEGEND_TOP_EXTRA_GAP_PT) if legend_above else None
    if title and subtitle:
        fig.suptitle(title, y=0.98)
        ax.set_title(subtitle, fontsize=9, style="italic", color="#555555", pad=title_pad)
    elif title:
        ax.set_title(title, pad=title_pad)
    if legend_above and title:
        fig.subplots_adjust(top=max(0.50, 0.86 - 0.06 * legend_rows))
    ax.grid(True, color=GRID_COLOR, linewidth=0.6)
    ax.set_axisbelow(True)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    if n > 1:
        if legend_above:
            # The gap is specified in points, so it stays the same visual size
            # whatever the axes ends up being; converting needs the axes box
            # after subplots_adjust above, not before.
            axes_height_pt = ax.get_position().height * FIGSIZE[1] * 72
            gap = LEGEND_TOP_EXTRA_GAP_PT / axes_height_pt if axes_height_pt else 0
            ax.legend(frameon=False, loc="lower center", bbox_to_anchor=(0.5, 1.0 + gap),
                      ncol=legend_ncol)
        else:
            ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.28),
                      ncol=legend_ncol)

    n_dates = len(series[0]["x"]) if series else 0
    if n_dates > MAX_X_LABELS:
        step = max(2, math.ceil(n_dates / MAX_X_LABELS))
        ax.set_xticks(list(range(0, n_dates, step)))
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

    buf = io.BytesIO()
    fig.savefig(buf, format=image_format, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    return buf.getvalue()
