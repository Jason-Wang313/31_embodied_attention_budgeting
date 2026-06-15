# Hostile Reviewer Response

## Likely Rejection

This is active perception or value of information with a cost term, evaluated in a synthetic suite. The oracle wins, and the deployable budgeted policies depend on hand-designed risk and cost models.

## Honest Response

That criticism is partly correct. The paper should not claim broad novelty over all cost-aware active perception. The defended contribution is narrower: attention can consume embodied control opportunity, and robotics evaluations should report task success, safety, attention cost, information gain, and horizon slack together.

The v3 suite strengthens the old toy claim. Across 12,288,000 represented attention-control decisions, greedy information succeeds in 39.1% of aggregate cases while spending 45.3 attention-cost units. Risk-coupled budgeting succeeds in 76.5% while spending 5.6 attention-cost units. Oracle value-of-attention succeeds in 82.9% and gives the best utility, showing the value of calibrated attention-cost models. Cheap-attention and long-horizon controls preserve the boundary where greedy information can recover.

## Required Upgrade For Main-Track Hardware Submission

- Evaluate on a real perception-action loop with measured sensing latency, motion cost, compute cost, or contact disturbance.
- Compare against cost-aware active sensing, POMDP, and belief-space planning baselines.
- Learn or tune value-of-attention models instead of hand-coding them.
- Report regimes where greedy information gathering is correctly preferred.
