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
- [x] Canonical PDF is 25 pages and 353551 bytes.
- [x] Canonical PDF SHA256 is `88388E37C44F4B5EA946D4AA0F68843D83871D5EC972A8A017046E62F80194D2`.
- [x] Local `main.pdf` is removed after canonical copy.
- [x] `build_pdflatex2.log` has no overfull boxes, unresolved references, undefined citations, fatal errors, or TeX `!` errors.

Recommended verification commands:

```powershell
python scripts\run_full_scale_attention_suite.py
powershell -ExecutionPolicy Bypass -File scripts\build_pdf.ps1
pdfinfo C:\Users\wangz\Downloads\31.pdf
Get-FileHash -Algorithm SHA256 C:\Users\wangz\Downloads\31.pdf
Test-Path main.pdf
```
