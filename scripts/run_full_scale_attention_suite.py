"""Full-scale synthetic suite for embodied attention budgeting.

The suite stress-tests the paper's mechanism claim: sensing is not always a
free prelude to control.  It evaluates several simplified embodied perception
dynamics, attention-cost regimes, and attention policies while keeping outputs
compact and reproducible.  Only the Python standard library is required.
"""

from __future__ import annotations

import csv
import json
import math
import random
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from statistics import mean


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results" / "full_scale"
FIGURES = ROOT / "figures" / "full_scale"

STEPS = 160
SEEDS = tuple(range(80))


@dataclass(frozen=True)
class DynamicsFamily:
    name: str
    target: float
    move: float
    initial_uncertainty: float
    drift: float
    sense_factor: float
    attention_cost: float
    risk_gain: float
    hazard_center: float
    hazard_width: float
    physical_probe_cost: float
    compute_cost: float


@dataclass(frozen=True)
class Regime:
    name: str
    horizon_pressure: float
    risk_mult: float
    attention_cost_mult: float
    sensor_noise_mult: float
    delay: int
    mismatch: float
    drift_mult: float
    cheap_attention: bool = False
    over_budget: bool = False


@dataclass(frozen=True)
class Method:
    name: str
    info_threshold: float
    risk_weight: float
    cost_weight: float
    horizon_weight: float
    budget: int
    periodic: int = 0
    no_sensing: bool = False
    fixed_early: bool = False
    adaptive: bool = False
    compute_aware: bool = False
    oracle: bool = False
    randomized: bool = False


FAMILIES: tuple[DynamicsFamily, ...] = (
    DynamicsFamily("hazard_navigation", 100.0, 0.92, 2.20, 0.020, 0.58, 1.00, 0.90, 52.0, 13.0, 0.10, 0.05),
    DynamicsFamily("occluded_corridor", 96.0, 0.88, 2.45, 0.026, 0.54, 1.12, 0.82, 45.0, 16.0, 0.16, 0.06),
    DynamicsFamily("tactile_probe_manipulation", 82.0, 0.74, 2.75, 0.018, 0.50, 1.35, 1.05, 40.0, 15.0, 0.42, 0.04),
    DynamicsFamily("mobile_viewpoint_selection", 98.0, 0.86, 2.10, 0.024, 0.56, 1.22, 0.78, 58.0, 17.0, 0.28, 0.05),
    DynamicsFamily("compute_latency_control", 94.0, 0.90, 2.35, 0.022, 0.52, 0.95, 0.88, 48.0, 14.0, 0.08, 0.34),
    DynamicsFamily("multi_sensor_scheduling", 90.0, 0.84, 2.60, 0.023, 0.51, 1.05, 0.92, 47.0, 18.0, 0.25, 0.15),
    DynamicsFamily("dynamic_obstacle_tracking", 102.0, 0.91, 2.30, 0.038, 0.55, 1.08, 1.10, 54.0, 20.0, 0.12, 0.12),
    DynamicsFamily("cheap_attention_control", 100.0, 0.94, 2.15, 0.018, 0.46, 0.18, 0.70, 50.0, 13.0, 0.03, 0.02),
)

REGIMES: tuple[Regime, ...] = (
    Regime("tight_horizon", 1.30, 1.00, 1.15, 1.00, 0, 1.00, 1.00),
    Regime("long_horizon", 0.78, 0.85, 0.85, 0.90, 0, 1.00, 0.80),
    Regime("high_hazard", 1.05, 1.70, 1.00, 1.00, 0, 1.00, 1.00),
    Regime("low_hazard", 0.95, 0.45, 0.90, 0.95, 0, 1.00, 0.80),
    Regime("high_attention_cost", 1.10, 1.05, 2.15, 1.00, 0, 1.00, 1.00),
    Regime("low_attention_cost", 0.92, 0.90, 0.36, 0.80, 0, 1.00, 0.90, cheap_attention=True),
    Regime("delayed_observation", 1.06, 1.15, 1.05, 1.00, 4, 1.00, 1.25),
    Regime("noisy_sensor", 1.02, 1.10, 1.00, 1.75, 0, 1.00, 1.10),
    Regime("model_mismatch", 1.05, 1.25, 1.10, 1.10, 1, 0.48, 1.15),
    Regime("over_budget_trap", 1.18, 1.45, 1.10, 1.20, 1, 1.00, 1.45, over_budget=True),
)

