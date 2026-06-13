# Claims

## Main claim

A robot can behave more safely and usefully if sensing is treated as a budgeted embodied action whose consumption is coupled to control risk.

## Subclaims

1. Standard active perception overvalues information gain when sensing has hidden physical cost.
2. A budgeted attention controller can choose safer action sequences even when it gathers less information overall.
3. The benefit comes from coupling sensing to risk, not from better prediction or a larger model.
4. The same principle applies across visual and tactile sensing modes.
5. V2 shows the boundary: when the control horizon grows to 16, greedy sensing succeeds in 1,886/2,000 seeds and beats the budgeted policy's 1,572/2,000 successes.

## Unsupported claims to avoid

- "This solves active perception."
- "This is the first work to ever budget attention."
- "The robot is universally more intelligent."
- "This generalizes to all embodiments without evidence."
- "Information gain is always the wrong objective."

## Evidence required

- runnable simulation,
- ablation against a standard information-gain policy,
- adversarial case where free attention fails,
- and at least one failure mode where the proposed budget can still be too conservative.
