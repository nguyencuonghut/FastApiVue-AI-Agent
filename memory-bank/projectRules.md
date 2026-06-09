# Project Rules

## Rule 1: Never Guess

If a fact is not verified from code, tests, command output, or cited documentation, the agent must say it is unverified and inspect first.

## Rule 2: Read Bug History First

Before touching an area that has known defects or regressions, read `memory-bank/bugPatterns.md`.

## Rule 3: Preserve Memory After Fixes

Every resolved bug should leave behind a durable record:

- trigger
- root cause
- fix
- regression test or guardrail

## Rule 4: Match Existing Coding Style

When code exists, follow its:

- naming conventions
- file placement
- framework idioms
- validation patterns
- test structure

Do not introduce a new style unless the user explicitly asks for it or the existing pattern is demonstrably broken.

## Rule 5: Use Verified Tech Stack Only

The source of truth is `memory-bank/techContext.md`.

If the codebase proves the file wrong or incomplete, update the file instead of silently assuming.

## Rule 6: Prefer Reuse Over New Structure

Search for extension points before creating files, folders, services, or abstractions.

## Rule 7: Record Durable Project Knowledge

Update the Memory Bank when a task reveals:

- a recurring bug pattern
- a stable architectural rule
- a tech stack fact
- a workflow constraint

## Rule 8: Evidence Beats Confidence

Technical claims should be backed by:

- file references
- command output
- tests
- linked upstream sources