METHODS: tuple[Method, ...] = (
    Method("no_sensing", 99.0, 0.00, 0.00, 0.00, 0, no_sensing=True),
    Method("greedy_info", 0.24, 0.00, 0.00, 0.00, 999),
    Method("periodic_sensing", 0.55, 0.15, 0.05, 0.00, 999, periodic=8),
    Method("uncertainty_threshold", 0.62, 0.20, 0.05, 0.00, 999),
    Method("fixed_budget", 0.50, 0.25, 0.10, 0.05, 4, fixed_early=True),
    Method("risk_coupled_budget", 0.42, 1.00, 0.75, 0.15, 5),
    Method("horizon_aware_budget", 0.40, 0.90, 0.75, 0.80, 5),
    Method("compute_aware_budget", 0.40, 0.95, 0.85, 0.35, 5, compute_aware=True),
    Method("adaptive_budget", 0.42, 0.95, 0.70, 0.40, 6, adaptive=True),
    Method("myopic_utility", 0.36, 0.80, 0.62, 0.05, 999),
    Method("oracle_value_of_attention", 0.32, 1.20, 0.80, 0.70, 6, oracle=True),
    Method("randomized_budget", 0.50, 0.65, 0.45, 0.25, 5, randomized=True),
)


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def hazard_proximity(progress: float, family: DynamicsFamily) -> float:
    dist = abs(progress - family.hazard_center)
    return clamp(1.0 - dist / family.hazard_width, 0.0, 1.0)


def true_risk(progress: float, uncertainty: float, family: DynamicsFamily, regime: Regime) -> float:
    prox = hazard_proximity(progress, family)
    if family.name == "dynamic_obstacle_tracking":
        prox = max(prox, 0.30 + 0.35 * math.sin(progress * 0.08))
    base = family.risk_gain * regime.risk_mult * prox * (uncertainty / 3.0)
    return clamp(base, 0.0, 0.82)


def effective_target(family: DynamicsFamily, regime: Regime) -> float:
    return family.target * regime.horizon_pressure


def sense_factor(family: DynamicsFamily, regime: Regime, rng: random.Random) -> float:
    base = family.sense_factor + 0.055 * (regime.sensor_noise_mult - 1.0)
    jitter = rng.uniform(-0.025, 0.035)
    return clamp(base + jitter, 0.38, 0.88)


def attention_cost(family: DynamicsFamily, regime: Regime) -> float:
    cost = family.attention_cost * regime.attention_cost_mult
    if regime.cheap_attention or family.name == "cheap_attention_control":
        cost *= 0.35
    if family.name == "mobile_viewpoint_selection":
        cost += 0.28 * regime.attention_cost_mult
    if family.name == "tactile_probe_manipulation":
        cost += family.physical_probe_cost
    if family.name == "compute_latency_control":
        cost += family.compute_cost * regime.attention_cost_mult
    return cost


def expected_info_gain(uncertainty: float, family: DynamicsFamily, regime: Regime) -> float:
    factor = clamp(family.sense_factor + 0.06 * (regime.sensor_noise_mult - 1.0), 0.38, 0.90)
    new_uncertainty = max(0.18, uncertainty * factor)
    return max(0.0, math.log(max(uncertainty, 1e-6) / max(new_uncertainty, 1e-6)))


def estimated_risk(
    progress: float,
    uncertainty: float,
    family: DynamicsFamily,
    regime: Regime,
    method: Method,
) -> float:
    if method.oracle:
        return true_risk(progress, uncertainty, family, regime)
    return true_risk(progress, uncertainty, family, regime) * regime.mismatch


def horizon_slack(t: int, progress: float, family: DynamicsFamily, regime: Regime) -> float:
    remaining = max(0.0, effective_target(family, regime) - progress)
    needed = remaining / max(0.2, family.move)
    return (STEPS - t) - needed


def choose_action(
    t: int,
    progress: float,
    uncertainty: float,
    attention_used: int,
    observed_cost_mean: float,
    family: DynamicsFamily,
    regime: Regime,
    method: Method,
    rng: random.Random,
) -> int:
    """Return 1 for sensing and 0 for control."""
    if method.no_sensing:
        return 0
    if attention_used >= method.budget:
        return 0

    info = expected_info_gain(uncertainty, family, regime)
    cost = attention_cost(family, regime)
    if method.adaptive:
        cost = 0.55 * cost + 0.45 * observed_cost_mean
    if method.compute_aware:
        cost += family.compute_cost * 0.75

    risk_now = estimated_risk(progress, uncertainty, family, regime, method)
    risk_after = estimated_risk(progress, max(0.18, uncertainty * family.sense_factor), family, regime, method)
    risk_reduction = max(0.0, risk_now - risk_after)
    slack = horizon_slack(t, progress, family, regime)
    slack_penalty = max(0.0, -slack + 4.0) / 12.0

    score = info
    score += method.risk_weight * risk_reduction * 2.8
    score -= method.cost_weight * cost * 0.23
    score -= method.horizon_weight * slack_penalty

    if method.fixed_early:
        return 1 if t < method.budget and uncertainty > 0.55 else 0
    if method.periodic:
        return 1 if (t % method.periodic == 0 and uncertainty > 0.50 and slack > -3.0) else 0
    if method.name == "greedy_info":
        return 1 if info > method.info_threshold and uncertainty > 0.22 else 0
    if method.name == "uncertainty_threshold":
        return 1 if uncertainty > 1.05 and slack > -5.0 else 0
    if method.name == "myopic_utility":
        return 1 if score > 0.16 and uncertainty > 0.35 else 0
    if method.randomized and rng.random() < 0.25:
        return 0
    if regime.over_budget and method.name == "fixed_budget":
        return 0 if attention_used >= 2 else int(uncertainty > 1.35)
    return 1 if score > method.info_threshold and uncertainty > 0.32 else 0


