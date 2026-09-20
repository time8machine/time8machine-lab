#!/usr/bin/env python3
"""ROH/OET synthetic benchmark v0.1. Standard-library only."""

from __future__ import annotations
import argparse
import hashlib
import json
import random
from dataclasses import asdict, dataclass
from pathlib import Path

RULES = {
    "parity": lambda x: x % 2,
    "threshold": lambda x: int(x >= 5),
    "mod3zero": lambda x: int(x % 3 == 0),
}

@dataclass
class WorldResult:
    world_id: int
    seed: int
    hidden_rule: str
    fixed_success: int
    adaptive_success: int
    developmental_success: int
    fixed_classes: list[str]
    adaptive_classes: list[str]
    developmental_classes: list[str]

def strategy_class(rule_name: str, action: int) -> str:
    return f"{rule_name}:action={action}"

def predict(rule_name: str, x: int) -> int:
    if rule_name == "parity-bucket":
        return x % 2
    if rule_name == "threshold":
        return int(x >= 5)
    return int(x % 3 == 0)

def run_world(world_id: int, seed: int, trials: int = 60) -> WorldResult:
    rng = random.Random(seed)
    rule_name = rng.choice(list(RULES))
    rule = RULES[rule_name]

    fixed_success = adaptive_success = developmental_success = 0
    adaptive_classes: set[str] = set()
    developmental_classes: set[str] = set()

    for _ in range(trials):
        x = rng.randrange(10)
        target = rule(x)
        action = rng.choice((0, 1))
        fixed_success += int(action == target)

    counts = {0: [0, 0], 1: [0, 0]}
    for _ in range(trials):
        x = rng.randrange(10)
        target = rule(x)
        bucket = x % 2
        action = max((0, 1), key=lambda a: counts[bucket][a])
        adaptive_success += int(action == target)
        counts[bucket][target] += 1
        adaptive_classes.add(strategy_class("parity-bucket", action))

    learned_rule = "parity-bucket"
    for t in range(trials):
        x = rng.randrange(10)
        target = rule(x)
        action = predict(learned_rule, x)
        developmental_success += int(action == target)
        developmental_classes.add(strategy_class(learned_rule, action))

        if t >= 15 and developmental_success / (t + 1) < 0.65:
            candidates = ["parity-bucket", "threshold", "mod3zero"]
            scores = []
            for candidate in candidates:
                score = sum(
                    predict(candidate, probe) == rule(probe)
                    for probe in range(10)
                )
                scores.append((score, candidate))
            learned_rule = max(scores)[1]

    return WorldResult(
        world_id,
        seed,
        rule_name,
        fixed_success,
        adaptive_success,
        developmental_success,
        sorted({strategy_class("fixed", a) for a in (0, 1)}),
        sorted(adaptive_classes),
        sorted(developmental_classes),
    )

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worlds", type=int, default=100)
    parser.add_argument("--seed", type=int, default=20260920)
    parser.add_argument("--out", default="results/roh-bench-v0.1")
    args = parser.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    jsonl = out / "worlds.jsonl"
    manifest = out / "manifest.json"

    results = [run_world(i, args.seed + i) for i in range(args.worlds)]
    with jsonl.open("w", encoding="utf-8") as handle:
        for result in results:
            handle.write(json.dumps(asdict(result), sort_keys=True) + "\n")

    digest = hashlib.sha256(jsonl.read_bytes()).hexdigest()
    summary = {
        "benchmark": "ROH-Bench",
        "version": "0.1",
        "worlds": args.worlds,
        "seed_base": args.seed,
        "sha256_worlds_jsonl": digest,
        "status": "generated; not independently audited",
    }
    manifest.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
