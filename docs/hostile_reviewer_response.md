# Hostile Reviewer Response

## Likely Rejection

This is active perception with a cost term, shown in a toy task where the horizon is chosen to punish greedy sensing. If sensing is cheap or the horizon is longer, information gain may be the right policy.

## Honest Response

We agree. The contribution is not a universal anti-information-gain result. It is a reminder that robot attention consumes physical control opportunity and must be priced against risk and horizon.

The v2 stress quantifies the boundary. At horizon 12, greedy sensing succeeds in 0/2,000 seeds because it spends five actions sensing and cannot finish. At horizon 16, greedy succeeds in 1,886/2,000 seeds, exceeding the budgeted policy's 1,572/2,000. The paper should claim finite-horizon, risk-coupled attention budgeting only.

## Required Upgrade For Main-Track Submission

- Evaluate on a real perception-action loop with measured sensing latency and motion cost.
- Compare against cost-aware active sensing and POMDP baselines.
- Learn or tune the risk proxy instead of hand-coding it.
- Report regimes where greedy information gathering is correctly preferred.