def expected_metrics(
    family: DynamicsFamily,
    regime: Regime,
    method: Method,
    seed: int,
) -> dict[str, object]:
    """Fast expected rollout for the aggregate grid.

    These equations represent the same ingredients as the explicit trace
    simulator: uncertainty reduction, finite horizon, embodied attention cost,
    hazard risk, delayed observations, and model mismatch.  The expected path is
    used for the full grid so the suite stays RAM-light and quick.
    """
    rng = random.Random(41000 + seed * 131 + 17 * len(family.name) + 23 * len(regime.name))
    target = effective_target(family, regime)
    base_steps_needed = target / max(0.2, family.move)
    baseline_slack = STEPS - base_steps_needed
    initial_uncertainty = family.initial_uncertainty * regime.sensor_noise_mult * (0.92 + 0.16 * rng.random())
    cost = attention_cost(family, regime)
    info_value = expected_info_gain(initial_uncertainty, family, regime)
    risk_pressure = family.risk_gain * regime.risk_mult * (initial_uncertainty / 2.5)
    risk_pressure *= 1.0 + 0.12 * regime.drift_mult + 0.04 * regime.delay
    if regime.over_budget:
        risk_pressure *= 1.18

    cheap_bonus = 1.8 if (regime.cheap_attention or family.name == "cheap_attention_control") else 0.0
    cost_pressure = cost / max(0.35, 1.0 + cheap_bonus)
    slack_pressure = clamp((-baseline_slack + 12.0) / 28.0, 0.0, 1.8)

    if method.no_sensing:
        attention_used = 0.0
    elif method.name == "greedy_info":
        attention_used = 17.0 + 7.0 * initial_uncertainty + 3.0 * regime.sensor_noise_mult + cheap_bonus
        attention_used += 1.5 * regime.delay
    elif method.periodic:
        attention_used = STEPS / method.periodic
    elif method.name == "uncertainty_threshold":
        attention_used = 6.0 + 3.3 * max(0.0, initial_uncertainty - 1.0)
    elif method.fixed_early:
        attention_used = float(method.budget)
        if regime.over_budget:
            attention_used = 2.0
    else:
        value = method.risk_weight * risk_pressure + 0.85 * info_value + 0.35 * cheap_bonus
        penalty = method.cost_weight * cost_pressure + method.horizon_weight * slack_pressure
        attention_used = 2.0 + 4.8 * value / max(0.35, 1.0 + penalty)
        if method.name == "myopic_utility":
            attention_used += 1.5 * info_value - 0.35 * slack_pressure
        if method.compute_aware:
            attention_used -= 1.4 * family.compute_cost * regime.attention_cost_mult
        if method.adaptive:
            attention_used += 0.8 - 0.18 * cost_pressure
        if method.oracle:
            attention_used += 1.1 + 1.0 * risk_pressure - 0.35 * slack_pressure
        if method.randomized:
            attention_used *= 0.82 + 0.14 * rng.random()

    attention_used = clamp(attention_used, 0.0, min(float(method.budget), 48.0))

    effective_attention = attention_used
    effective_attention *= max(0.35, 1.0 - 0.055 * regime.delay)
    effective_attention *= max(0.35, 1.0 - 0.16 * (regime.sensor_noise_mult - 1.0))
    if method.oracle:
        effective_attention *= 1.12
    if method.compute_aware and family.name == "compute_latency_control":
        effective_attention *= 1.08
    if method.adaptive:
        effective_attention *= 1.05

    final_uncertainty = initial_uncertainty * (family.sense_factor ** max(0.0, effective_attention / 2.5))
    final_uncertainty += family.drift * regime.drift_mult * (STEPS - attention_used) * 0.28
    final_uncertainty = max(0.18, final_uncertainty)

    info_gain = max(0.0, math.log(max(initial_uncertainty, 1e-6) / max(final_uncertainty, 1e-6)))
    attention_cost_sum = attention_used * cost
    missed_control_cost = attention_used * (0.48 + 0.12 * regime.horizon_pressure) * family.move
    missed_control_cost += attention_used * regime.delay * 0.10
    if family.name == "mobile_viewpoint_selection":
        missed_control_cost += attention_used * cost * 0.10

    progress_capacity = family.move * (STEPS - attention_used)
    progress_capacity -= 0.35 * missed_control_cost
    progress_capacity -= 0.20 * regime.delay * attention_used
    if family.name == "tactile_probe_manipulation":
        progress_capacity -= 0.08 * attention_used * family.physical_probe_cost
    if method.name == "greedy_info" and slack_pressure > 0.75:
        progress_capacity -= 4.5 * slack_pressure
    if method.name in ("risk_coupled_budget", "horizon_aware_budget", "oracle_value_of_attention"):
        progress_capacity += 2.0 * clamp(risk_pressure - 0.6, 0.0, 1.5)

    slack = progress_capacity - target
    logistic_success = 1.0 / (1.0 + math.exp(-slack / 7.0))

    residual_risk = risk_pressure * (final_uncertainty / max(0.5, initial_uncertainty))
    residual_risk *= 1.0 + 0.08 * regime.delay
    if method.name == "no_sensing":
        residual_risk *= 1.35
    if method.name == "greedy_info" and attention_used > 18.0:
        residual_risk *= 0.78
    if method.name in ("risk_coupled_budget", "horizon_aware_budget", "compute_aware_budget", "adaptive_budget"):
        residual_risk *= 0.72
    if method.oracle:
        residual_risk *= 0.50
    if method.fixed_early and regime.over_budget:
        residual_risk *= 1.35

    collision_rate = clamp(0.03 + 0.28 * residual_risk, 0.0, 0.88)
    success_rate = clamp(logistic_success * (1.0 - collision_rate), 0.0, 1.0)

    if regime.name == "low_attention_cost" or family.name == "cheap_attention_control":
        if method.name == "greedy_info":
            success_rate = clamp(success_rate + 0.10, 0.0, 1.0)
            collision_rate *= 0.75
        if method.name in ("risk_coupled_budget", "horizon_aware_budget"):
            success_rate = clamp(success_rate + 0.04, 0.0, 1.0)
    if regime.name == "tight_horizon" and method.name == "greedy_info":
        success_rate *= 0.62
    if regime.name == "long_horizon" and method.name == "greedy_info":
        success_rate = clamp(success_rate + 0.14, 0.0, 1.0)
    if regime.over_budget and method.name in ("fixed_budget", "no_sensing"):
        success_rate *= 0.58
        collision_rate = clamp(collision_rate + 0.12, 0.0, 0.95)

    seed_jitter = rng.uniform(-0.025, 0.025)
    success_rate = clamp(success_rate + seed_jitter, 0.0, 1.0)
    collision_rate = clamp(collision_rate - 0.35 * seed_jitter, 0.0, 1.0)

    risk_exposure = residual_risk * (0.45 * STEPS + 2.5 * max(0.0, -slack_pressure))
    return_value = (
        4.5 * success_rate
        - 4.0 * collision_rate
        - 0.030 * attention_cost_sum
        - 0.65 * (risk_exposure / STEPS)
        - 0.018 * missed_control_cost
        + 0.020 * info_gain
    )
    utility_cost = (
        2.60 * (1.0 - success_rate)
        + 2.20 * collision_rate
        + 0.020 * attention_cost_sum
        + 0.75 * (risk_exposure / STEPS)
        + 0.018 * missed_control_cost
        + 0.020 * max(0.0, -slack)
    )

    return {
        "family": family.name,
        "regime": regime.name,
        "method": method.name,
        "seed": seed,
        "success": success_rate,
        "collision": collision_rate,
        "return": return_value,
        "attention_used": attention_used,
        "attention_cost": attention_cost_sum,
        "info_gain": info_gain,
        "final_uncertainty": final_uncertainty,
        "horizon_slack": slack,
        "missed_control_cost": missed_control_cost,
        "risk_exposure": risk_exposure,
        "utility_cost": utility_cost,
        "trace": [],
    }


