# Learnings Log — LogSift

## 2026-07-16 — Report/stats keyword mismatch after refactor
- Symptom: TypeError: top_endpoints() got an unexpected keyword argument 'n' (report tests red).
- Root cause: refactor renamed the parameter to `limit`; report.py call site never migrated.
- Fix: report.py:21 now calls `top_endpoints(entries, limit=top)`.
- Prevention: intent rule recorded — tests define the signature (3 test call sites used
  `limit`); migrate stale minority call sites forward, never rename back.
- Keywords: unexpected keyword argument, top_endpoints, limit, n

## 2026-07-16 — Query strings counted as separate endpoints
- Symptom: top endpoints listed /search?q=desk and /search?q=lamp separately; README promises
  they both count toward /search.
- Root cause: top_endpoints counted raw entry.path; stripping was lost in the refactor.
- Fix: stats.py top_endpoints groups by `entry.path.split("?", 1)[0]`.
- Prevention: invariant in PROJECT-MAP.md — stripping lives in stats, parser keeps raw paths
  (a parser test enforces the latter).
- Keywords: query string, top endpoints, grouping, split

## 2026-07-16 — Test helper import masked 10 tests
- Symptom: ModuleNotFoundError: No module named 'logsift.utils'; only 9 of 19 tests ran.
- Root cause: utils.py was renamed timeutil.py; tests/helpers.py import never migrated —
  the import error prevented two whole test modules from loading, hiding their failures.
- Fix: tests/helpers.py imports from logsift.timeutil.
- Prevention: repair discipline — fix first masking error, RE-RUN to get the true failure
  list before planning further fixes; watch the "N tests ran" count as evidence.
- Keywords: ModuleNotFoundError, logsift.utils, timeutil, masked failures, import error
