# Child Status: Paper 31

Stage: complete; v2 submission hardening ready to commit and push

Current facts:
- Literature sweep completed with `docs/related_work_matrix.csv` containing 2013 rows.
- Main toy simulator regenerated `docs/toy_attention_budget_results.csv`.
- Main horizon-12 result: greedy sensing succeeds in 0/2000 seeds while budgeted attention succeeds in 1572/2000.
- V2 horizon stress generated `docs/toy_attention_horizon_stress.csv` and `docs/toy_attention_horizon_stress_table.tex`.
- V2 stress result: at horizon 16, greedy sensing succeeds in 1886/2000 seeds and beats budgeted attention's 1572/2000 successes.
- Paper source is `main.tex` with visible v2 note, horizon stress table, and narrowed limitations.
- LaTeX build completed with `scripts/build_pdf.ps1`.
- Final PDF copied to `C:/Users/wangz/Downloads/31.pdf`.
- Transient `main.pdf` removed so the final PDF exists only at the required Downloads path.
- Checked Desktop paths contain no `31.pdf`.
- Public GitHub repo exists: `https://github.com/Jason-Wang313/31_embodied_attention_budgeting`.
- `docs/final_audit.md` exists and reports build status, v2 stress evidence, Downloads-only artifact status, Desktop absence, and local PDF absence.

Commands run:
- `python scripts\toy_attention_budget.py`
- `powershell -ExecutionPolicy Bypass -File scripts\build_pdf.ps1`
- Safe probes for build status, Downloads PDF, Desktop absence, local PDF absence, LaTeX log status, and generated stress outputs.

Historical failures:
- Original child attempt timed out during an unbounded template search.
- V1 was manually recovered by copying local ICLR style files and compiling directly.

Recovery / hardening steps:
- Added v2 horizon stress and narrowed the claim to finite-horizon, risk-coupled attention budgeting.
- Added standard hardening docs: attack log, version log, hostile reviewer response, rigor checklist, reproducibility checklist, and readiness decision.
- Added `scripts/build_pdf.ps1` and `.gitignore` rule for `main.pdf`.
- Rebuilt the canonical PDF and removed the tracked local PDF.

Next:
- Commit and push the v2 hardening update.