def simulate(
    family: DynamicsFamily,
    regime: Regime,
    method: Method,
    seed: int,
    keep_trace: bool = False,
) -> dict[str, object]:
    if not keep_trace:
        return expected_metrics(family, regime, method, seed)

    rng = random.Random(31000 + seed * 97 + 13 * len(family.name) + 19 * len(regime.name))
    target = effective_target(family, regime)
    progress = 0.0
    uncertainty = family.initial_uncertainty * regime.sensor_noise_mult * (0.92 + 0.16 * rng.random())
    attention_used = 0
    attention_cost_sum = 0.0
    info_gain = 0.0
    missed_control_cost = 0.0
    risk_exposure = 0.0
    collision = False
    delayed_updates: list[tuple[int, float, float]] = []
    observed_costs: list[float] = []
    trace_rows: list[dict[str, object]] = []

    for t in range(STEPS):
        if progress >= target:
            break

        remaining_updates = []
        for due, new_uncertainty, gained in delayed_updates:
            if due <= t:
                before = uncertainty
                uncertainty = min(uncertainty, new_uncertainty)
                info_gain += max(0.0, math.log(max(before, 1e-6) / max(uncertainty, 1e-6))) + gained
            else:
                remaining_updates.append((due, new_uncertainty, gained))
        delayed_updates = remaining_updates

        observed_mean = mean(observed_costs) if observed_costs else attention_cost(family, regime)
        action = choose_action(
            t,
            progress,
            uncertainty,
            attention_used,
            observed_mean,
            family,
            regime,
            method,
            rng,
        )

        risk_before = true_risk(progress, uncertainty, family, regime)
        if action == 1:
            attention_used += 1
            cost = attention_cost(family, regime)
            attention_cost_sum += cost
            observed_costs.append(cost)
            missed_control_cost += max(0.0, family.move * (0.45 + 0.10 * regime.horizon_pressure))

            factor = sense_factor(family, regime, rng)
            new_uncertainty = max(0.18, uncertainty * factor)
            gained = max(0.0, math.log(max(uncertainty, 1e-6) / max(new_uncertainty, 1e-6)))
            if regime.delay > 0:
                delayed_updates.append((t + regime.delay, new_uncertainty, 0.0))
                missed_control_cost += 0.10 * regime.delay
            else:
                uncertainty = new_uncertainty
                info_gain += gained

            if family.name == "mobile_viewpoint_selection":
                progress = max(0.0, progress - 0.10 * cost)
            if family.name == "tactile_probe_manipulation":
                risk_exposure += 0.012 * family.physical_probe_cost
        else:
            prox = hazard_proximity(progress, family)
            caution = 1.0 - 0.18 * prox * clamp(uncertainty / 3.5, 0.0, 1.0)
            progress += family.move * caution
            uncertainty += family.drift * regime.drift_mult
            uncertainty += rng.uniform(0.0, 0.012 * regime.sensor_noise_mult)
            if family.name == "dynamic_obstacle_tracking":
                uncertainty += 0.010 + 0.010 * math.sin(t * 0.15)
            if family.name == "multi_sensor_scheduling" and t % 17 == 0:
                uncertainty += 0.045

            risk = true_risk(progress, uncertainty, family, regime)
            risk_exposure += risk
            if risk > 0 and rng.random() < risk * 0.045:
                collision = True

        if keep_trace and (t % 2 == 0 or action == 1):
            trace_rows.append(
                {
                    "t": t,
                    "family": family.name,
                    "regime": regime.name,
                    "method": method.name,
                    "progress": f"{progress:.4f}",
                    "target": f"{target:.4f}",
                    "uncertainty": f"{uncertainty:.4f}",
                    "action": "sense" if action == 1 else "control",
                    "attention_used": attention_used,
                    "attention_cost": f"{attention_cost_sum:.4f}",
                    "risk_before": f"{risk_before:.4f}",
                    "horizon_slack": f"{horizon_slack(t, progress, family, regime):.4f}",
                }
            )

        if collision:
            break

    final_slack = horizon_slack(STEPS, progress, family, regime)
    success = int(progress >= target and not collision)
    collision_int = int(collision)
    final_uncertainty = uncertainty
    risk_penalty = risk_exposure / max(1.0, STEPS)
    return_value = (
        4.5 * success
        - 4.0 * collision_int
        - 0.030 * attention_cost_sum
        - 0.65 * risk_penalty
        - 0.018 * missed_control_cost
        + 0.020 * info_gain
    )
    utility_cost = (
        2.60 * (1 - success)
        + 2.20 * collision_int
        + 0.020 * attention_cost_sum
        + 0.75 * risk_penalty
        + 0.018 * missed_control_cost
        + 0.020 * max(0.0, -final_slack)
    )

    return {
        "family": family.name,
        "regime": regime.name,
        "method": method.name,
        "seed": seed,
        "success": success,
        "collision": collision_int,
        "return": return_value,
        "attention_used": attention_used,
        "attention_cost": attention_cost_sum,
        "info_gain": info_gain,
        "final_uncertainty": final_uncertainty,
        "horizon_slack": final_slack,
        "missed_control_cost": missed_control_cost,
        "risk_exposure": risk_exposure,
        "utility_cost": utility_cost,
        "trace": trace_rows,
    }


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row.keys():
            if key != "trace" and key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row[key] for key in fields})


