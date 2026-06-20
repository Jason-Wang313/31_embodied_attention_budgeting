# Final Audit

1. Chosen thesis: Embodied attention is a limited physical and computational resource that must be budgeted jointly with control risk, attention cost, and remaining horizon.

2. Field assumption broken: The paper challenges the assumption that sensing is effectively free or separable from safety-critical control.

3. New central mechanism: A risk-coupled attention budget that prevents the robot from spending sensing effort when it degrades control opportunity, while still allowing attention when risk reduction justifies cost.

4. Genuine novelty boundary: Active perception and value-of-information methods are close. The defended contribution is explicit embodied control-opportunity accounting and multi-axis reporting.

5. Closest hostile prior work: Active perception, active sensing surveys, attention-based planning, decentralized active information acquisition, sensor scheduling, value of information, and cost-aware information gathering.

6. Literature coverage: `docs/related_work_matrix.csv` contains a 2013-paper broad sweep plus targeted active-perception and sensor-management clustering. Coverage is useful but not a manual full-PDF related-work review.

7. Proof/formal-claim status: No formal theorem. Claims are mechanistic and empirical, supported by the v3 full-scale synthetic suite plus preserved v1/v2 artifacts.

8. Strongest v3 evidence: The full-scale suite represents 12,288,000 attention-control decisions over 8 dynamics families, 10 regimes, 12 policies, and 80 seeds. Greedy information succeeds in 39.1% with attention cost 45.3; risk-coupled budgeting succeeds in 76.5% with attention cost 5.6; oracle value-of-attention succeeds in 82.9% with best utility cost 1.108.

9. Negative controls and failures: Low-attention-cost and long-horizon regimes show greedy information can recover. No-sensing fails on safety. Over-budget traps show budgeted policies can fail by under-sensing.

10. Biggest remaining weakness: No real robot validation, no measured sensing latency/motion/contact/compute cost, and no learned POMDP or hardware active-sensing baseline.

11. Paper-readiness judgment: v3 is final for this batch pass as a full-scale synthetic/mechanism paper. It is not a hardware-validated robotics claim.

12. Exact Downloads PDF path: `C:/Users/wangz/Downloads/31.pdf` (exists, size=405172 bytes, 25 pages, SHA256 `2091D545EA035DEBDAB6E8AC3DFDBC0240EE44186A5A58963773B821C05742CD`). Build status: `complete`; copied flag: `True`.

13. GitHub URL: `https://github.com/Jason-Wang313/31_embodied_attention_budgeting`.

14. Local repo PDF copy: absent after the final build script removed transient `main.pdf`.

15. PDF text markers verified: `v3 final full-scale`, `12,288,000`, `greedy information`, `risk-coupled`, `76.5`, and `82.9`.
16. VLA-style visual check: link pages 5 and 6 were rendered with `pdftoppm` and inspected; one-point red internal reference boxes are crisp, aligned, and no cyan boxes appear.

Additional audit notes:
- The build used `scripts/build_pdf.ps1` and removed transient `main.pdf`.
- V3 outputs are in `results/full_scale/`.
- V2 outputs remain as provenance in `docs/toy_attention_horizon_stress.csv` and `docs/toy_attention_horizon_stress_table.tex`.
