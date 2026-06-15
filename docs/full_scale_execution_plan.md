# Paper31 Full-Scale Execution Plan

## Current Claim

Paper31 argues that attention is an embodied resource: sensing, probing, view changes, high-resolution inference, and tactile checks consume finite control opportunity. The current v2 manuscript demonstrates the idea with one one-dimensional hazard task and a horizon stress. The key v2 result is useful but narrow: at horizon 12, greedy sensing succeeds in 0/2000 seeds while budgeted attention succeeds in 1572/2000; at horizon 16, greedy recovers and beats the budgeted policy.

The v3 paper must keep this honesty but dramatically expand the evidence. The final claim should be: when sensing actions consume time, safety margin, energy, compute, contact opportunity, or motion budget, attention policies should be evaluated on task success, risk, return, attention cost, horizon slack, and information gain together. Greedy information gain is not wrong in general; it is incomplete when control opportunity is scarce.

## Gaps To Close

1. The existing experiment has one dynamics family and three policies.
2. The existing stress only changes horizon length.
3. The claim is vulnerable to active-perception priors that already price information by cost.
4. The manuscript is far below the final page threshold.
5. There are no figures showing tradeoffs, family-level behavior, or regime boundaries.
6. There is no cheap-attention control where greedy sensing should be allowed to win.
7. There is no over-budget failure showing that budgeted attention can become too conservative.
8. There is no model-mismatch or delayed-observation stress.
9. There is no explicit hardware evaluation template for measuring embodied attention cost.

## Target Full-Scale Experiment

Create `scripts/run_full_scale_attention_suite.py` using only the Python standard library. Write outputs to `results/full_scale/` and figures to `figures/full_scale/`. The suite should stream metrics and avoid storing per-step trajectories except a small representative trace.

Target scale:

- 8 dynamics families
- 10 regimes
- 12 attention policies
- 80 deterministic seeds
- 160 represented decision steps per seed
- 12,288,000 represented attention-control decisions

The scale can be implemented as a real streaming loop if runtime is reasonable. If a full per-step loop becomes too slow, use deterministic closed-form or semi-analytic expected metrics for aggregate rows, but preserve explicit representative traces for auditability.

## Dynamics Families

1. `hazard_navigation`: finite-horizon navigation through a risky cell.
2. `occluded_corridor`: view changes reveal blocked paths but consume travel time.
3. `tactile_probe_manipulation`: probing reduces grasp uncertainty but can disturb contact.
4. `mobile_viewpoint_selection`: camera motion improves belief but shifts the robot away from a goal path.
5. `compute_latency_control`: high-resolution inference reduces perception error but delays control.
6. `multi_sensor_scheduling`: visual, tactile, and proprioceptive channels have different costs and risk reductions.
7. `dynamic_obstacle_tracking`: sensing improves obstacle estimates while the obstacle keeps moving.
8. `cheap_attention_control`: sensing is nearly free, so greedy information gathering should often be competitive or best.

## Regimes

1. `tight_horizon`: sensing consumes scarce control time.
2. `long_horizon`: enough slack for greedy sensing to recover.
3. `high_hazard`: uncertainty has large collision cost.
4. `low_hazard`: risk is mild and attention spending should be conservative.
5. `high_attention_cost`: sensing consumes large time, power, or motion budget.
6. `low_attention_cost`: sensing is cheap and information-gain methods should perform well.
7. `delayed_observation`: sensing result arrives after a delay.
8. `noisy_sensor`: attention reduces uncertainty less reliably.
9. `model_mismatch`: the policy's risk model is biased relative to the environment.
10. `over_budget_trap`: overly conservative attention budgets fail because they refuse necessary sensing.

## Policies / Baselines

1. `no_sensing`: never spends attention.
2. `greedy_info`: senses whenever expected information gain is high.
3. `periodic_sensing`: senses on a fixed cadence.
4. `uncertainty_threshold`: senses when uncertainty crosses a threshold.
5. `fixed_budget`: spends a fixed number of early sensing actions.
6. `risk_coupled_budget`: senses only when expected risk reduction exceeds embodied attention cost.
7. `horizon_aware_budget`: additionally prices remaining horizon slack.
8. `compute_aware_budget`: prices inference latency separately from physical sensing.
9. `adaptive_budget`: updates attention cost from recent outcomes.
10. `myopic_utility`: maximizes immediate risk reduction minus attention cost.
11. `oracle_value_of_attention`: uses true environment parameters as an upper reference.
12. `randomized_budget`: randomized debounce/control baseline.