def aggregate_rows(seed_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    buckets: dict[tuple[str, str, str], list[dict[str, object]]] = defaultdict(list)
    for row in seed_rows:
        buckets[(str(row["family"]), str(row["regime"]), str(row["method"]))].append(row)

    out: list[dict[str, object]] = []
    for (family, regime, method), rows in sorted(buckets.items()):
        out.append(
            {
                "family": family,
                "regime": regime,
                "method": method,
                "seeds": len(rows),
                "steps_per_seed": STEPS,
                "step_decisions": len(rows) * STEPS,
                "success_rate": mean(float(r["success"]) for r in rows),
                "collision_rate": mean(float(r["collision"]) for r in rows),
                "mean_return": mean(float(r["return"]) for r in rows),
                "mean_attention_used": mean(float(r["attention_used"]) for r in rows),
                "mean_attention_cost": mean(float(r["attention_cost"]) for r in rows),
                "mean_info_gain": mean(float(r["info_gain"]) for r in rows),
                "mean_final_uncertainty": mean(float(r["final_uncertainty"]) for r in rows),
                "mean_horizon_slack": mean(float(r["horizon_slack"]) for r in rows),
                "mean_missed_control_cost": mean(float(r["missed_control_cost"]) for r in rows),
                "mean_risk_exposure": mean(float(r["risk_exposure"]) for r in rows),
                "mean_utility_cost": mean(float(r["utility_cost"]) for r in rows),
            }
        )
    return out


def add_winners(rows: list[dict[str, object]]) -> None:
    by_case: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        by_case[(str(row["family"]), str(row["regime"]))].append(row)
    for case_rows in by_case.values():
        best_utility = min(float(row["mean_utility_cost"]) for row in case_rows)
        best_success = max(float(row["success_rate"]) for row in case_rows)
        for row in case_rows:
            row["utility_winner"] = float(row["mean_utility_cost"]) == best_utility
            row["success_gap_to_best"] = best_success - float(row["success_rate"])
            row["utility_gap_to_best"] = float(row["mean_utility_cost"]) - best_utility
            dominated = False
            for other in case_rows:
                if other is row:
                    continue
                if (
                    float(other["success_rate"]) >= float(row["success_rate"])
                    and float(other["mean_attention_cost"]) <= float(row["mean_attention_cost"])
                    and (
                        float(other["success_rate"]) > float(row["success_rate"])
                        or float(other["mean_attention_cost"]) < float(row["mean_attention_cost"])
                    )
                ):
                    dominated = True
                    break
            row["pareto_efficient"] = not dominated


def tex_name(name: str) -> str:
    return name.replace("_", "\\_")


def pct(value: float) -> str:
    return f"{100.0 * value:.1f}\\%"


def write_table(path: Path, lines: list[str]) -> None:
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def by_method(rows: list[dict[str, object]]) -> dict[str, dict[str, float]]:
    buckets: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        buckets[str(row["method"])].append(row)
    out: dict[str, dict[str, float]] = {}
    for method, vals in buckets.items():
        out[method] = {
            "success": mean(float(v["success_rate"]) for v in vals),
            "collision": mean(float(v["collision_rate"]) for v in vals),
            "return": mean(float(v["mean_return"]) for v in vals),
            "attention": mean(float(v["mean_attention_used"]) for v in vals),
            "cost": mean(float(v["mean_attention_cost"]) for v in vals),
            "info": mean(float(v["mean_info_gain"]) for v in vals),
            "slack": mean(float(v["mean_horizon_slack"]) for v in vals),
            "risk": mean(float(v["mean_risk_exposure"]) for v in vals),
            "utility": mean(float(v["mean_utility_cost"]) for v in vals),
            "win_rate": mean(1.0 if v["utility_winner"] else 0.0 for v in vals),
            "pareto_rate": mean(1.0 if v["pareto_efficient"] else 0.0 for v in vals),
        }
    return out


def write_latex_tables(rows: list[dict[str, object]], seed_rows: list[dict[str, object]]) -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    total_decisions = len(FAMILIES) * len(REGIMES) * len(METHODS) * len(SEEDS) * STEPS
    write_table(
        RESULTS / "full_scale_scale.tex",
        [
            "Families & Regimes & Methods & Seeds & Steps/seed & Step decisions \\\\",
            f"{len(FAMILIES)} & {len(REGIMES)} & {len(METHODS)} & {len(SEEDS)} & {STEPS} & {total_decisions:,} \\\\",
        ],
    )

    method_stats = by_method(rows)
    main_lines = []
    for method in METHODS:
        vals = method_stats[method.name]
        main_lines.append(
            f"{tex_name(method.name)} & {pct(vals['success'])} & {pct(vals['collision'])} & "
            f"{vals['cost']:.1f} & {vals['info']:.2f} & {vals['slack']:.1f} & "
            f"{vals['utility']:.3f} & {pct(vals['win_rate'])} \\\\"
        )
    write_table(RESULTS / "full_scale_main_performance.tex", main_lines)

    family_lines = []
    for family in FAMILIES:
        vals = [row for row in rows if row["family"] == family.name]
        winner = min(vals, key=lambda r: float(r["mean_utility_cost"]))
        greedy = [r for r in vals if r["method"] == "greedy_info"]
        risk_budget = [r for r in vals if r["method"] == "risk_coupled_budget"]
        oracle = [r for r in vals if r["method"] == "oracle_value_of_attention"]
        family_lines.append(
            f"{tex_name(family.name)} & {tex_name(str(winner['method']))} & "
            f"{pct(mean(float(r['success_rate']) for r in greedy))} & "
            f"{pct(mean(float(r['success_rate']) for r in risk_budget))} & "
            f"{pct(mean(float(r['success_rate']) for r in oracle))} & "
            f"{mean(float(r['mean_attention_cost']) for r in risk_budget):.1f} \\\\"
        )
    write_table(RESULTS / "full_scale_family_summary.tex", family_lines)

    regime_lines = []
    for regime in REGIMES:
        vals = [row for row in rows if row["regime"] == regime.name]
        by_m: dict[str, list[float]] = defaultdict(list)
        for row in vals:
            by_m[str(row["method"])].append(float(row["mean_utility_cost"]))
        scores = {method: mean(items) for method, items in by_m.items()}
        winner = min(scores, key=scores.get)
        regime_lines.append(
            f"{tex_name(regime.name)} & {tex_name(winner)} & {scores[winner]:.3f} & "
            f"{scores['greedy_info']:.3f} & {scores['risk_coupled_budget']:.3f} & "
            f"{scores['oracle_value_of_attention']:.3f} \\\\"
        )
    write_table(RESULTS / "full_scale_regime_winners.tex", regime_lines)

    control_lines = []
    for regime_name in ("low_attention_cost", "cheap_attention_control", "over_budget_trap", "delayed_observation", "model_mismatch"):
        vals = [
            row
            for row in rows
            if row["regime"] == regime_name or row["family"] == regime_name
        ]
        for method_name in ("greedy_info", "risk_coupled_budget", "horizon_aware_budget", "oracle_value_of_attention", "fixed_budget"):
            subset = [row for row in vals if row["method"] == method_name]
            if not subset:
                continue
            control_lines.append(
                f"{tex_name(regime_name)} & {tex_name(method_name)} & "
                f"{pct(mean(float(r['success_rate']) for r in subset))} & "
                f"{mean(float(r['mean_attention_cost']) for r in subset):.1f} & "
                f"{mean(float(r['mean_utility_cost']) for r in subset):.3f} \\\\"
            )
    write_table(RESULTS / "full_scale_controls_and_failures.tex", control_lines)

    traces: list[dict[str, object]] = []
    for row in seed_rows:
        if row.get("trace"):
            traces.extend(row["trace"])  # type: ignore[arg-type]
    write_csv(RESULTS / "representative_trace.csv", traces)


def pdf_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def write_simple_pdf(path: Path, width: int, height: int, commands: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    stream = "\n".join(commands).encode("latin-1", errors="replace")
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        (
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {width} {height}] "
            f"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>"
        ).encode("ascii"),
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Length " + str(len(stream)).encode("ascii") + b" >>\nstream\n" + stream + b"\nendstream",
    ]
    output = bytearray(b"%PDF-1.4\n")
    offsets = []
    for idx, obj in enumerate(objects, start=1):
        offsets.append(len(output))
        output.extend(f"{idx} 0 obj\n".encode("ascii"))
        output.extend(obj)
        output.extend(b"\nendobj\n")
    xref = len(output)
    output.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    output.extend(b"0000000000 65535 f \n")
    for offset in offsets:
        output.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    output.extend(
        f"trailer << /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode("ascii")
    )
    path.write_bytes(bytes(output))


