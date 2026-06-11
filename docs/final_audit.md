# Final Audit

1. Chosen thesis: embodied attention is a limited physical resource that must be budgeted jointly with control risk.
2. Field assumption broken: sensing is effectively free or separable from safety-critical control.
3. New central mechanism: a risk-coupled attention budget that can prevent the robot from spending sensing effort when it would degrade safe action options.
4. Genuine novelty: the central variable is not uncertainty or information gain; it is the embodied consumption of attention under risk.
5. Closest hostile prior work: `Attention-Based Planning with Active Perception`, `Active Sensing for Robotics – A Survey`, and `Decentralized Active Information Acquisition: Theory and Application to Multi-Robot SLAM`.
6. Literature coverage: 2,013-paper broad sweep in `docs/related_work_matrix.csv`, plus targeted active-perception and sensor-management clustering.
7. Proof/formal-claim status: no formal theorem yet; empirical mechanism evidence is provided by `scripts/toy_attention_budget.py`.
8. Strongest evidence: 2,013-paper literature boundary, hostile-prior analysis, and a deterministic toy task where greedy sensing spends all five attention actions and fails while budgeted attention succeeds in 1,572/2,000 seeds.
9. Biggest weaknesses: toy evidence risk, possible overlap with active perception cost terms, and the need to validate the mechanism on richer embodied-control benchmarks.
10. Paper-readiness judgment: recovered and paper artifact built.
11. Exact Downloads PDF path: `C:/Users/wangz/Downloads/31.pdf`
12. GitHub URL: `https://github.com/Jason-Wang313/31_embodied_attention_budgeting`
13. Visible Desktop PDF copy by orchestrator: `C:/Users/wangz/OneDrive/Desktop/31.pdf`
14. Manual recovery: child attempt 2 timed out during an unbounded template search; the orchestrator copied the local ICLR 2026 style files, reran the toy simulation, corrected the result table, compiled `main.tex`, and copied the numbered PDF to Downloads and Desktop.
