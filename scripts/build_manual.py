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
PAGE_TITLE = "NutriMagnus User Manual"
WORDS_PER_MINUTE = 225

# Matches a markdown heading that ends with a [short-anchor] tag.
# Groups: (hashes, title_text, anchor)
_ANCHOR_RE = re.compile(
    r'^(#{1,6})\s+(.+?)\s+\[([a-z][a-z0-9-]*)\]\s*$',
    re.MULTILINE,
)

# The manual's second line: "*Updated YYYY-MM-DD:HHMM* / Reading time: ..."
# The timestamp is bumped by hand per CLAUDE.md convention; only the reading
# time portion is regenerated here.
_HEADER_LINE_RE = re.compile(
    r'^(\*Updated \d{4}-\d{2}-\d{2}:\d{4}\*) / Reading time: .+$',
    re.MULTILINE,
)


def preprocess(text: str) -> str:
    """Strip [anchor] from heading display text; inject {#anchor} for attr_list."""
    def _replace(m: re.Match) -> str:
        hashes, title, anchor = m.group(1), m.group(2).strip(), m.group(3)
        return f'{hashes} {title} {{#{anchor}}}'
    return _ANCHOR_RE.sub(_replace, text)


def count_words(markdown_text: str) -> int:
    """Word count of the manual body, ignoring code and link targets."""
    text = _HEADER_LINE_RE.sub('', markdown_text, count=1)
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    text = re.sub(r'`[^`]*`', '', text)
    text = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', text)
    return len(text.split())


def reading_time_str(word_count: int, wpm: int = WORDS_PER_MINUTE) -> str:
    total_minutes = max(1, round(word_count / wpm))
    hours, minutes = divmod(total_minutes, 60)
    parts = []
    if hours:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    return ", ".join(parts)


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
    display: flex;
    flex-direction: column;
    padding: 1.25rem 0.75rem 1.5rem 0.5rem;
    border-right: 1px solid var(--border);
    background: var(--bg);
    font-size: 14.5px;
    line-height: 1.4;
}
/* Everything from "Contents" down scrolls in its own region — the page
   title and search box above it stay put no matter how far the current-
   section link below has scrolled. */
#toc-scroll {
    flex: 1;
    min-height: 0;
    overflow-y: auto;
}
#toc-sidebar .toc-page-title {
    display: block;
    font-size: 15.5px;
    font-weight: 700;
    color: var(--heading);
    text-decoration: none;
    padding: 0.1rem 0.2rem 0.6rem;
    margin-bottom: 0.6rem;
    border-bottom: 1px solid var(--border);
}
#toc-sidebar .toc-page-title:hover { color: var(--accent); }
#toc-sidebar h2 {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.5em;
    font-size: 11.5px;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--muted);
    margin-top: 0;
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

/* Currently-visible section, kept in sync with scroll position */
#toc-sidebar .toc a.toc-current {
    background: var(--accent-light);
    color: var(--accent);
    font-weight: 600;
    box-shadow: inset 2px 0 0 var(--accent);
}

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
#search-func-toggle {
    display: flex;
    align-items: center;
    gap: 0.35em;
    font-size: 13px;
    color: var(--muted);
    margin-top: 6px;
    cursor: pointer;
}
#search-func-toggle input { margin: 0; cursor: pointer; }
#search-results {
    list-style: none;
    margin: 6px 0 0;
    max-height: 220px;
    overflow-y: auto;
}
#search-results li { margin: 0; padding: 0; }
#search-results a {
    display: block;
    padding: 3px 6px;
    border-radius: 3px;
    color: var(--toc-fg);
    text-decoration: none;
    font-size: 12.5px;
}
#search-results a:hover { background: var(--accent-light); color: var(--accent); }
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
#search-howto-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.5em;
    margin-top: 6px;
}
.search-howto-link {
    display: inline-block;
    font-size: 12.5px;
}

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
/* ── Section search: AND-of-words over whole sections, not raw substring
   highlighting over the whole document. See "Using this manual's search"
   (#search-howto) for the user-facing explanation of why. ── */