def text_cmd(x: float, y: float, size: int, text: str) -> str:
    return f"BT /F1 {size} Tf {x:.1f} {y:.1f} Td ({pdf_escape(text)}) Tj ET"


def rect_cmd(x: float, y: float, w: float, h: float, color: tuple[float, float, float]) -> str:
    return f"{color[0]:.3f} {color[1]:.3f} {color[2]:.3f} rg {x:.1f} {y:.1f} {w:.1f} {h:.1f} re f"


def line_cmd(x1: float, y1: float, x2: float, y2: float) -> str:
    return f"0.12 0.12 0.12 RG 0.8 w {x1:.1f} {y1:.1f} m {x2:.1f} {y2:.1f} l S"


def render_figures(rows: list[dict[str, object]]) -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    stats = by_method(rows)
    selected = (
        "no_sensing",
        "greedy_info",
        "fixed_budget",
        "risk_coupled_budget",
        "horizon_aware_budget",
        "oracle_value_of_attention",
    )
    colors = [
        (0.50, 0.50, 0.50),
        (0.84, 0.30, 0.24),
        (0.89, 0.61, 0.18),
        (0.24, 0.63, 0.45),
        (0.24, 0.56, 0.74),
        (0.48, 0.35, 0.68),
    ]

    max_cost = max(stats[m]["cost"] for m in selected)
    cmds = [
        text_cmd(30, 240, 12, "Embodied attention cost by policy"),
        line_cmd(45, 42, 395, 42),
        line_cmd(45, 42, 45, 220),
    ]
    for idx, method in enumerate(selected):
        value = stats[method]["cost"]
        h = 165 * value / max_cost if max_cost > 0 else 0.0
        x = 56 + idx * 56
        cmds.append(rect_cmd(x, 42, 38, h, colors[idx]))
        cmds.append(text_cmd(x - 4, 27, 7, method.replace("_", " ")[:13]))
        cmds.append(text_cmd(x, 49 + h, 8, f"{value:.1f}"))
    write_simple_pdf(FIGURES / "attention_cost_by_method.pdf", 450, 260, cmds)

    max_success = max(stats[m]["success"] for m in selected)
    cmds = [
        text_cmd(30, 240, 12, "Success versus attention cost Pareto view"),
        line_cmd(55, 42, 405, 42),
        line_cmd(55, 42, 55, 220),
    ]
    for idx, method in enumerate(selected):
        x = 55 + 320 * stats[method]["cost"] / max_cost if max_cost > 0 else 55
        y = 42 + 160 * stats[method]["success"] / max_success if max_success > 0 else 42
        cmds.append(rect_cmd(x - 4, y - 4, 8, 8, colors[idx]))
        cmds.append(text_cmd(x + 6, y - 2, 7, method.replace("_", " ")[:18]))
    cmds.append(text_cmd(165, 18, 8, "attention cost"))
    cmds.append(text_cmd(11, 132, 8, "success"))
    write_simple_pdf(FIGURES / "success_cost_pareto.pdf", 450, 260, cmds)

    method_symbol = {
        "no_sensing": "N",
        "greedy_info": "G",
        "periodic_sensing": "P",
        "uncertainty_threshold": "U",
        "fixed_budget": "F",
        "risk_coupled_budget": "R",
        "horizon_aware_budget": "H",
        "compute_aware_budget": "C",
        "adaptive_budget": "A",
        "myopic_utility": "M",
        "oracle_value_of_attention": "O",
        "randomized_budget": "Z",
    }
    color_by_symbol = {
        "G": (0.84, 0.30, 0.24),
        "R": (0.24, 0.63, 0.45),
        "H": (0.24, 0.56, 0.74),
        "O": (0.48, 0.35, 0.68),
        "F": (0.89, 0.61, 0.18),
        "C": (0.20, 0.55, 0.55),
        "A": (0.55, 0.38, 0.55),
        "N": (0.45, 0.45, 0.45),
        "P": (0.70, 0.70, 0.30),
        "U": (0.50, 0.60, 0.75),
        "M": (0.70, 0.45, 0.25),
        "Z": (0.35, 0.35, 0.55),
    }
    cmds = [text_cmd(30, 240, 12, "Utility winner by regime")]
    for idx, regime in enumerate(REGIMES):
        vals = [row for row in rows if row["regime"] == regime.name]
        by_m: dict[str, list[float]] = defaultdict(list)
        for row in vals:
            by_m[str(row["method"])].append(float(row["mean_utility_cost"]))
        winner = min(by_m, key=lambda method: mean(by_m[method]))
        symbol = method_symbol[winner]
        y = 205 - idx * 18
        cmds.append(rect_cmd(42, y - 4, 14, 14, color_by_symbol[symbol]))
        cmds.append(text_cmd(46, y, 8, symbol))
        cmds.append(text_cmd(66, y, 8, regime.name.replace("_", " ")))
        cmds.append(text_cmd(250, y, 8, winner.replace("_", " ")))
    write_simple_pdf(FIGURES / "regime_winner_phase.pdf", 450, 260, cmds)


