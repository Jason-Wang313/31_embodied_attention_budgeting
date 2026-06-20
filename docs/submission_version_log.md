# Submission Version Log

## v3 - 2026-06-15

- Wrote `docs/full_scale_execution_plan.md` before substantive v3 edits.
- Added `scripts/run_full_scale_attention_suite.py`.
- Generated full-scale outputs under `results/full_scale/`.
- Generated v3 figures under `figures/full_scale/`.
- Expanded `main.tex` into a 25-page final full-scale manuscript with v3 marker, full-scale results, controls, failure cases, reproducibility material, hardware protocols, and claim-boundary appendices.
- Built the canonical PDF at `C:/Users/wangz/Downloads/31.pdf`.
- Verified the v3 final PDF hash before the later visual-hardening rebuild.
- Verified local `main.pdf` was removed by the build script.

## v4 Visual Hardening - 2026-06-20

- Added the VLA role-model `hyperref` box policy to `main.tex`.
- Rebuilt the canonical Downloads PDF.
- Verified 25 pages, size 405,172 bytes, SHA256 `2091D545EA035DEBDAB6E8AC3DFDBC0240EE44186A5A58963773B821C05742CD`, and no local `main.pdf`.
- Verified one-point red internal link boxes on pages 5 and 6, with no cyan boxes. The manuscript has no cite/url link annotations, so green cite/url boxes are configured but not present.

## v2 - 2026-06-13

- Added horizon stress generation to `scripts/toy_attention_budget.py`.
- Generated `docs/toy_attention_horizon_stress.csv`.
- Generated `docs/toy_attention_horizon_stress_table.tex`.
- Updated the manuscript with a visible v2 note, horizon stress table, narrowed abstract, and stronger limitations.
- Added `scripts/build_pdf.ps1` to build, copy to Downloads, and remove local `main.pdf`.

## v1 - 2026-06-11

- Recovered initial embodied-attention-budgeting paper package with literature sweep, toy simulation, ICLR-style manuscript, final audit, canonical Downloads PDF, Desktop copy, and public GitHub repo.
