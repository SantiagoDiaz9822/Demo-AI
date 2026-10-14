---
name: code-review
description: Review a code change against its task, repository conventions, architecture, and tests before approving it as complete.
---

# Code Review Skill

Use this Skill to review a completed or proposed change. Review for correctness and scope using repository evidence, not appearance.

## Workflow

### 1. Establish the contract

- Read the original task, acceptance criteria, and repository instructions.
- Identify required behavior, explicit constraints, and behavior that must remain unchanged.
- Verify every assumption against the repository. Do not trust AI-generated code merely because it looks plausible.

### 2. Inspect the change

- Read the complete diff and every affected file in context.
- Trace changed behavior through callers, data models, boundaries, and relevant configuration.
- Flag unrelated edits, unnecessary rewrites, generated noise, or missing requested changes.

### 3. Review correctness and design

- Confirm the implementation satisfies the task without unintended behavior changes.
- Check consistency with the existing architecture, conventions, error handling, and dependency boundaries.
- Look for duplicated logic, invented APIs or repository conventions, unnecessary dependencies, premature abstractions, and over-engineering.
- Confirm future functionality was not implemented before the task requested it.

### 4. Review tests and regressions

- Check that tests cover the acceptance criteria, important errors, edge cases, and behavior at risk of regression.
- Ensure assertions validate observable behavior and tests remain deterministic.
- Run focused tests first and the full suite when reasonable. Investigate failures rather than weakening tests.
- Note untested risks explicitly; passing tests do not replace code inspection.

### 5. Report findings

Report only actionable findings, with the affected file and location, evidence, impact, and a concise correction. Order findings by severity:

- **Blocking**: Incorrect behavior, security or data-loss risk, broken acceptance criteria, failing required tests, or a change that cannot be approved safely.
- **Important**: A meaningful regression risk, architectural inconsistency, missing valuable coverage, or unnecessary complexity that should be fixed before completion.
- **Minor**: A localized clarity or maintainability issue with low behavioral risk.

Do not inflate severity or report style preferences as defects. If there are no findings, say so and mention any remaining verification gap.

## Final Approval Checklist

Approve only when:

- [ ] The acceptance criteria and constraints are satisfied.
- [ ] The diff is limited to necessary, understandable changes.
- [ ] Behavior matches repository evidence and no unintended behavior changed.
- [ ] Architecture and existing conventions remain consistent.
- [ ] No over-engineering, duplicated logic, invented API, or unnecessary dependency remains.
- [ ] No future capability was added prematurely.
- [ ] Relevant tests pass and regression risks are acceptably covered.
- [ ] No unresolved Blocking or Important finding remains.
