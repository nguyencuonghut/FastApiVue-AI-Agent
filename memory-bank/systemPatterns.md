# System Patterns

## Agent Workflow Pattern

This repository uses a two-layer memory pattern:

1. `AGENTS.md` for always-loaded startup instructions
2. `memory-bank/` for durable, human-readable project context

## Memory Pattern

The chosen memory design is adapted from `axiomhq/agent-memory`:

1. capture durable learning
2. consolidate into structured memory
3. surface hot memory into startup instructions

## Documentation Pattern

If code and docs disagree:

1. verify with code or commands
2. fix the docs
3. record any recurring mismatch as a bug pattern
