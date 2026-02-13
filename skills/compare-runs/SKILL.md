---
name: compare-runs
description: Compare metrics across multiple training runs to identify best configurations. Use when user wants to compare different training sessions, find the best hyperparameters, or understand which configuration performed better.
allowed-tools: Read, Bash, Glob, Grep
---

# Compare Runs: Training Run Comparison

Compare multiple training runs to identify which configuration performed best. Key metrics include the maximum number of consecutive successes, and percentage of successes in each batch.

## When to Use This Skill

- User asks "which run was better" or "compare these runs"
- User wants to find the best configuration
- User has multiple log files to compare
- After hyperparameter sweeps to rank results

## Workflow

1. **Find logs**: Locate training logs in user-specified directories
2. **Parse all**: Extract metrics from each log
3. **Compare**: Generate comparison across runs
4. **Visualize**: Generate comparison charts
5. **Recommend**: Identify best configuration

## Quick Start

```bash
# Compare multiple log files
python scripts/compare_runs.py run1.txt run2.txt run3.txt

# Compare all logs in a directory
python scripts/compare_runs.py logs/*.txt

# Export comparison to CSV
python scripts/compare_runs.py logs/*.txt --output comparison.csv

# Generate comparison plots
python scripts/plot_comparison.py logs/*.txt --output charts/
```

## Metrics Compared

| Metric | Description | Higher is Better |
|--------|-------------|-----------------|
| Success Rate | % successful episodes (project-defined threshold) | Yes |
| Mean Reward | Average episode reward | Yes |
| Max Reward | Best single episode | Yes |
| First Success | Episode of first success | No (lower = faster) |
| Final 100 Success | Last 100 episodes success rate | Yes |
| Reward Std Dev | Consistency | No (lower = stable) |

## Output Format

```
╔══════════════════════════════════════════════════════════════════════════╗
║                        TRAINING RUN COMPARISON                           ║
╠═══════════════════════╦══════════╦══════════╦══════════╦════════════════╣
║ Run                   ║ Success% ║ Mean Rwd ║ Max Rwd  ║ First Success  ║
╠═══════════════════════╬══════════╬══════════╬══════════╬════════════════╣
║ run_config_a ⭐       ║  82.5%   ║  178.9   ║  305.2   ║    32          ║
║ run_config_b          ║  78.2%   ║  156.3   ║  298.5   ║    45          ║
║ run_baseline          ║  71.4%   ║  142.1   ║  287.6   ║    89          ║
╚═══════════════════════╩══════════╩══════════╩══════════╩════════════════╝

Best: run_config_a (82.5% success rate)
```

## Comparison Considerations

- Ensure runs have similar episode counts for fair comparison
- Consider statistical significance for close results
- Check final performance, not just averages
- Review learning curves, not just final metrics