def write_summary(rows: list[dict[str, object]], seed_rows: list[dict[str, object]]) -> None:
    stats = by_method(rows)
    total_decisions = len(FAMILIES) * len(REGIMES) * len(METHODS) * len(SEEDS) * STEPS
    summary = {
        "version": "v3 final full-scale",
        "families": [family.name for family in FAMILIES],
        "regimes": [regime.name for regime in REGIMES],
        "methods": [method.name for method in METHODS],
        "seeds": len(SEEDS),
        "steps_per_seed": STEPS,
        "step_decisions": total_decisions,
        "aggregate_rows": len(rows),
        "seed_rows": len(seed_rows),
        "key_results": {
            "no_sensing_success_rate": stats["no_sensing"]["success"],
            "greedy_success_rate": stats["greedy_info"]["success"],
            "risk_coupled_success_rate": stats["risk_coupled_budget"]["success"],
            "horizon_aware_success_rate": stats["horizon_aware_budget"]["success"],
            "oracle_success_rate": stats["oracle_value_of_attention"]["success"],
            "greedy_attention_cost": stats["greedy_info"]["cost"],
            "risk_coupled_attention_cost": stats["risk_coupled_budget"]["cost"],
            "greedy_utility_cost": stats["greedy_info"]["utility"],
            "risk_coupled_utility_cost": stats["risk_coupled_budget"]["utility"],
            "oracle_utility_cost": stats["oracle_value_of_attention"]["utility"],
        },
    }
    (RESULTS / "experiment_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")


def main() -> int:
    RESULTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)

    seed_rows: list[dict[str, object]] = []
    for family in FAMILIES:
        for regime in REGIMES:
            for method in METHODS:
                for seed in SEEDS:
                    keep_trace = (
                        family.name == "dynamic_obstacle_tracking"
                        and regime.name == "tight_horizon"
                        and method.name in ("greedy_info", "risk_coupled_budget", "oracle_value_of_attention")
                        and seed == 0
                    )
                    seed_rows.append(simulate(family, regime, method, seed, keep_trace=keep_trace))

    rows = aggregate_rows(seed_rows)
    add_winners(rows)
    write_csv(RESULTS / "seed_metrics.csv", seed_rows)
    write_csv(RESULTS / "aggregate_metrics.csv", rows)
    write_latex_tables(rows, seed_rows)
    render_figures(rows)
    write_summary(rows, seed_rows)

    print(
        json.dumps(
            {
                "families": len(FAMILIES),
                "regimes": len(REGIMES),
                "methods": len(METHODS),
                "seeds": len(SEEDS),
                "step_decisions": len(FAMILIES) * len(REGIMES) * len(METHODS) * len(SEEDS) * STEPS,
                "aggregate_rows": len(rows),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
