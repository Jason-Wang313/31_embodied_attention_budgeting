# Final Audit

1. Chosen thesis: Embodied attention is a limited physical resource that must be budgeted jointly with control risk.

2. Field assumption broken: The paper challenges the assumption that sensing is effectively free or separable from safety-critical control.

3. New central mechanism: A risk-coupled attention budget that can prevent the robot from spending sensing effort when it would degrade safe action options.

4. Genuine novelty: The central variable is not uncertainty or information gain alone; it is embodied consumption of attention under finite control opportunity.

5. Closest hostile prior work: Active perception, active sensing surveys, attention-based planning with active perception, decentralized active information acquisition, sensor scheduling, and cost-aware information gathering.

6. Literature coverage: `docs/related_work_matrix.csv` contains a 2013-paper broad sweep plus targeted active-perception and sensor-management clustering. Coverage is useful but not a manual full-PDF related-work review.

7. Proof/formal-claim status: No formal theorem. The claims are mechanistic and empirical, supported by `scripts/toy_attention_budget.py`.

8. Strongest evidence: At horizon 12, the greedy information policy spends five attention actions and succeeds in 0/2000 seeds, while budgeted attention spends two attention actions and succeeds in 1572/2000 seeds.

9. V2 stress evidence: The horizon stress shows the boundary. At horizon 16, greedy sensing recovers to 1886/2000 successes with 114 collisions and average return 1.807, beating budgeted attention at 1572/2000 successes and average return 1.049. This supports finite-horizon attention budgeting, not a universal rejection of information gain.

10. Biggest weaknesses: Toy one-dimensional task; hand-coded risk/budget rule; no hardware validation; no measured sensing latency or physical attention cost; no POMDP or cost-aware active sensing baseline.

11. Paper-readiness judgment: workshop-only / strong-revise. The mechanism is clear, but a strong ICLR submission would need richer embodied-control benchmarks, measured sensing costs, and stronger active-perception baselines.

12. Exact Downloads PDF path: `C:/Users/wangz/Downloads/31.pdf` (exists, size=152764 bytes). Build status: `complete`; copied flag: `True`.

13. GitHub URL: `https://github.com/Jason-Wang313/31_embodied_attention_budgeting`.

14. Visible Desktop PDF copy: absent at checked Desktop paths (expected; canonical PDF is Downloads only).

15. Local repo PDF copy: absent (expected after Downloads copy).

Additional audit notes:
- The build used `scripts/build_pdf.ps1` and removed transient `main.pdf`.
- V2 outputs are `docs/toy_attention_horizon_stress.csv` and `docs/toy_attention_horizon_stress_table.tex`.
