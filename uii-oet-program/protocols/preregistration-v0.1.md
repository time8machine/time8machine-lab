# Preregistration v0.1 — ROH/OET Synthetic Benchmark

## Objective

Test whether agents exposed to hidden-rule worlds exhibit measurable differences in transformation-space expansion under controlled feedback and adaptation conditions.

## Primary hypothesis

Agents receiving informative consequence feedback and capable of retaining successful strategy changes will acquire more distinct transformation classes than agents restricted to a fixed strategy repertoire.

## Exploratory hypothesis

Greater feedback fidelity will be associated with greater transformation-space expansion.

## Unit of analysis

One synthetic world × one agent configuration × one random seed.

## Planned sample

100 independently seeded synthetic worlds.

## Conditions

- fixed-repertoire baseline
- adaptive baseline
- feedback-manipulated condition
- open-ended developmental condition

The executable implementation may begin with a smoke test; the preregistered 100-world run is the target benchmark.

## Primary outcome

Transformation-class expansion, operationalized in v0.1 as the number of distinct strategy classes acquired after interaction, with the class definition fixed in code before the target run.

## Secondary outcomes

Task success, hidden-rule inference, failed interventions, adaptation events, persistence of acquired strategy, and residual obstruction.

## Exclusions

Worlds are excluded only for documented software or data corruption identified by automated validation or an independent audit rule established before result inspection.

## Interpretation

A positive result would constitute evidence relevant to the narrower claim that controlled developmental conditions can produce measurable expansion of a defined transformation space. It would not establish general intelligence.
