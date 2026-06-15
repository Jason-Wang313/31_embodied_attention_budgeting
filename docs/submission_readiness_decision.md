# Submission Readiness Decision

Decision: final for this batch pass as a v3 full-scale synthetic/mechanism paper.

## Why This Is Now Final For The Batch

- The manuscript renders to 25 pages without padding.
- The v3 suite represents 12,288,000 attention-control decisions over 8 families, 10 regimes, 12 policies, and 80 seeds.
- The comparison set is no longer only no-sensing, greedy, and budgeted attention; it includes periodic, threshold, fixed-budget, risk-coupled, horizon-aware, compute-aware, adaptive, myopic, oracle, and randomized policies.
- The paper reports success, collision, attention cost, information gain, horizon slack, risk exposure, and utility together.
- The suite includes cheap-attention, long-horizon, delayed-observation, noisy-sensor, model-mismatch, and over-budget controls.
- The final PDF exists only as the canonical Downloads artifact.

## Remaining Non-Claims

- No real robot validation.
- No measured sensing latency, motion cost, power, contact disturbance, or safety-margin consumption.
- No learned value-of-attention model.
- No high-fidelity POMDP or hardware active-sensing baseline.
- No claim that information gain is always wrong.

## Required Next Work For A Strong Hardware Submission

- Evaluate on a real perception-action task with measured sensing cost.
- Compare against cost-aware active sensing and POMDP/belief-space baselines.
- Learn or calibrate value-of-attention models from logs.
- Include regimes where greedy information gathering is correctly preferred.
