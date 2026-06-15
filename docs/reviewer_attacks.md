# Reviewer Attacks

1. This is active perception with a cost term.
2. The budget and utility weights are hand-designed.
3. The suite is synthetic, not a robot.
4. The oracle is not deployable.
5. The comparison set still lacks a full POMDP/belief-space planner.
6. The method depends on custom risk and attention-cost estimates.
7. The benefit may disappear if sensing is cheap.
8. The policy may be overly conservative and under-sense.
9. The paper confuses uncertainty reduction with safety.
10. The finite-horizon setup can punish greedy sensing.
11. Expected rollouts may smooth rare catastrophic events.

## Responses

- Keep novelty to embodied control-opportunity accounting, not all active perception.
- Report the cheap-attention and long-horizon controls where greedy information recovers.
- Report the over-budget trap where conservative attention fails.
- Treat the oracle as an upper reference only.
- State that hardware validation and stronger planning baselines are required for the next claim level.
- Preserve the v2 horizon stress as provenance.
