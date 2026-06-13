# Submission Readiness Decision

Decision: workshop-only / strong-revise.

## Why Not Submit-Ready

- Evidence is a toy one-dimensional hazard task.
- The budgeted policy is hand-coded.
- V2 shows the advantage depends on a tight horizon.
- There is no measured sensing latency, motion cost, power, or safety-margin consumption.
- There is no comparison to POMDP or cost-aware active sensing baselines.

## Why Not Kill

- The embodied-attention framing is clear and useful for robot perception-action loops.
- The toy task cleanly separates information gain from control opportunity.
- The v2 stress makes the finite-horizon boundary explicit.
- The claim is narrow enough after hardening.

## Required Next Work

- Evaluate on a real perception-action task with measured sensing cost.
- Compare against cost-aware active sensing/POMDP baselines.
- Learn or calibrate the risk-coupled budget rule.
- Include regimes where greedy information gathering is the correct choice.
