---
name: sweep
description: Run hyperparameter sweep experiments for RL training. Use when user wants to test multiple hyperparameter configurations, find optimal settings, tune learning rates, or compare different training setups systematically.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Hyperparameter Sweep

Help the user set up and run hyperparameter sweeps for RL training.

## When to Use This Skill

- User wants to find optimal hyperparameters
- User wants to run an experiment
- User mentions "sweep", "grid search", "hyperparameter tuning"
- User wants to compare multiple configurations systematically
- User wants to improve how fast the agent learns and reaches a successful stable state

## Common Hyperparameters

Training hyperparameters (check project's config for specifics):
- `actor_lr` / `learning_rate` - Learning rate for actor/policy network
- `critic_lr` - Learning rate for critic/value network
- `batch_size` - Training batch size
- `buffer_size` - Replay buffer capacity
- `gamma` - Discount factor
- `tau` - Target network soft update rate
- `policy_update_frequency` - Delayed policy updates (TD3)
- `training_updates_per_episode` - Updates per episode

Exploration hyperparameters:
- `sigma` - Noise sigma
- `theta` - Noise theta (for OU noise)
- `noise_scale_initial` - Starting noise multiplier
- `noise_scale_final` - Final noise multiplier
- `noise_decay_episodes` - Episodes to decay noise

## Workflow

1. **Generate config**: Run `python scripts/generate_config.py` to create a sweep configuration
2. **Execute sweep**: Run `python scripts/sweep_runner.py config.json` to execute
3. **Analyze results**: Run `python scripts/analyze_results.py results_dir/` to summarize

## Reference Documentation

- For recommended parameter ranges, see [hyperparameter_ranges.md](references/hyperparameter_ranges.md)
- For sweep strategy guidance, see [sweep_strategies.md](references/sweep_strategies.md)

## Example Sweep Config

```json
{
  "name": "lr_sweep",
  "type": "grid",
  "episodes_per_run": 500,
  "parameters": {
    "actor_lr": [0.0005, 0.001, 0.002],
    "critic_lr": [0.001, 0.002, 0.004]
  }
}
```

## Output

Results saved to `sweep_results/[timestamp]/` with:
- Individual run logs
- Summary CSV with all configurations and metrics
- Best configuration recommendation
