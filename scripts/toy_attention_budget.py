import csv
import math
import random
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Result:
    policy: str
    success: int
    collisions: int
    avg_return: float
    avg_attention_used: float
    avg_info: float


def step_dynamics(x, belief_sigma, budget, action, rng):
    # Task: move toward target x=10 while avoiding a hazard at x=5.
    # action 0 = move, action 1 = sense.
    info_gain = 0.0
    attention_cost = 0.0
    reward = -0.05
    collided = False
    if action == 1:
        # Sensing reduces uncertainty, but takes time and consumes a limited budget.
        belief_sigma = max(0.2, belief_sigma * 0.6)
        budget -= 1
        attention_cost = 1.0
        info_gain = math.log(1.0 / belief_sigma)
        reward -= 0.15
    else:
        # Moving while uncertain risks entering the hazard.
        x += 1
        reward -= 0.02
        hazard_prob = min(0.95, max(0.0, belief_sigma * 0.25))
        if x == 5 and rng.random() < hazard_prob:
            collided = True
            reward -= 5.0
        elif x >= 10:
            reward += 4.0
    return x, belief_sigma, budget, reward, collided, info_gain, attention_cost


def run_episode(policy, seed, horizon=12):
    rng = random.Random(seed)
    x = 0
    belief_sigma = 2.2
    budget = 3 if policy == "budgeted" else 999
    total_reward = 0.0
    total_info = 0.0
    attention_used = 0.0
    collided = False
    for t in range(horizon):
        if x >= 10 or collided:
            break
        if policy == "greedy":
            action = 1 if belief_sigma > 0.25 else 0
        elif policy == "budgeted":
            risky = x >= 4 and x <= 5
            action = 1 if (budget > 0 and belief_sigma > 1.2 and not risky) else 0
        else:  # baseline
            action = 0
        x, belief_sigma, budget, reward, collided, info_gain, attention_cost = step_dynamics(
            x, belief_sigma, budget, action, rng
        )
        total_reward += reward
        total_info += info_gain
        attention_used += attention_cost
    success = int(x >= 10 and not collided)
    return success, int(collided), total_reward, attention_used, total_info


def aggregate(policy, n=2000, horizon=12):
    vals = [run_episode(policy, s, horizon=horizon) for s in range(n)]
    success = sum(v[0] for v in vals)
    collisions = sum(v[1] for v in vals)
    avg_return = sum(v[2] for v in vals) / n
    avg_attention_used = sum(v[3] for v in vals) / n
    avg_info = sum(v[4] for v in vals) / n
    return Result(policy, success, collisions, avg_return, avg_attention_used, avg_info)


def horizon_stress(horizons=(12, 14, 16, 18), n=2000):
    rows = []
    for horizon in horizons:
        for policy in ["baseline", "greedy", "budgeted"]:
            result = aggregate(policy, n=n, horizon=horizon)
            rows.append(
                {
                    "horizon": horizon,
                    "policy": policy,
                    "success": result.success,
                    "collisions": result.collisions,
                    "avg_return": result.avg_return,
                    "avg_attention_used": result.avg_attention_used,
                    "avg_info": result.avg_info,
                }
            )
    return rows


def write_horizon_stress(rows):
    out = Path("docs/toy_attention_horizon_stress.csv")
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "horizon",
                "policy",
                "success",
                "collisions",
                "avg_return",
                "avg_attention_used",
                "avg_info",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    table = Path("docs/toy_attention_horizon_stress_table.tex")
    lines = [
        "\\begin{tabular}{llrrrr}",
        "\\toprule",
        "Horizon & Policy & Success & Collisions & Return & Attention \\\\",
        "\\midrule",
    ]
    for row in rows:
        lines.append(
            f"{row['horizon']} & {row['policy']} & {row['success']} & {row['collisions']} & "
            f"{float(row['avg_return']):.3f} & {float(row['avg_attention_used']):.3f} \\\\"
        )
    lines.extend(["\\bottomrule", "\\end{tabular}", ""])
    table.write_text("\n".join(lines), encoding="utf-8")


def main():
    out = Path("docs/toy_attention_budget_results.csv")
    rows = [aggregate("baseline"), aggregate("greedy"), aggregate("budgeted")]
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["policy", "success", "collisions", "avg_return", "avg_attention_used", "avg_info"])
        for r in rows:
            writer.writerow([r.policy, r.success, r.collisions, f"{r.avg_return:.3f}", f"{r.avg_attention_used:.3f}", f"{r.avg_info:.3f}"])
    for r in rows:
        print(r)
    stress_rows = horizon_stress()
    write_horizon_stress(stress_rows)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
