# Embodied Attention Budgeting

Recovered paper package for robotics batch paper 31.

The project contains a broad arXiv-derived robotics literature sweep, novelty
notes, a small attention-budgeting simulation, and an anonymous ICLR-style
paper.

## Hardening Status

This is the v2 submission-hardened version. The added horizon stress shows the
boundary: at horizon 12, budgeted attention succeeds in 1,572/2,000 seeds while
greedy information gathering succeeds in 0/2,000; at horizon 16, greedy recovers
to 1,886/2,000 and beats the budgeted policy.

Build from the project root:

```powershell
python scripts/toy_attention_budget.py
powershell -ExecutionPolicy Bypass -File scripts/build_pdf.ps1
```

The batch output PDF is copied to `C:/Users/wangz/Downloads/31.pdf`.