(function () {
  var VERBS = ['add', 'click', 'link', 'edit', 'set', 'type', 'change', 'pick',
               'check', 'create', 'enter', 'archive', 'save', 'choose', 'scale',
               'delete', 'copy', 'select', 'import', 'remove', 'restore',
               'override', 'toggle', 'fill', 'weigh', 'update', 'rename',
               'paste', 'export'];

  var sections = [], resultItems = [], currentWords = [];
  var openSection = null, sectionMatches = [], idx = 0;
  var input, funcCheckbox, resultsEl;

  function buildSectionIndex() {
    var headings = Array.prototype.slice.call(
      document.querySelectorAll('#content h1[id], #content h2[id], #content h3[id], #content h4[id]')
    );
    return headings.map(function (h, i) {
      var next = headings[i + 1] || null;
      var text = h.textContent;
      var el = h.nextElementSibling;
      while (el && el !== next) { text += ' ' + el.textContent; el = el.nextElementSibling; }
      return {
        id: h.id,
        title: h.textContent.replace(/\\u00b6/g, '').trim(),
        el: h,
        nextEl: next,
        text: text.toLowerCase(),
      };
    });
  }

  function elementsBetween(start, end) {
    var els = [];
    var el = start.nextElementSibling;
    while (el && el !== end) { els.push(el); el = el.nextElementSibling; }
    return els;
  }

  function countOccurrences(haystack, needle) {
    if (!needle) return 0;
    var count = 0, pos = 0;
    while ((pos = haystack.indexOf(needle, pos)) !== -1) { count++; pos += needle.length; }
    return count;
  }

  function scoreOf(section, words) {
    var score = 0;
    words.forEach(function (w) {
      score += countOccurrences(section.text, w);
      if (section.title.toLowerCase().indexOf(w) !== -1) score += 5;
    });
    return score;
  }

  function setCount(txt) { document.getElementById('search-count').textContent = txt; }

  function closeSectionHighlights() {
    document.querySelectorAll('mark.search-hit').forEach(function (m) {
      var t = document.createTextNode(m.textContent);
      m.parentNode.replaceChild(t, m);
      t.parentNode.normalize();
    });
    sectionMatches = []; idx = 0;
  }

  function highlightWordInRoot(root, word) {
    var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
      acceptNode: function (n) {
        return n.parentElement.closest('script,style,mark,.headerlink') ?
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
      while ((start = lower.indexOf(word, pos)) !== -1) {
        if (start > pos) frags.push(document.createTextNode(text.slice(pos, start)));
        var mark = document.createElement('mark');
        mark.className = 'search-hit';
        mark.textContent = text.slice(start, start + word.length);
        frags.push(mark);
        sectionMatches.push(mark);
        pos = start + word.length;
      }
      if (frags.length) {
        if (pos < text.length) frags.push(document.createTextNode(text.slice(pos)));
        var parent = node.parentNode;
        frags.forEach(function (f) { parent.insertBefore(f, node); });
        parent.removeChild(node);
      }
    });
  }

  function scrollToMark(i) {
    sectionMatches.forEach(function (m, j) {
      m.className = j === i ? 'search-hit search-current' : 'search-hit';
    });
    if (sectionMatches[i]) sectionMatches[i].scrollIntoView({ behavior: 'smooth', block: 'center' });
    setCount(sectionMatches.length ? (i + 1) + ' / ' + sectionMatches.length + ' in this section' : 'no matches in this section');
  }

  function openResult(item) {
    closeSectionHighlights();
    openSection = item.section;
    var roots = [openSection.el].concat(elementsBetween(openSection.el, openSection.nextEl));
    currentWords.forEach(function (w) {
      roots.forEach(function (r) { highlightWordInRoot(r, w); });
    });
    sectionMatches.sort(function (a, b) {
      var pos = a.compareDocumentPosition(b);
      return (pos & Node.DOCUMENT_POSITION_FOLLOWING) ? -1 : 1;
    });
    openSection.el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    idx = 0;
    if (sectionMatches.length) scrollToMark(0);
    else setCount('no matches in this section');
  }

  var RESULT_CAP = 25;

  function renderResults(items, funcMode) {
    resultsEl.innerHTML = '';
    if (!currentWords.length) { setCount(''); return; }
    if (!items.length) {
      setCount(funcMode ? 'No sections match (try unchecking the box above)' : 'No sections match');
      return;
    }
    var shown = items.slice(0, RESULT_CAP);
    var msg = items.length + (items.length === 1 ? ' section matches' : ' sections match');
    if (items.length > RESULT_CAP) msg += ' (showing top ' + RESULT_CAP + ')';
    msg += ' \\u2014 pick one, or press Enter';
    setCount(msg);
    shown.forEach(function (item) {
      var li = document.createElement('li');
      var a = document.createElement('a');
      a.href = '#' + item.section.id;
      a.textContent = item.section.title;
      a.addEventListener('click', function (e) {
        e.preventDefault();
        openResult(item);
        history.replaceState(null, '', '#' + item.section.id);
      });
      li.appendChild(a);
      resultsEl.appendChild(li);
    });
  }

  function runSearch() {
    var query = input.value.trim();
    currentWords = query.length < 2 ? [] : query.toLowerCase().split(/\\s+/).filter(Boolean);
    closeSectionHighlights();
    openSection = null;
    var funcMode = funcCheckbox.checked;
    if (!currentWords.length) {
      resultItems = [];
      renderResults(resultItems, funcMode);
      return;
    }
    resultItems = sections.filter(function (s) {
      var allPresent = currentWords.every(function (w) { return s.text.indexOf(w) !== -1; });
      if (!allPresent) return false;
      if (funcMode) return VERBS.some(function (v) { return s.text.indexOf(v) !== -1; });
      return true;
    }).map(function (s) {
      return { section: s, score: scoreOf(s, currentWords) };
    }).sort(function (a, b) { return b.score - a.score; });
    renderResults(resultItems, funcMode);
  }

  function step(dir) {
    if (!openSection) { if (resultItems.length) openResult(resultItems[0]); return; }
    if (!sectionMatches.length) return;
    idx = (idx + dir + sectionMatches.length) % sectionMatches.length;
    scrollToMark(idx);
  }

  document.addEventListener('DOMContentLoaded', function () {
    sections = buildSectionIndex();
    input = document.getElementById('search-input');
    funcCheckbox = document.getElementById('search-func-mode');
    resultsEl = document.getElementById('search-results');
    var timer;
    input.addEventListener('input', function () {
      clearTimeout(timer);
      timer = setTimeout(runSearch, 180);
    });
    funcCheckbox.addEventListener('change', runSearch);
    input.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') { e.preventDefault(); step(e.shiftKey ? -1 : 1); }
      if (e.key === 'Escape') {
        input.value = '';
        currentWords = []; resultItems = []; openSection = null;
        closeSectionHighlights();
        resultsEl.innerHTML = '';
        setCount('');
      }
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
      /* Clicking the heading text itself also expands a collapsed section
         (in addition to navigating to it) so it doesn't look "stuck" shut. */
      a.addEventListener('click', function () {
        if (li.classList.contains('toc-collapsed')) {
          li.classList.remove('toc-collapsed');
          btn.textContent = '▾';
        }
      });
    });

    if (!mainLis.length) return;

    var header = document.querySelector('#search-howto-row');
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

/* ── TOC scroll-spy: highlight the section currently on screen ── */
(function () {
  document.addEventListener('DOMContentLoaded', function () {
    var headings = Array.prototype.slice.call(
      document.querySelectorAll('#content h1[id], #content h2[id], #content h3[id], #content h4[id]')
    );
    if (!headings.length) return;

    var tocLinks = {};
    document.querySelectorAll('#toc-sidebar .toc a[href^="#"]').forEach(function (a) {
      var id = decodeURIComponent(a.getAttribute('href').slice(1));
      tocLinks[id] = a;
    });

    var current = null;
    var OFFSET = 100; /* px from top of viewport treated as the "reading line" */

    function expandAncestors(link) {
      var li = link.closest('li');
      while (li) {
        var parentLi = li.parentElement && li.parentElement.closest('li.toc-collapsed');
        if (!parentLi) break;
        parentLi.classList.remove('toc-collapsed');
        var btn = parentLi.querySelector(':scope > .toc-toggle');
        if (btn) btn.textContent = '▾';
        li = parentLi;
      }
    }

    function activate(id) {
      if (id === current || !tocLinks[id]) return;
      if (current && tocLinks[current]) tocLinks[current].classList.remove('toc-current');
      current = id;
      var link = tocLinks[id];
      link.classList.add('toc-current');
      expandAncestors(link);
      link.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    }

    function update() {
      var activeId = headings[0].id;
      for (var i = 0; i < headings.length; i++) {
        if (headings[i].getBoundingClientRect().top <= OFFSET) {
          activeId = headings[i].id;
        } else {
          break;
        }
      }
      /* Near the bottom of the page, force the last heading active even if
         its top never crosses OFFSET (happens with a short final section). */
      if (window.innerHeight + window.scrollY >= document.body.scrollHeight - 2) {
        activeId = headings[headings.length - 1].id;
      }
      activate(activeId);
    }

    var ticking = false;
    window.addEventListener('scroll', function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () { update(); ticking = false; });
    }, { passive: true });
    window.addEventListener('resize', update);

    update();
  });
})();
"""

HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
{css}
</style>
</head>
<body>
<nav id="toc-sidebar" aria-label="Table of contents">
  <a class="toc-page-title" href="#content">{title}</a>
  <div id="search-box">
    <input id="search-input" type="search" placeholder="Search manual… (all words must match)"
           autocomplete="off" spellcheck="false">
    <label id="search-func-toggle">
      <input type="checkbox" id="search-func-mode">
      Only show things you can do
    </label>
    <ul id="search-results"></ul>
    <div id="search-nav">
      <span id="search-count"></span>
      <button class="search-btn" id="btn-prev" title="Previous match in open section (Shift+Enter)">&#x25B2;</button>
      <button class="search-btn" id="btn-next" title="Next match in open section (Enter)">&#x25BC;</button>
    </div>
    <div id="search-howto-row">
      <a class="search-howto-link" href="#search-howto">How does this search work?</a>
    </div>
  </div>
  <div id="toc-scroll">
    <h2>Contents</h2>
    {toc}
  </div>
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

    word_count = count_words(raw)
    reading_time = reading_time_str(word_count)
    updated_raw, n = _HEADER_LINE_RE.subn(
        lambda m: f"{m.group(1)} / Reading time: {reading_time}", raw, count=1
    )
    if n and updated_raw != raw:
        SOURCE.write_text(updated_raw, encoding="utf-8")
        raw = updated_raw

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

    html = HTML_TEMPLATE.format(css=CSS, toc=toc_html, body=body, js=JS, title=PAGE_TITLE)
    OUTPUT.write_text(html, encoding="utf-8")

    size_kb = OUTPUT.stat().st_size / 1024
    print(f"Built: {OUTPUT}")
    print(f"  Source : {SOURCE}")
    print(f"  Output : {size_kb:.1f} KB")
    print(f"  Words  : {word_count} ({reading_time} reading time @ {WORDS_PER_MINUTE} wpm)")


if __name__ == "__main__":
    main()