## Metrics

For each seed-level row record:

- success
- collision or safety violation
- average return / utility
- attention actions used
- embodied attention cost
- information gained
- final uncertainty
- horizon slack
- missed-control cost
- risk exposure
- family, regime, method, and seed identifiers

For aggregate rows record means, standard errors, win rates, and failure rates.

## Ablations And Stress Tests

1. Horizon sweep: show when greedy information gathering recovers.
2. Attention-cost sweep: show the boundary between cheap and expensive sensing.
3. Risk-coupling ablation: compare information-only, cost-only, and risk-cost policies.
4. Delay ablation: show that late information can be less useful than less information now.
5. Model-mismatch ablation: measure degradation when risk estimates are biased.
6. Over-budget ablation: show failure when attention is rationed too aggressively.
7. Cheap-attention control: confirm the framework does not blindly punish sensing.
8. Sensor-noise stress: test whether repeated sensing is useful or wasteful.

## Figures And Tables

Generate manuscript-ready artifacts:

- `full_scale_scale.tex`: families, regimes, methods, seeds, steps, decisions.
- `full_scale_main_performance.tex`: main method comparison.
- `full_scale_family_summary.tex`: family-level winners and failure rates.
- `full_scale_regime_winners.tex`: regime-level winning policies.
- `full_scale_controls_and_failures.tex`: cheap-attention, over-budget, delayed-observation, and mismatch controls.
- `attention_cost_by_method.pdf`: embodied attention cost by policy.
- `success_cost_pareto.pdf`: success versus attention cost/risk tradeoff.
- `regime_winner_phase.pdf`: which policy wins across regimes.
- `representative_trace.csv`: one explicit trace showing belief, attention, risk, slack, and action.

## Manuscript Expansion Strategy

Rewrite `main.tex` into a v3 full-scale manuscript:

1. Keep the claim bounded and explicit.
2. Replace the v2 note with `v3 final full-scale`.
3. Add a stronger abstract with the 12,288,000 decision scale.
4. Expand related work around active perception, sensor scheduling, information value, perception-aware planning, and compute-latency control.
5. Define embodied attention cost as a vector, not only a scalar.
6. Describe dynamics families, regimes, and policies.
7. Report main results with tables and figures.
8. Include negative controls where greedy information should win.
9. Include failure modes where budgeted attention is too conservative.
10. Add appendices for simulator equations, policy definitions, metric derivations, calibration, hardware evaluation, artifact schema, reviewer attacks, limitations, and deployment guidance.

The page count target is at least 25 rendered pages. Extra pages must come from real content: experiments, ablations, stress interpretations, failure catalogs, reproducibility, hardware protocols, and reviewer-facing claim boundaries. Do not pad with spacing tricks.

## RAM-Light Execution Strategy

- Stream seed-level rows directly to CSV.
- Store only aggregate accumulators in memory.
- Store one representative trace rather than all trajectories.
- Generate tiny vector PDFs directly or with a standard-library writer if no plotting package is available.
- Keep seeds deterministic.
- Avoid multiprocessing unless needed.
- Keep all intermediate artifacts inside the paper repo.
- Do not copy to Downloads until final acceptance checks pass.

## Final Acceptance Checklist

Paper31 is not final until all of the following are true:

- `docs/full_scale_execution_plan.md` exists before substantive edits.
- Full-scale runner completes reproducibly.
- Generated outputs exist in `results/full_scale/`.
- Generated figures exist in `figures/full_scale/`.
- Manuscript renders to at least 25 pages.
- PDF text contains `v3 final full-scale` and the represented decision count.
- Build log has no fatal LaTeX errors, unresolved references, undefined citations, or overfull boxes.
- Canonical PDF is copied only to `C:/Users/wangz/Downloads/31.pdf`.
- Local `main.pdf` is removed after final build.
- Docs and status files describe v3, not stale v2 results.
- Commit is pushed and local HEAD matches upstream.
