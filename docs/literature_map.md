# Literature Map

## Field box

The relevant field is not generic "attention" in embodied AI. It is the robotics subfield that treats sensing as an action: active perception, active sensing, sensor scheduling, information gathering, visual search, view planning, and perception-aware navigation/manipulation.

The literature mostly assumes:

1. sensing is cheap relative to control,
2. sensor choice can be optimized independently of closed-loop risk,
3. extra observations are always good if information gain rises,
4. compute/latency are implementation details rather than first-class physical resources,
5. uncertainty is the primary objective proxy for perception.

This paper should only claim novelty if it breaks at least one of those assumptions in a way that matters for robot behavior.

## 1000-paper landscape sweep

The local matrix `docs/related_work_matrix.csv` contains 2,013 deduplicated papers harvested from arXiv-style robotics and robotics-adjacent queries. It is broad enough to support a 1000-paper sweep requirement, but the actual thematic center is much narrower.

## 300-paper serious skim

The serious skim should be centered on the active-perception cluster and adjacent support papers:

- active perception / active sensing
- information gathering and view planning
- sensor scheduling and mobility-aware sensing
- tactile and visuo-tactile perception
- perception-aware control and manipulation
- world models used for planning under partial observability
- uncertainty-aware but still decoupled sensor selection

## Deep-read shortlist

The deepest reads are the papers that either:

- make sensing a decision variable,
- connect sensing to control or task risk,
- or explicitly exploit embodiment to change what is observable.

Recommended deep-read anchors:

- `Active Sensing for Robotics – A Survey`
- `Decentralized Active Information Acquisition: Theory and Application to Multi-Robot SLAM`
- `Attention-Based Planning with Active Perception`
- `Exploiting Submodular Value Functions For Scaling Up Active Perception`
- `Multi-Modal Active Perception for Information Gathering in Science Missions`
- `One-Shot Informed Robotic Visual Search in the Wild`
- `Active Perception and Representation for Robotic Manipulation`
- `Robot Active Neural Sensing and Planning in Unknown Cluttered Environments`
- `Learning to See Physical Properties with Active Sensing Motor Policies`
- `Active Perception using Neural Radiance Fields`
- `An Active Perception Game for Robust Information Gathering`
- `Vision in Action: Learning Active Perception from Human ...`
- `Apple: Toward General Active Perception via Reinforcement Learning`
- `Co-GLANCE: Uncertainty-Aware Active Perception for Heterogeneous Robot Teaming`

## Mechanism-level takeaways

### 1. Active perception as information gain maximization

Problem claimed: choose observations that reduce uncertainty.

Actual mechanism introduced: score candidate views, motions, or sensing actions using entropy, mutual information, or submodular value.

Hidden assumptions:

- uncertainty correlates with task risk,
- the robot can afford the sensing action,
- all sensing actions are interchangeable except for expected information gain,
- control can wait until sensing is done,
- and the state estimate is the right objective.

Failure modes ignored:

- high-information observations that are too slow, too risky, or too expensive,
- sensing that worsens safety because the robot must enter a bad physical configuration,
- and "informative" observations that are irrelevant to task success.

What it makes less novel:

- any method that merely chooses better views, better frames, or better sensor placements with standard information gain.

What it leaves open:

- how to budget sensing when the robot is under real control risk,
- how to trade latency, power, and safety against information gain,
- and how to make sensing compete with actuation rather than float above it.

### 2. Sensor scheduling and multi-robot information gathering

Problem claimed: distribute sensors or agents to maximize coverage or information.

Actual mechanism introduced: combinatorial optimization over measurement locations, time, and limited communication.

Hidden assumptions:

- sensing capacity is the main bottleneck,
- action risk is separable,
- and one can treat sensing as an exogenous resource allocation problem.

What it leaves open:

- embodied tradeoffs where the sensing action changes controllability and safety.

### 3. Perception-aware manipulation and navigation

Problem claimed: improve manipulation/navigation by moving the sensor or choosing the next best view.

Actual mechanism introduced: perception policy is coupled to the task policy, often through imitation, RL, or search.

Hidden assumptions:

- the new observation is always worth pursuing if it improves success probability,
- and the robot can choose among views without changing the essential risk envelope.

What it leaves open:

- explicit attention budgets,
- physical cost of maintaining attention,
- and the possibility that too much sensing is dangerous or wasted because the task should proceed.

### 4. Tactile and visuo-tactile active perception

Problem claimed: use contact to disambiguate object properties.

Actual mechanism introduced: deliberate interaction reveals hidden properties.

Hidden assumptions:

- contact is acceptable once uncertainty is high enough,
- and the robot can pay the interaction cost.

What it leaves open:

- a shared budget across visual, tactile, and proprioceptive attention modes.

## Working thesis candidate

The strongest direction is:

> Treat attention as a limited embodied resource that must be budgeted jointly with control risk, not as a free choice among information-rich observations.

This is stronger than "active perception" because the central variable is not uncertainty reduction. It is the joint feasibility of sensing and acting under a budget that can be consumed by physical movement, latency, and hazard exposure.

## Why this is potentially novel

Existing work usually optimizes sensing because it is informative. Much less of it treats sensing itself as something that can be over-consumed, or as a resource whose use must be justified against immediate control risk.

That suggests a paper around a new central mechanism:

- a risk-weighted attention budget,
- a consumption rule for sensing actions,
- and an evaluation that shows the robot behaves differently once sensing is no longer free.
