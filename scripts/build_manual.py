#!/usr/bin/env python3
"""
build_manual.py — Convert user-manual.md to user-manual.html.

Run from the project root (or any directory):
    python scripts/build_manual.py

Output: user-manual.html, placed next to user-manual.md.

Requires: pip install markdown  (already in requirements.txt)

Heading anchor convention
-------------------------
Headings that end with [anchor] in the source markdown (e.g. "### Title [foo]")
are the same sections used by the in-program ?help system.  This script strips
the bracketed tag from the visible heading text and sets the HTML id to that
short tag, so internal links can use clean short fragments like #foo instead of
the long auto-slugged form.

Headings without a bracketed tag get auto-slugged ids from the toc extension.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import markdown
    from markdown.extensions.toc import TocExtension
except ImportError:
    sys.exit("Error: 'markdown' package required.  Run: pip install markdown")


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SOURCE = PROJECT_ROOT / "user-manual.md"
OUTPUT = PROJECT_ROOT / "user-manual.html"

# Matches a markdown heading that ends with a [short-anchor] tag.
# Groups: (hashes, title_text, anchor)
_ANCHOR_RE = re.compile(
    r'^(#{1,6})\s+(.+?)\s+\[([a-z][a-z0-9-]*)\]\s*$',
    re.MULTILINE,
)


def preprocess(text: str) -> str:
    """Strip [anchor] from heading display text; inject {#anchor} for attr_list."""
    def _replace(m: re.Match) -> str:
        hashes, title, anchor = m.group(1), m.group(2).strip(), m.group(3)
        return f'{hashes} {title} {{#{anchor}}}'
    return _ANCHOR_RE.sub(_replace, text)


# ── Styling ──────────────────────────────────────────────────────────────────

CSS = """\
:root {
    --bg:           #ffffff;
    --fg:           #1a1a2e;
    --muted:        #5a5a7a;
    --toc-fg:       #4a4a6a;
    --accent:       #2a52be;
    --accent-light: #eef0ff;
    --border:       #d0d0e0;
    --code-bg:      #f4f4f8;
    --heading:      #0d1b5e;
    --toc-w:        390px;
}
@media (prefers-color-scheme: dark) {
    :root {
        --bg:           #12121e;
        --fg:           #dde0f0;
        --muted:        #9090b0;
        --toc-fg:       #c8cee8;
        --accent:       #7090f0;
        --accent-light: #1a2040;
        --border:       #2a2a4a;
        --code-bg:      #1e1e30;
        --heading:      #a0c0ff;
    }
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
                 "Helvetica Neue", Arial, sans-serif;
    font-size: 16px;
    line-height: 1.7;
    color: var(--fg);
    background: var(--bg);
    display: flex;
    min-height: 100vh;
}

/* ── Sidebar TOC ── */
#toc-sidebar {
    width: var(--toc-w);
    min-width: var(--toc-w);
    position: sticky;
    top: 0;
    height: 100vh;
    overflow-y: auto;
    padding: 1.25rem 0.75rem 1.5rem 0.5rem;
    border-right: 1px solid var(--border);
    background: var(--bg);
    font-size: 14.5px;
    line-height: 1.4;
}
#toc-sidebar h2 {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.5em;
    font-size: 11.5px;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--muted);
    margin-bottom: 0.75rem;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid var(--border);
}
#toc-collapse-all {
    background: none;
    border: 1px solid var(--border);
    border-radius: 3px;
    color: var(--toc-fg);
    cursor: pointer;
    font-size: 9px;
    text-transform: none;
    letter-spacing: normal;
    padding: 1px 5px;
    flex: none;
}
#toc-collapse-all:hover { background: var(--accent-light); color: var(--accent); }
#toc-sidebar .toc { list-style: none; }
#toc-sidebar .toc li { padding: 1px 0; }
#toc-sidebar .toc a {
    color: var(--toc-fg);
    text-decoration: none;
    display: block;
    padding: 2px 4px 2px 0.9em;
    text-indent: -0.9em;
    border-radius: 3px;
    white-space: normal;
    overflow-wrap: break-word;
    word-break: break-word;
}
#toc-sidebar .toc a:hover { color: var(--accent); background: var(--accent-light); }
#toc-sidebar .toc ul { list-style: none; padding-left: 0.85em; }
#toc-sidebar .toc ul a { font-size: 13.5px; }
#toc-sidebar .toc ul ul a { font-size: 13px; }

/* Per-heading collapse toggle + collapsed state */
#toc-sidebar .toc li.toc-has-children { position: relative; padding-left: 1.05em; }
#toc-sidebar .toc li.toc-has-children > a { padding-left: 0; text-indent: 0; }
#toc-sidebar .toc .toc-toggle {
    position: absolute;
    left: 0;
    top: 2px;
    background: none;
    border: none;
    cursor: pointer;
    color: var(--muted);
    font-size: 9px;
    width: 1em;
    padding: 0;
    line-height: 1.4;
}
#toc-sidebar .toc .toc-toggle:hover { color: var(--accent); }
#toc-sidebar .toc li.toc-collapsed > ul { display: none; }

/* ── Main content ── */
#content {
    flex: 1;
    max-width: 860px;
    padding: 2.5rem 3rem;
    min-width: 0;
}

h1 { font-size: 1.9rem; color: var(--heading); margin: 2rem 0 1rem;
     border-bottom: 2px solid var(--border); padding-bottom: 0.5rem; }
h2 { font-size: 1.45rem; color: var(--heading); margin: 2.5rem 0 0.75rem;
     border-bottom: 1px solid var(--border); padding-bottom: 0.25rem; }
h3 { font-size: 1.15rem; color: var(--heading); margin: 2rem 0 0.5rem; }
h4 { font-size: 1rem; color: var(--heading); margin: 1.5rem 0 0.4rem; font-style: italic; }

/* Permalink anchors from toc extension — hide unless hovering */
.headerlink { opacity: 0; margin-left: 0.4em; font-size: 0.8em; }
h1:hover .headerlink,
h2:hover .headerlink,
h3:hover .headerlink,
h4:hover .headerlink { opacity: 0.4; }

p { margin: 0.75rem 0; }
a { color: var(--accent); }
a:hover { text-decoration: underline; }

ul, ol { margin: 0.75rem 0 0.75rem 1.75rem; }
li { margin: 0.3rem 0; }

code {
    font-family: "SFMono-Regular", "Consolas", "Liberation Mono", monospace;
    font-size: 0.875em;
    background: var(--code-bg);
    padding: 0.1em 0.35em;
    border-radius: 3px;
    border: 1px solid var(--border);
}
pre {
    background: var(--code-bg);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 1rem 1.25rem;
    overflow-x: auto;
    margin: 1rem 0;
    font-size: 0.875em;
    line-height: 1.5;
}
pre code { background: none; border: none; padding: 0; font-size: inherit; }

table {
    border-collapse: collapse;
    width: 100%;
    margin: 1rem 0;
    font-size: 0.9em;
}
th {
    background: var(--accent-light);
    color: var(--heading);
    font-weight: 600;
    padding: 0.5rem 0.75rem;
    text-align: left;
    border: 1px solid var(--border);
}
td {
    padding: 0.4rem 0.75rem;
    border: 1px solid var(--border);
    vertical-align: top;
}
tr:nth-child(even) td { background: var(--code-bg); }

blockquote {
    border-left: 3px solid var(--accent);
    padding: 0.5rem 1rem;
    margin: 1rem 0;
    color: var(--muted);
    background: var(--accent-light);
    border-radius: 0 4px 4px 0;
}

hr { border: none; border-top: 1px solid var(--border); margin: 2rem 0; }

/* Footnotes */
.footnote { font-size: 0.85em; color: var(--muted); border-top: 1px solid var(--border);
            margin-top: 2rem; padding-top: 0.75rem; }


/* ── Search box ── */
#search-box {
    margin-bottom: 1rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid var(--border);
}
#search-input {
    width: 100%;
    padding: 5px 8px;
    border: 1px solid var(--border);
    border-radius: 4px;
    background: var(--code-bg);
    color: var(--fg);
    font-size: 12.5px;
    outline: none;
}
#search-input:focus { border-color: var(--accent); }
#search-nav {
    display: flex;
    align-items: center;
    gap: 4px;
    margin-top: 5px;
}
#search-count {
    flex: 1;
    font-size: 11px;
    color: var(--muted);
}
.search-btn {
    background: none;
    border: 1px solid var(--border);
    border-radius: 3px;
    color: var(--toc-fg);
    cursor: pointer;
    font-size: 11px;
    padding: 1px 6px;
    line-height: 1.6;
}
.search-btn:hover { background: var(--accent-light); color: var(--accent); }

/* ── Search highlights ── */
mark.search-hit {
    background: #ffe066;
    color: #1a1a00;
    border-radius: 2px;
    padding: 0 1px;
}
mark.search-current {
    background: #ff8c00;
    color: #fff;
    border-radius: 2px;
    padding: 0 1px;
}

/* ── Print ── */
@media print {
    #toc-sidebar { display: none; }
    body { display: block; }
    #content { max-width: 100%; padding: 1cm; }
    h2 { page-break-before: always; }
    h2:first-of-type { page-break-before: avoid; }
    .headerlink { display: none; }
    mark.search-hit, mark.search-current { background: none; color: inherit; }
}

/* ── Responsive: hide sidebar on narrow screens ── */
@media (max-width: 1050px) {
    #toc-sidebar { display: none; }
    #content { padding: 1.5rem; }
}
"""

JS = """\
(function () {
  var matches = [], idx = 0;

  function clearHighlights() {
    document.querySelectorAll('mark.search-hit').forEach(function (m) {
      var t = document.createTextNode(m.textContent);
      m.parentNode.replaceChild(t, m);
      t.parentNode.normalize();
    });
    matches = []; idx = 0;
  }

  function highlight(query) {
    clearHighlights();
    var q = query.trim();
    if (q.length < 2) { setCount(''); return; }
    var ql = q.toLowerCase();
    var content = document.getElementById('content');
    var walker = document.createTreeWalker(content, NodeFilter.SHOW_TEXT, {
      acceptNode: function (n) {
        return n.parentElement.closest('script,style,mark') ?
          NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT;
      }
    });
    var nodes = [];
    var n;
    while ((n = walker.nextNode())) nodes.push(n);

    nodes.forEach(function (node) {
      var text = node.textContent;
      var lower = text.toLowerCase();
      var pos = 0, start, frags = [];
      while ((start = lower.indexOf(ql, pos)) !== -1) {
        if (start > pos) frags.push(document.createTextNode(text.slice(pos, start)));
        var mark = document.createElement('mark');
        mark.className = 'search-hit';
        mark.textContent = text.slice(start, start + ql.length);
        frags.push(mark);
        matches.push(mark);
        pos = start + ql.length;
      }
      if (frags.length) {
        if (pos < text.length) frags.push(document.createTextNode(text.slice(pos)));
        var parent = node.parentNode;
        frags.forEach(function (f) { parent.insertBefore(f, node); });
        parent.removeChild(node);
      }
    });

    if (matches.length) { idx = 0; scrollTo(0); }
    setCount(matches.length ? (1) + ' / ' + matches.length : 'no matches');
  }

  function scrollTo(i) {
    matches.forEach(function (m, j) {
      m.className = j === i ? 'search-hit search-current' : 'search-hit';
    });
    if (matches[i]) matches[i].scrollIntoView({ behavior: 'smooth', block: 'center' });
    setCount(matches.length ? (i + 1) + ' / ' + matches.length : 'no matches');
  }

  function setCount(txt) {
    document.getElementById('search-count').textContent = txt;
  }

  function step(dir) {
    if (!matches.length) return;
    idx = (idx + dir + matches.length) % matches.length;
    scrollTo(idx);
  }

  document.addEventListener('DOMContentLoaded', function () {
    var input = document.getElementById('search-input');
    var timer;
    input.addEventListener('input', function () {
      clearTimeout(timer);
      timer = setTimeout(function () { highlight(input.value); }, 180);
    });
    input.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') { e.preventDefault(); step(e.shiftKey ? -1 : 1); }
      if (e.key === 'Escape') { input.value = ''; clearHighlights(); setCount(''); }
    });
    document.getElementById('btn-prev').addEventListener('click', function () { step(-1); });
    document.getElementById('btn-next').addEventListener('click', function () { step(1); });
  });
})();

/* ── TOC collapse/expand ── */
(function () {
  document.addEventListener('DOMContentLoaded', function () {
    var root = document.querySelector('#toc-sidebar .toc > ul');
    if (!root) return;

    /* The doc title (h1) wraps everything in one outer <li>; the "main
       headings" (h2 — Preface, Part 1, Part 2, ...) are its grandchildren.
       Fall back to the root list itself if there's no such wrapper. */
    var mainList = root.querySelector(':scope > li > ul') || root;
    var mainLis = Array.prototype.filter.call(mainList.children, function (el) {
      return el.tagName === 'LI';
    });

    mainLis.forEach(function (li) {
      var childUl = li.querySelector(':scope > ul');
      if (!childUl) return;
      var a = li.querySelector(':scope > a');
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'toc-toggle';
      btn.setAttribute('aria-label', 'Collapse or expand this section');
      btn.textContent = '▾';
      li.classList.add('toc-has-children');
      li.insertBefore(btn, a);
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        var collapsed = li.classList.toggle('toc-collapsed');
        btn.textContent = collapsed ? '▸' : '▾';
      });
    });

    if (!mainLis.length) return;

    var header = document.querySelector('#toc-sidebar h2');
    var allBtn = document.createElement('button');
    allBtn.type = 'button';
    allBtn.id = 'toc-collapse-all';
    allBtn.textContent = 'Collapse all';
    header.appendChild(allBtn);

    var allCollapsed = false;
    allBtn.addEventListener('click', function () {
      allCollapsed = !allCollapsed;
      mainLis.forEach(function (li) {
        if (!li.classList.contains('toc-has-children')) return;
        li.classList.toggle('toc-collapsed', allCollapsed);
        var btn = li.querySelector(':scope > .toc-toggle');
        if (btn) btn.textContent = allCollapsed ? '▸' : '▾';
      });
      allBtn.textContent = allCollapsed ? 'Expand all' : 'Collapse all';
    });
  });
})();
"""

HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NutriMagnus User Manual</title>
<style>
{css}
</style>
</head>
<body>
<nav id="toc-sidebar" aria-label="Table of contents">
  <div id="search-box">
    <input id="search-input" type="search" placeholder="Search manual…"
           autocomplete="off" spellcheck="false">
    <div id="search-nav">
      <span id="search-count"></span>
      <button class="search-btn" id="btn-prev" title="Previous (Shift+Enter)">&#x25B2;</button>
      <button class="search-btn" id="btn-next" title="Next (Enter)">&#x25BC;</button>
    </div>
  </div>
  <h2>Contents</h2>
  {toc}
</nav>
<main id="content">
{body}
</main>
<script>{js}</script>
</body>
</html>
"""


def main() -> None:
    if not SOURCE.exists():
        sys.exit(f"Error: source not found: {SOURCE}")

    raw = SOURCE.read_text(encoding="utf-8")
    processed = preprocess(raw)

    md = markdown.Markdown(
        extensions=[
            TocExtension(
                permalink=True,
                permalink_class="headerlink",
                toc_depth="1-4",
            ),
            "tables",
            "fenced_code",
            "attr_list",
            "footnotes",
        ],
    )

    body = md.convert(processed)
    toc_html = md.toc  # populated after convert(); sidebar version

    html = HTML_TEMPLATE.format(css=CSS, toc=toc_html, body=body, js=JS)
    OUTPUT.write_text(html, encoding="utf-8")

    size_kb = OUTPUT.stat().st_size / 1024
    print(f"Built: {OUTPUT}")
    print(f"  Source : {SOURCE}")
    print(f"  Output : {size_kb:.1f} KB")


if __name__ == "__main__":
    main()
