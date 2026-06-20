# Child Status: Paper 31

Stage: complete; v3 final full-scale hardening ready to commit and push

Current facts:
- Literature sweep completed with `docs/related_work_matrix.csv` containing 2013 rows.
- Original toy simulator and v2 horizon stress artifacts are preserved for provenance.
- A paper-specific full-scale execution plan was written before substantive v3 edits at `docs/full_scale_execution_plan.md`.
- Full-scale suite is `scripts/run_full_scale_attention_suite.py`.
- Full-scale outputs are in `results/full_scale/`.
- The v3 suite covers 8 families, 10 regimes, 12 policies, 80 seeds, 160 steps per seed, and 12,288,000 represented attention-control decisions.
- Main v3 result: greedy information succeeds in 39.1% of aggregate cases with attention cost 45.3; risk-coupled budgeting succeeds in 76.5% with attention cost 5.6; oracle value-of-attention succeeds in 82.9% with utility cost 1.108.
- Negative controls remain explicit: low-attention-cost/long-horizon controls let greedy information recover, no-sensing fails on safety, and over-budget traps expose under-sensing.
- Paper source is `main.tex` with visible `v3 final full-scale` marker and 25 rendered pages.
- Canonical final PDF is `C:/Users/wangz/Downloads/31.pdf` with SHA256 `2091D545EA035DEBDAB6E8AC3DFDBC0240EE44186A5A58963773B821C05742CD`.
- Final PDF size is 405172 bytes.
- Latest visual hardening: VLA-style one-point red internal link boxes verified on pages 5 and 6; green cite/url border policy configured, with no cite/url annotations present in this manuscript.
- Transient `main.pdf` was removed by `scripts/build_pdf.ps1`.
- Public GitHub repo exists: `https://github.com/Jason-Wang313/31_embodied_attention_budgeting`.

Commands run:
- `python scripts\run_full_scale_attention_suite.py`
- `pdflatex -interaction=nonstopmode -halt-on-error main.tex` twice for local page-count QA
- `powershell -ExecutionPolicy Bypass -File scripts\build_pdf.ps1`
- Safe probes for build status, Downloads PDF, local PDF absence, LaTeX log status, PDF text markers, page count, file size, and SHA256 hash.

Historical failures:
- Original child attempt timed out during an unbounded template search.
- V1 was manually recovered by copying local ICLR style files and compiling directly.
- V2 was useful but short and toy-scale; v3 replaces it with a broader full-scale synthetic manuscript.

Next:
- Commit and push the v3 hardening update.
