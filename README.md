# Embodied Attention Budgeting

Recovered and v3 submission-hardened package for robotics batch paper 31.

The project contains a broad robotics literature sweep, novelty/audit notes,
the original toy attention-budgeting simulation, a RAM-light full-scale
synthetic suite, and a 25-page anonymous ICLR-style manuscript.

## Hardening Status

This is the v3 final full-scale version. The new suite represents 12,288,000
attention-control decisions across 8 dynamics families, 10 regimes, 12 policies,
80 seeds, and 160 steps per seed. Greedy information gathering succeeds in
39.1% of aggregate cases while spending 45.3 attention-cost units. Risk-coupled
budgeting succeeds in 76.5% while spending 5.6 attention-cost units. The oracle
value-of-attention policy succeeds in 82.9% and achieves the best utility cost,
1.108.

Build from the project root:

```powershell
python scripts\run_full_scale_attention_suite.py
powershell -ExecutionPolicy Bypass -File scripts\build_pdf.ps1
```

The canonical final PDF is `C:/Users/wangz/Downloads/31.pdf`.
The final build removes the transient local `main.pdf`.
VLA-style visual hardening is applied: one-point red internal link boxes are verified on pages 5 and 6, with no cyan boxes. The manuscript has no cite/url link annotations, so green cite/url boxes are configured but not artificially introduced.
