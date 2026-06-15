# Claims

## Main claim

A robot can behave more safely and usefully if sensing is treated as a budgeted embodied action whose consumption is coupled to control risk, attention cost, and remaining horizon slack.

## Supported v3 subclaims

1. Greedy information gathering can over-spend embodied control opportunity even when each observation is informative.
2. Risk-coupled attention budgeting can succeed with less information by preserving time, motion, contact, and compute opportunity.
3. In the v3 suite, greedy information succeeds in 39.1% of aggregate cases and spends 45.3 attention-cost units.
4. In the v3 suite, risk-coupled budgeting succeeds in 76.5% of aggregate cases and spends 5.6 attention-cost units.
5. The oracle value-of-attention policy succeeds in 82.9% and achieves best utility cost, 1.108.
6. Cheap-attention and long-horizon controls show that greedy information can recover when attention is affordable.
7. Over-budget traps show that budgeted attention can fail by under-sensing.

## Unsupported claims to avoid

- "This solves active perception."
- "This is the first work to ever budget attention."
- "The robot is universally more intelligent."
- "This generalizes to all embodiments without evidence."
- "Information gain is always the wrong objective."
- "The v3 suite is hardware validation."

## Evidence required for the next claim level

- measured sensing latency, motion cost, contact disturbance, or compute cost;
- hardware comparison against greedy information and budgeted attention;
- cheap-attention and under-sensing controls;
- calibrated value-of-attention model;
- and paired failure analysis.
