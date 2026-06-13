# Reproducibility Checklist

- [x] Main simulator is `scripts/toy_attention_budget.py`.
- [x] Build script is `scripts/build_pdf.ps1`.
- [x] Main output is `docs/toy_attention_budget_results.csv`.
- [x] V2 outputs are `docs/toy_attention_horizon_stress.csv` and `docs/toy_attention_horizon_stress_table.tex`.
- [x] Paper source is `main.tex`.
- [x] Canonical PDF path is `C:/Users/wangz/Downloads/31.pdf`.
- [x] Local `main.pdf` is removed after canonical copy.
- [x] Visible Desktop PDF copies are absent.

Recommended verification commands:

```powershell
python scripts\toy_attention_budget.py
powershell -ExecutionPolicy Bypass -File scripts\build_pdf.ps1
```
