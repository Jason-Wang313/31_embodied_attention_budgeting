# Reproducibility Checklist

- [x] Full-scale runner is `scripts/run_full_scale_attention_suite.py`.
- [x] Build script is `scripts/build_pdf.ps1`.
- [x] Paper source is `main.tex`.
- [x] Full-scale CSV outputs are in `results/full_scale/seed_metrics.csv` and `results/full_scale/aggregate_metrics.csv`.
- [x] Full-scale summary is `results/full_scale/experiment_summary.json`.
- [x] Generated manuscript tables are in `results/full_scale/*.tex`.
- [x] Generated v3 figures are in `figures/full_scale/`.
- [x] Legacy v2 outputs remain in `docs/toy_attention_horizon_stress.csv` and `docs/toy_attention_horizon_stress_table.tex`.
- [x] Canonical PDF path is `C:/Users/wangz/Downloads/31.pdf`.
- [x] Canonical PDF is 25 pages and 405172 bytes.
- [x] Canonical PDF SHA256 is `2091D545EA035DEBDAB6E8AC3DFDBC0240EE44186A5A58963773B821C05742CD`.
- [x] Local `main.pdf` is removed after canonical copy.
- [x] `build_pdflatex2.log` has no overfull boxes, unresolved references, undefined citations, fatal errors, or TeX `!` errors.
- [x] VLA-style link-box policy is configured in `main.tex`; final PDF has one-point red internal reference boxes and no cyan boxes.

Recommended verification commands:

```powershell
python scripts\run_full_scale_attention_suite.py
powershell -ExecutionPolicy Bypass -File scripts\build_pdf.ps1
pdfinfo C:\Users\wangz\Downloads\31.pdf
Get-FileHash -Algorithm SHA256 C:\Users\wangz\Downloads\31.pdf
Test-Path main.pdf
```
