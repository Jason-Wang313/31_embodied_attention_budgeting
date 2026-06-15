# Experiment Rigor Checklist

- [x] A paper-specific v3 execution plan was written before substantive full-scale edits.
- [x] Full-scale runner is `scripts/run_full_scale_attention_suite.py`.
- [x] Full-scale suite covers 8 embodied attention dynamics families.
- [x] Full-scale suite covers 10 regimes, including cheap-attention, delayed-observation, model-mismatch, and over-budget controls.
- [x] Full-scale suite compares 12 policies.
- [x] Full-scale suite uses 80 seeds and 12,288,000 represented attention-control decisions.
- [x] Baselines include no-sensing, greedy information, periodic sensing, uncertainty thresholding, fixed budget, risk-coupled budget, horizon-aware budget, compute-aware budget, adaptive budget, myopic utility, oracle value-of-attention, and randomized budget.
- [x] Metrics include success, collision, return, attention used, attention cost, information gain, uncertainty, horizon slack, missed-control cost, risk exposure, and utility.
- [x] Negative controls are explicit: cheap attention, long horizon, no sensing, and over-budget trap.
- [x] Figures include attention cost, success/cost Pareto view, and regime winners.
- [x] Tables include scale, main performance, family summary, regime winners, controls/failures, and legacy v2 horizon stress.
- [ ] No hardware validation.
- [ ] No high-fidelity embodied perception simulator.
- [ ] No learned risk proxy or POMDP baseline.

Decision: final for the batch pass as a full-scale synthetic/mechanism paper; hardware claims remain out of scope.
