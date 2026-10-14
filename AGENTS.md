# Mini Product Assistant — Repository Instructions

This is an educational project for the Decision Support Systems course. It evolves class by class to teach how to build applications with LLMs. Keep it intentionally simple: readability, ease of explanation, and a clear learning path matter more than production-scale abstraction. Inspect the repository before assuming implementation details.

## General Principles

- Keep the code simple, readable, and easy to explain.
- Prefer small, focused functions over large abstractions.
- Use clear and descriptive names.
- Follow the existing project structure and conventions.
- Avoid unnecessary refactors.
- Avoid adding dependencies unless they are clearly needed.
- Do not modify unrelated files.
- Prefer the smallest change that correctly solves the task.

## Before Making Changes

Before editing code:

1. Inspect the relevant parts of the repository.
2. Read the files involved in the task.
3. Review related tests when they exist.
4. Understand the current behavior before changing it.
5. Check whether the repository already contains a pattern or abstraction that should be reused.

Do not assume how the project works without inspecting it first.

## Implementation

When implementing a task:

- Respect the existing architecture.
- Keep changes limited to the requested behavior.
- Reuse existing code when appropriate.
- Avoid premature abstractions.
- Do not introduce new frameworks or architectural patterns without a clear reason.
- Preserve existing behavior unless the task explicitly requires changing it.
- Use type hints where they are already part of the project conventions.

## Testing

After changing behavior:

- Run the relevant tests.
- Add or update tests when appropriate.
- Keep tests deterministic whenever possible.
- Do not change tests only to make them pass without understanding the failure.
- Run the full test suite before finishing when reasonable.

Use the repository's existing testing tools and conventions.

## Documentation

Update documentation only when the change makes existing documentation inaccurate or incomplete.

Keep documentation concise and aligned with the actual implementation.

## Code Review

Before considering a task complete:

- Review the diff.
- Check for unrelated changes.
- Check for unnecessary complexity.
- Verify that the implementation matches the task.
- Verify that tests cover the relevant behavior.
- Make sure no existing behavior was unintentionally changed.

## Definition of Done

A task is complete when:

- the requested behavior is implemented;
- relevant tests pass;
- existing behavior is preserved unless intentionally changed;
- the diff is focused and understandable;
- no unnecessary dependencies or abstractions were introduced;
- the final changes can be clearly explained.