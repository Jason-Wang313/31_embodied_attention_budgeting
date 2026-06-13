# Experiment Rigor Checklist

- [x] Main simulator is `scripts/toy_attention_budget.py`.
- [x] Main run uses 2,000 deterministic seeds.
- [x] Baselines include no sensing, greedy information gathering, and budgeted attention.
- [x] Main metrics include success, collisions, return, attention used, and information.
- [x] V2 horizon stress attacks the finite-horizon assumption.
- [x] Negative boundary is explicit: at horizon 16, greedy reaches 1,886/2,000 successes and beats budgeted attention.
- [ ] No hardware validation.
- [ ] No high-fidelity embodied perception simulator.
- [ ] No learned risk proxy.
- [ ] No POMDP or cost-aware active sensing baseline.

Decision: mechanism evidence only; terminal state is workshop-only / strong-revise.
