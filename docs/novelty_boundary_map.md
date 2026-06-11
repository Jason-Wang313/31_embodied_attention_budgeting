# Novelty Boundary Map

## Core boundary

Not novel:

- choosing a next best view,
- adding uncertainty estimates,
- adding active learning,
- adding a verifier,
- combining perception and control modules,
- using RL to jointly optimize sensing and control,
- or increasing sensor/model scale.

Potentially novel:

- making sensing itself a consumable embodied budget,
- coupling the sensing budget to control risk,
- showing that the robot sometimes should not attend even when information is available,
- and demonstrating that the best policy can spend its limited attention on risk management rather than on entropy reduction.

## Boundary broken by the paper

The paper should break the assumption that "more attention is always better if it improves belief quality."

Instead, it should show that:

1. attention can be exhausted,
2. exhausting it changes downstream controllability,
3. and the optimal policy can ration attention to preserve safe action options.

## What must be demonstrated

- A setting where the same information gain can be achieved with different risk costs.
- A case where standard active perception chooses an unsafe or wasteful sensing action.
- A policy that performs better because it budgets attention, not because it sees more.

## If this cannot be shown

Then the project collapses back into ordinary active perception and should be revised or killed.
