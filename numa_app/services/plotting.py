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
import re
import textwrap

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
LEGEND_POSITIONS = ("auto", "top", "bottom", "right")
# A right-of-plot legend is one column; names longer than this many
# characters wrap onto further lines, so the column stays narrow enough to
# fit in the space a below-the-plot legend would have left blank beside the
# plot. The extra label spacing keeps one wrapped name from reading as two.
LEGEND_RIGHT_WRAP_CHARS = 28
LEGEND_RIGHT_LABEL_SPACING = 1.0
LEGEND_TOP_PAD_BASE = 12
LEGEND_TOP_PAD_PER_ROW = 15
# Extra breathing room (points) between an above-the-plot legend and the top
# of the plot frame, on top of the legend's own ~5pt border padding — i.e.
# the gap is half again as wide as matplotlib leaves it. Anchoring the legend
# at exactly 1.0 sat it too close to the frame to read as a separate block.
# The subtitle's pad grows by the same amount, so the legend gains the room
# below it without losing any above.
LEGEND_TOP_EXTRA_GAP_PT = 2.5

# One marker shape per series, cycled in order, so every line can be told
# apart by its points (and its legend sample) as well as its color — and in
# grayscale, as well as its dash pattern. Each entry is (marker, size,
# fillable): the asterisk and "#" are stroke-only shapes, so they draw a
# little larger to read at the same weight, and can't be shown hollow.
# The rectangle is a custom wide box (matplotlib has no built-in one).
_RECT = [(-1.0, -0.4), (1.0, -0.4), (1.0, 0.4), (-1.0, 0.4), (-1.0, -0.4)]
MARKERS = [
    ("o", 4, True),          # solid circle
    ("s", 4, True),          # square
    (_RECT, 7, True),        # rectangle
    ((6, 2, 0), 7, False),   # asterisk
    (r"$\#$", 7, False),    # pound sign
    ("^", 5, True),          # triangle
    ("D", 4, True),          # diamond
    ("v", 5, True),          # downward triangle
]

GRID_COLOR = "#CCCCCC"
GRAYSCALE_COLOR = "#222222"
FIGSIZE = (9, 4.5)
DPI = 150


def _wrap_legend_label(label: str) -> str:
    """Wrap a legend name for the one-column right-of-plot legend. A
    parenthesized group ("(hollow = partial)") and the scale factor ("÷31.1
    ×8") each stay on one line, so a wrap never strands a fragment of either;
    non-breaking spaces hold them together, which textwrap won't split on and
    which draw like ordinary spaces."""
    glued = re.sub(r"\([^)]*\)", lambda m: m.group(0).replace(" ", "\u00a0"), label)
    glued = re.sub(r"[÷×]\S+( [÷×]\S+)*", lambda m: m.group(0).replace(" ", "\u00a0"), glued)
    return "\n".join(textwrap.wrap(glued, LEGEND_RIGHT_WRAP_CHARS)) or label


def line_plot_image(series: list[dict], xlabel: str, ylabel: str, title: str = "",
                     subtitle: str = "", image_format: str = "png", grayscale: bool = False,
                     hide_y_values: bool = False, legend_pos: str = "auto",
                     narrow: bool = False) -> bytes:
    """Render a line plot to image bytes (PNG or SVG). Each series dict:
    {"x": [...], "y": [...], "label": str, "color": str (optional),
    "highlight": bool (optional), "goal": float (optional), "limit": float
    (optional), "hollow": [bool, ...] (optional, one per x — those points
    draw as open circles, e.g. a day whose value is only partly known)}. All series share the same x (a date string list); a
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

    Each series also gets its own marker shape (MARKERS, cycled in series
    order) in both modes, shown on the legend sample too. A "hollow" point
    draws as that same shape unfilled; a stroke-only shape (asterisk, "#")
    has no fill to remove, so it gets an open ring around it instead.

    Grayscale mode (grayscale=True): every line is the same dark gray —
    the "highlight" series (if any) draws solid, every other series cycles
    through distinct dash patterns instead of colors, so the plot still
    reads correctly printed on a non-color printer.

    The legend is wrapped horizontally rather than stacked vertically, so
    it never overlaps a data line and stays print-friendly. Drawn only when
    there's more than one series.

    legend_pos: "top" puts the legend between the subtitle and the top of
    the plot frame, "bottom" puts it under the plot, "right" stacks it in
    one column beside the plot, top-aligned, with long names wrapped (the
    image grows wider by the column's width; the plot keeps its size), and "auto" (the
    default) picks "top" while the legend still fits on one row and
    "right" once it would wrap — a wrapped multi-row block above the plot
    squeezes the plot area and reads as a heavy header. Any unrecognized
    value is treated as "auto".

    narrow: the image is for a screen too narrow for a side column, so
    "right" (asked for, or picked by "auto") becomes "bottom" instead. Above-the-plot placement has to reserve its
    own vertical room (the subtitle's pad and the axes' top both shrink by
    the legend's row count) because, unlike the below case, there's no free
    margin there to grow into."""
    fig, ax = plt.subplots(figsize=FIGSIZE)
    n = len(series)
    # Resolved before anything is drawn: a right-of-plot legend wraps the
    # labels themselves, and an above-the-plot one sits in space the
    # title/subtitle would otherwise occupy, so how far to push them up
    # depends on how many rows the legend wraps to.
    legend_ncol = min(n, LEGEND_MAX_NCOL)
    legend_rows = math.ceil(n / legend_ncol) if n > 1 else 0
    if legend_pos not in LEGEND_POSITIONS:
        legend_pos = "auto"
    if legend_pos == "auto":
        legend_pos = "top" if legend_rows <= 1 else "right"
    if narrow and legend_pos == "right":
        legend_pos = "bottom"
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
        marker, msize, fillable = MARKERS[i % len(MARKERS)]
        label = s.get("label") or f"Series {i + 1}"
        if legend_pos == "right":
            label = _wrap_legend_label(label)
        ax.plot(s["x"], s["y"], color=color, linestyle=linestyle, linewidth=1,
                 marker=marker, markersize=msize, label=label)
        hollow = s.get("hollow")
        if hollow and any(hollow):
            # Redraw just those points hollow over the filled ones.
            hx = [x for x, h in zip(s["x"], hollow) if h]
            hy = [y for y, h in zip(s["y"], hollow) if h]
            if fillable:
                ax.plot(hx, hy, linestyle="none", marker=marker, markersize=msize + 1,
                        markerfacecolor="white", markeredgecolor=color, markeredgewidth=1)
            else:
                ax.plot(hx, hy, linestyle="none", marker="o", markersize=msize + 3,
                        markerfacecolor="none", markeredgecolor=color, markeredgewidth=1)
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
        elif legend_pos == "right":
            ax.legend(frameon=False, loc="upper left", bbox_to_anchor=(1.02, 1.0),
                      ncol=1, labelspacing=LEGEND_RIGHT_LABEL_SPACING)
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
