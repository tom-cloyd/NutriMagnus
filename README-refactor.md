# Running this refactor

Recommended setup:

```bash
cd numa_llm_refactor
./scripts/setup_venv.sh
source .venv/bin/activate
python numa.py
```

Quick run without activating the venv:

```bash
./scripts/run_numa.sh
```

This build intentionally removes `typer` and uses only the Python standard library plus `rich`.

---

# numa offline-friendly refactor

This refactor splits the original monolithic `numa.py` into smaller modules that are easier for a local coding model to handle.

## Layout

- `numa.py` — thin CLI entrypoint
- `db.py`, `usda.py`, `diaas.py`, `export.py`, `profile.py` — original support modules copied intact
- `numa_app/state.py` — shared UI/app state and the lightweight `AppContext`
- `numa_app/config/` — theme and preference persistence
- `numa_app/ui/` — prompting, common menu helpers, rich render helpers
- `numa_app/services/` — food search, portion parsing, report export support
- `numa_app/workflows/` — foods, pantry, recipes, meals, summary, settings menus

## Design goal

The split is intentionally pragmatic:
- preserve behavior
- reduce file size
- keep menu/workflow logic separate from lower-level helpers
- make it easier to work on one feature area at a time in an offline LLM setup

## Smoke checks performed

- imports resolve
- package compiles with `python -m compileall`
- `python numa.py --help` works

## Still recommended in your real repo

Once you drop this into the real project, test these interactive paths manually:
- food search and portion analysis
- recipe create/view/edit
- meal log/analyze
- daily summary
- settings changes for theme, API key, and dietary preferences

