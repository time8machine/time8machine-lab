# ROH-Bench v0.1

A minimal synthetic benchmark for testing adaptation, hidden-rule inference, and transformation-class expansion.

Each world contains a hidden rule mapping observations to successful interventions. Agents receive observations and consequence feedback.

The benchmark compares fixed repertoire, adaptive strategy selection, and open-ended strategy generation.

The initial implementation deliberately uses transparent discrete mechanisms rather than a large model so that every result can be inspected.

Run:
python uii-oet-program/experiments/roh-bench/run_experiment.py --worlds 100 --seed 20260920

This is a research instrument, not evidence of general intelligence.
