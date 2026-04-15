"""Experiment runner — the ONLY way to execute Meta Architect.

Every run goes through this wrapper. Direct calls to MetaArchitect.run() are blocked.
All data is automatically collected, measured, judged, and saved.

Usage:
    runner = ExperimentRunner()
    result = runner.run(config)         # single run
    runner.run_experiment("EXP-SCALE")  # full experiment matrix
"""

from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from eval.auto_measure import RunMetrics, measure_all
from eval.experiment_config import (
    ExperimentConfig,
    ExperimentName,
    generate_ablation_matrix,
    generate_challenge_matrix,
    generate_model_matrix,
    generate_scale_matrix,
)
from eval.maj_eval import EvalResult, evaluate_mock

PROJECT_ROOT = Path(__file__).parent.parent
EVAL_DIR = PROJECT_ROOT / "eval" / "experiments"


class ExperimentRunner:
    """Wraps all Meta Architect executions for reproducible data collection."""

    def __init__(self, use_mock_judge: bool = True):
        self.use_mock_judge = use_mock_judge

    def run(self, config: ExperimentConfig) -> dict:
        """Execute one experimental condition and save all data.

        Returns the complete run record (config + output + metrics + scores).
        """
        run_id = str(uuid4())[:8]
        timestamp = datetime.now(timezone.utc).isoformat()

        # --- 1. Execute system ---
        start_time = time.time()
        run_output = self._execute_system(config)
        wall_time = time.time() - start_time

        # --- 2. Auto-measure ---
        metrics = measure_all(run_output)
        metrics.total_latency_sec = wall_time

        # --- 3. Judge ---
        if self.use_mock_judge:
            judge_result = evaluate_mock(run_output.get("blackboard_text", ""))
        else:
            # TODO: async judge when LLM provider ready
            judge_result = evaluate_mock(run_output.get("blackboard_text", ""))

        # --- 4. Assemble record ---
        record = {
            "run_id": run_id,
            "timestamp": timestamp,
            "experiment": config.experiment.value,
            "condition": config.condition_name,
            "scenario": config.scenario.value,
            "repetition": config.repetition,
            "config": {
                "agents": [a.value for a in config.agents],
                "models": config.models,
                "enable_phase4": config.enable_phase4,
                "enable_blackboard": config.enable_blackboard,
                "temperature": config.controls.temperature,
                "seed": config.controls.seed,
                "max_global_rounds": config.controls.max_global_rounds,
            },
            "metrics": metrics.to_dict(),
            "judge_scores": {
                "scores": [
                    {
                        "judge_role": s.judge_role,
                        "score": s.score,
                        "reasoning": s.reasoning,
                        "subscores": s.subscores,
                    }
                    for s in judge_result.scores
                ],
                "aggregate": judge_result.aggregate_score,
                "cohens_kappa": judge_result.cohens_kappa,
            },
        }

        # --- 5. Save ---
        self._save_record(record)

        return record

    def run_experiment(self, experiment: str) -> list[dict]:
        """Run all conditions for a given experiment."""
        generators = {
            "EXP-SCALE": generate_scale_matrix,
            "EXP-ABLATION": generate_ablation_matrix,
            "EXP-CHALLENGE": generate_challenge_matrix,
            "EXP-MODEL": generate_model_matrix,
        }
        gen = generators.get(experiment)
        if not gen:
            raise ValueError(f"Unknown experiment: {experiment}")

        configs = gen()
        results = []
        total = len(configs)
        for i, config in enumerate(configs, 1):
            print(f"[{i}/{total}] {config.experiment.value} | {config.condition_name} | {config.scenario.value} | rep {config.repetition}")
            result = self.run(config)
            results.append(result)
        return results

    def _execute_system(self, config: ExperimentConfig) -> dict:
        """Execute Meta Architect with given config.

        Returns raw output dict for measurement.
        TODO: Replace with actual MetaArchitect integration.
        """
        # Placeholder — returns empty output structure
        # Real implementation will call the LangGraph system
        return {
            "blackboard_text": "",
            "agent_calls": [],
            "challenges": [],
            "qoc_records": [],
            "decisions": [],
            "conflicts": [],
        }

    def _save_record(self, record: dict) -> Path:
        """Save run record to eval/experiments/{EXP}/runs/run-{id}.json."""
        exp_dir = EVAL_DIR / record["experiment"] / "runs"
        exp_dir.mkdir(parents=True, exist_ok=True)

        filename = f"run-{record['run_id']}.json"
        filepath = exp_dir / filename

        with open(filepath, "w") as f:
            json.dump(record, f, indent=2, ensure_ascii=False)

        return filepath


if __name__ == "__main__":
    # Quick smoke test with mock
    from eval.experiment_config import Controls, ExperimentConfig, ExperimentName, ScenarioID

    runner = ExperimentRunner(use_mock_judge=True)
    config = ExperimentConfig(
        experiment=ExperimentName.SCALE,
        condition_name="3-agent",
        scenario=ScenarioID.CHAT,
        repetition=1,
    )
    result = runner.run(config)
    print(f"Run {result['run_id']} saved. Metrics: {result['metrics']}")
