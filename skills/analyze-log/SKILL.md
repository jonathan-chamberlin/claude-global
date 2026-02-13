---
name: analyze-log
description: Parse and analyze training output logs for insights. Use when user wants to understand training results, extract metrics from logs, see learning curves, or analyze episode outcomes and behavior distributions.
allowed-tools: Read, Bash, Glob, Grep
---

# Analyze Log: Training Log Parser and Analyzer

Parse training log files to extract metrics and generate insights about training performance.

## When to Use This Skill

- User asks about training results or performance
- User wants to analyze a log file
- User mentions "success rate", "reward", or "learning curve"
- User wants to understand training outcomes

## Workflow

1. **Locate logs**: Find training logs in user-specified path or common locations
2. **Parse**: Extract metrics from log files using appropriate parsing scripts
3. **Visualize**: Generate charts showing training progress
4. **Report**: Generate summary with key insights

## Quick Start

```bash
# Analyze a specific log file
python scripts/log_analyzer.py <logfile>

# Generate plots
python scripts/log_plotter.py <logfile> --output charts/

# Export to CSV
python scripts/log_analyzer.py <logfile> --csv results.csv
```

## Metrics Extracted

| Metric | Description |
|--------|-------------|
| Episode count | Total training episodes |
| Success rate | % of successful episodes (project-defined threshold) |
| Mean reward | Average episode reward |
| Max/Min reward | Best and worst episodes |
| Outcome distribution | Frequency of each outcome type |
| Learning curve | Reward over time |
| First success episode | When agent first succeeded |

## Output Example

```
=== Training Log Analysis ===
File: <logfile>
Episodes: 500

Success Rate: 78.2% (391/500)
Mean Reward: 156.3 (std: 89.2)
Max Reward: 298.5
Min Reward: -234.1

Outcome Distribution:
  <OUTCOME_A>: 45 (9.0%)
  <OUTCOME_B>: 198 (39.6%)
  <OUTCOME_C>: 89 (17.8%)
  ...

Learning Curve (50-episode windows):
  Episodes 1-50: 12% success
  Episodes 51-100: 34% success
  ...
```
