"""Auto-generate paper tables and figures from experiment data.

Reads eval/experiments/*/runs/*.json and produces:
- Table 1: Agent count vs quality (EXP-SCALE)
- Table 2: Ablation study (EXP-ABLATION)
- Table 3: Model diversity effect (EXP-MODEL)
- Figure 1: Scaling curve with logistic fit
- Figure 2: Cost-quality Pareto frontier
- Figure 3: Challenge phase impact (EXP-CHALLENGE)

Output: eval/paper/tables/*.md, eval/paper/figures/*.png
"""

from __future__ import annotations

import json
import statistics
from pathlib import Path

EVAL_DIR = Path(__file__).parent.parent / "experiments"
OUTPUT_DIR = Path(__file__).parent


def load_runs(experiment: str) -> list[dict]:
    """Load all run records for an experiment."""
    runs_dir = EVAL_DIR / experiment / "runs"
    if not runs_dir.exists():
        return []
    runs = []
    for f in sorted(runs_dir.glob("run-*.json")):
        with open(f) as fp:
            runs.append(json.load(fp))
    return runs


def group_by_condition(runs: list[dict]) -> dict[str, list[dict]]:
    """Group runs by condition name."""
    groups: dict[str, list[dict]] = {}
    for run in runs:
        cond = run["condition"]
        groups.setdefault(cond, []).append(run)
    return groups


def mean_std(values: list[float]) -> tuple[float, float]:
    if not values:
        return 0.0, 0.0
    m = statistics.mean(values)
    s = statistics.stdev(values) if len(values) > 1 else 0.0
    return round(m, 2), round(s, 2)


def generate_table_1():
    """Table 1: Effect of Agent Count on Architecture Quality."""
    runs = load_runs("EXP-SCALE")
    if not runs:
        print("No EXP-SCALE data found.")
        return

    groups = group_by_condition(runs)
    order = ["1-agent", "3-agent", "6-agent", "10-agent", "17-agent"]

    lines = [
        "# Table 1: Effect of Agent Count on Architecture Quality",
        "",
        "| Condition | Coverage | Quality | Cost ($) | Latency (s) | Rounds |",
        "|-----------|----------|---------|----------|-------------|--------|",
    ]

    for cond in order:
        cond_runs = groups.get(cond, [])
        if not cond_runs:
            lines.append(f"| {cond} | - | - | - | - | - |")
            continue

        cov_m, cov_s = mean_std([r["metrics"]["concept_coverage"] for r in cond_runs])
        qual_m, qual_s = mean_std([r["judge_scores"]["aggregate"] for r in cond_runs])
        cost_m, cost_s = mean_std([r["metrics"]["total_cost_usd"] for r in cond_runs])
        lat_m, lat_s = mean_std([r["metrics"]["total_latency_sec"] for r in cond_runs])
        rnd_m, rnd_s = mean_std([r["metrics"]["total_rounds"] for r in cond_runs])

        lines.append(
            f"| {cond} | {cov_m} +/- {cov_s} | {qual_m} +/- {qual_s} | "
            f"${cost_m} +/- {cost_s} | {lat_m} +/- {lat_s} | {rnd_m} +/- {rnd_s} |"
        )

    output = OUTPUT_DIR / "tables" / "table_1_scale.md"
    output.write_text("\n".join(lines))
    print(f"Generated: {output}")


def generate_table_2():
    """Table 2: Ablation Study — Individual Agent Contribution."""
    runs = load_runs("EXP-ABLATION")
    if not runs:
        print("No EXP-ABLATION data found.")
        return

    # Get baseline (17-agent) from EXP-SCALE
    scale_runs = load_runs("EXP-SCALE")
    baseline_runs = [r for r in scale_runs if r["condition"] == "17-agent"]
    if baseline_runs:
        baseline_quality = statistics.mean([r["judge_scores"]["aggregate"] for r in baseline_runs])
    else:
        baseline_quality = 0.0

    groups = group_by_condition(runs)

    lines = [
        "# Table 2: Ablation Study — Individual Agent Contribution",
        "",
        f"Baseline (17-agent) quality: {round(baseline_quality, 2)}",
        "",
        "| Removed Agent | Quality | Delta | Coverage Delta |",
        "|--------------|---------|-------|---------------|",
    ]

    for cond_name in sorted(groups.keys()):
        cond_runs = groups[cond_name]
        qual_m, _ = mean_std([r["judge_scores"]["aggregate"] for r in cond_runs])
        cov_m, _ = mean_std([r["metrics"]["concept_coverage"] for r in cond_runs])

        baseline_cov_runs = [r for r in baseline_runs]
        baseline_cov = statistics.mean([r["metrics"]["concept_coverage"] for r in baseline_cov_runs]) if baseline_cov_runs else 0

        delta_q = round(qual_m - baseline_quality, 2)
        delta_c = round(cov_m - baseline_cov, 1)
        sign_q = "+" if delta_q >= 0 else ""
        sign_c = "+" if delta_c >= 0 else ""

        agent_name = cond_name.replace("without-", "")
        lines.append(f"| {agent_name} | {qual_m} | {sign_q}{delta_q} | {sign_c}{delta_c} |")

    output = OUTPUT_DIR / "tables" / "table_2_ablation.md"
    output.write_text("\n".join(lines))
    print(f"Generated: {output}")


