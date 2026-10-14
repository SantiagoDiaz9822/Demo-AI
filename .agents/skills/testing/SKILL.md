---
name: testing
description: Add, modify, or repair tests for Mini Product Assistant behavior while keeping validation deterministic and aligned with the repository's existing pytest conventions.
---

# Testing Skill

Use this Skill when a task adds, modifies, or fixes behavior that should be validated with tests.

## Goal

Validate observable behavior, prevent regressions, and keep tests clear and deterministic without coupling them unnecessarily to implementation details.

## Workflow

### 1. Understand the expected behavior

Read the complete task and its acceptance criteria. Inspect the relevant implementation, related tests, and current behavior before writing or changing a test.

### 2. Identify relevant test cases

Select the smallest valuable set covering:

- The successful case.
- Relevant edge cases.
- Expected errors.
- Existing behavior that must not regress.

Do not add arbitrary cases that do not protect a meaningful contract.

### 3. Prefer deterministic tests

Avoid dependencies on internet access, real LLM or embedding calls, external APIs, paid services, current time, or uncontrolled random data. Use pytest fixtures, `monkeypatch`, fakes, or mocks when they make the boundary clearer; do not mock indiscriminately.

### 4. Write the smallest useful test

Give each test a descriptive name and verify one clear behavior. Keep setup and assertions explicit, avoid complex test logic, and do not combine unrelated behaviors in one test.

### 5. Run focused tests first

Run the directly related test module or test case first. Fix failures, then run the full suite with `pytest` when reasonable.

### 6. Investigate failures

When a test fails:

1. Understand the failure.
2. Decide whether the cause is production code, the test, test data, or the environment.
3. Fix the cause.
4. Rerun the focused tests and then the broader suite as appropriate.

Do not delete tests, remove or weaken assertions, change expected results without justification, or ignore errors merely to obtain a green suite. Update expectations only when the task intentionally changes the expected behavior.

### 7. Final verification

Confirm that new and relevant existing tests pass, the full suite passes when appropriate, no unexpected external calls occur, acceptance criteria are covered, and the implementation remains simple.

## Testing AI-related Code

### LLM

- Do not make real Ollama or other LLM calls in unit tests.
- Replace provider responses with small deterministic fakes when needed.
- Test deterministic validation, prompt inputs, schema handling, and data transformations separately.

### Structured Outputs

Test Pydantic model validation, optional fields, normalization, serialization, unknown or invalid fields, and malformed provider responses deterministically.

### RAG

- Test deterministic pieces such as catalog loading, the one-row-to-one-document transformation, metadata, context construction, ingestion coordination, and vector-store behavior.
- Use small local datasets and explicit vectors. If a requested change introduces chunking, test its boundaries and metadata without using a live model.
- Keep real embedding or LLM queries in optional integration, manual, or demo tests; they must not be required by the unit suite.

## What Not to Do

- Do not write tests that merely reproduce the implementation.
- Do not create brittle assertions around irrelevant formatting.
- Do not add testing dependencies unless necessary.
- Do not modify production code solely to make a test easier when a simpler alternative exists.
- Do not change existing tests without understanding the contract they protect.
- Do not make real LLM calls to verify basic functionality.
