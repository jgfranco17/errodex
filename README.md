# ErroDex

_ErroDex — Turn failing tests into a structured errors index._

---

## About

### What is ErroDex?

ErroDex is a Pytest plugin for QA engineers and developers who want more than just stack traces.
It brings unique test case IDs, structured error tracking, and clear defect reporting into your
test workflow.

With ErroDex, every failure is logged, indexed, and documented — turning noisy test outputs into
actionable defect records.

### Features

- **Unique Test IDs:** Assign consistent, trackable IDs to each test case.
- **Failure Collection:** On test failures, ErroDex records the ID, error type, and message.
- **Defect Reports:** Generates a human-readable defect document summarizing all failures.
- **QA-Friendly:** Bridges the gap between Pytest output and formal defect tracking.
- **Configurable Output:** Choose where and how your reports are written.

## Installation

```bash
pip install errodex
```

## Usage

### Test case marking

Mark your test cases with `@errodex.mark` to assign them a unique ID.

```python
import pytest

from system_under_test.auth import login


@pytest.mark.testcase_id("TC-101")
def test_login_with_invalid_password():
    assert login("user", "wrongpass") == "Invalid credentials"
```

When running your tests, include the `--errodex` flag to enable ErroDex.

### Failure collection

When a test fails, ErroDex will automatically record the ID, error type, and message.