def generate_table_3():
    """Table 3: Effect of Model Diversity."""
    runs = load_runs("EXP-MODEL")
    if not runs:
        print("No EXP-MODEL data found.")
        return

    groups = group_by_condition(runs)

    lines = [
        "# Table 3: Effect of Model Diversity",
        "",
        "| Model Config | Quality | Coverage | Unique Perspectives | Cost ($) |",
        "|-------------|---------|----------|--------------------|---------| ",
    ]

    for cond in ["all-opus", "mixed", "all-sonnet"]:
        cond_runs = groups.get(cond, [])
        if not cond_runs:
            lines.append(f"| {cond} | - | - | - | - |")
            continue

        qual_m, qual_s = mean_std([r["judge_scores"]["aggregate"] for r in cond_runs])
        cov_m, _ = mean_std([r["metrics"]["concept_coverage"] for r in cond_runs])
        uniq_m, _ = mean_std([r["metrics"]["unique_perspectives"] for r in cond_runs])
        cost_m, _ = mean_std([r["metrics"]["total_cost_usd"] for r in cond_runs])

        lines.append(f"| {cond} | {qual_m} +/- {qual_s} | {cov_m} | {uniq_m} | ${cost_m} |")

    output = OUTPUT_DIR / "tables" / "table_3_model.md"
    output.write_text("\n".join(lines))
    print(f"Generated: {output}")


def generate_figure_1():
    """Figure 1: Scaling curve with logistic fit (H2).

    Fits Q = L / (1 + exp(-k*(N - N0))) to agent count vs quality.
    Reference: Qian et al. (ICLR 2025, arXiv:2406.07155) [src:paper-B1][UNVERIFIED]
    """
    runs = load_runs("EXP-SCALE")
    if not runs:
        print("No EXP-SCALE data for Figure 1.")
        return

    try:
        import numpy as np
        from scipy.optimize import curve_fit
    except ImportError:
        print("Figure 1 requires: pip install numpy scipy matplotlib")
        return

    groups = group_by_condition(runs)
    agent_counts = {"1-agent": 1, "3-agent": 3, "6-agent": 6, "10-agent": 10, "17-agent": 17}

    x_data, y_data = [], []
    for cond, n in agent_counts.items():
        cond_runs = groups.get(cond, [])
        if cond_runs:
            for r in cond_runs:
                x_data.append(n)
                y_data.append(r["judge_scores"]["aggregate"])

    if len(set(x_data)) < 3:
        print("Figure 1: Need at least 3 distinct agent counts for logistic fit.")
        return

    x = np.array(x_data, dtype=float)
    y = np.array(y_data, dtype=float)

    def logistic(n, L, k, n0):
        return L / (1.0 + np.exp(-k * (n - n0)))

    try:
        popt, pcov = curve_fit(logistic, x, y, p0=[5.0, 0.5, 5.0], maxfev=5000)
        L, k, n0 = popt

        y_pred = logistic(x, *popt)
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else 0

        stats_path = OUTPUT_DIR / "stats" / "figure_1_logistic.md"
        stats_path.parent.mkdir(parents=True, exist_ok=True)
        stats_path.write_text(
            f"# Figure 1: Logistic Fit Parameters\n\n"
            f"Q = L / (1 + exp(-k*(N - N0)))\n\n"
            f"- L (upper asymptote) = {L:.3f}\n"
            f"- k (growth rate) = {k:.3f}\n"
            f"- N0 (midpoint) = {n0:.1f}\n"
            f"- R-squared = {r_squared:.4f}\n\n"
            f"Data points: {len(x_data)}\n"
            f"Distinct agent counts: {sorted(set(x_data))}\n"
        )
        print(f"Generated: {stats_path} (R²={r_squared:.4f})")

    except Exception as e:
        print(f"Figure 1 logistic fit failed: {e}")

    try:
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(8, 5))

        means = {}
        for cond, n in agent_counts.items():
            cond_runs = groups.get(cond, [])
            if cond_runs:
                scores = [r["judge_scores"]["aggregate"] for r in cond_runs]
                means[n] = (statistics.mean(scores), statistics.stdev(scores) if len(scores) > 1 else 0)

        xs = sorted(means.keys())
        ys = [means[n][0] for n in xs]
        errs = [means[n][1] for n in xs]
        ax.errorbar(xs, ys, yerr=errs, fmt="o", capsize=5, label="Observed")

        if "popt" in dir():
            x_smooth = np.linspace(1, 17, 100)
            ax.plot(x_smooth, logistic(x_smooth, *popt), "--", label=f"Logistic fit (R²={r_squared:.3f})")

        ax.set_xlabel("Number of Agents")
        ax.set_ylabel("Quality Score (1-5)")
        ax.set_title("Effect of Agent Count on Architecture Quality")
        ax.legend()
        ax.set_xticks([1, 3, 6, 10, 17])

        fig_path = OUTPUT_DIR / "figures" / "figure_1_scaling.png"
        fig_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(fig_path, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"Generated: {fig_path}")

    except ImportError:
        print("Figure 1 PNG requires: pip install matplotlib")


def generate_all():
    """Generate all tables and figures."""
    print("=== Generating Paper Tables & Figures ===\n")
    generate_table_1()
    generate_table_2()
    generate_table_3()
    generate_figure_1()
    print("\n=== Done ===")


if __name__ == "__main__":
    generate_all()
