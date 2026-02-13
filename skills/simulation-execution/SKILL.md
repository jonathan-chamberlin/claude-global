---
name: simulation-execution
description: Run the project simulation or training. Use when user asks to run, execute, start, or re-run the simulation, training, or main entry point. Also use when deciding to test changes by running the simulation.
allowed-tools: Bash, Read
---

# Simulation Execution Protocol

## STATUS
**MANDATORY** - This skill MUST be followed for all simulation runs.

## RULE
When running simulations or training, use appropriate wrappers or configurations to manage output verbosity.

## USAGE

### Starting the simulation
To run the simulation, use the project's main entry point with appropriate flags for background/quiet output:
```bash
python main.py --quiet
# or
python scripts/run_simulation.py
```

### Stopping the simulation
To stop a running simulation gracefully, use Ctrl+C or the project's stop mechanism if available.

## RATIONALE
Simulations produce high-volume diagnostic output that can exhaust an AI agent's context window and degrade long-horizon reasoning.

The wrapper/quiet mode enforces an agent-safe execution environment by:
- Automatically reducing output verbosity
- Only printing batch completion summaries
- Preventing verbose per-episode diagnostics
- Preserving agent context for interpreting trends, diagnostics, and charts

## ENFORCEMENT
- Prefer quiet/background modes when running simulations
- Do not run verbose training with full per-episode output unless specifically debugging
- Preserve agent context for interpreting results
