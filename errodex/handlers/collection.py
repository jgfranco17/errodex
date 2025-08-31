from typing import Dict, List

import pytest


class TestCaseRegistry:
    """Manages test case IDs and ensures uniqueness."""

    def __init__(self):
        self._node_to_caseid: Dict[str, str] = {}
        self._seen_ids: set = set()

    def register(self, nodeid: str, case_id: str):
        if case_id in self._seen_ids:
            raise pytest.UsageError(f"Duplicate test case ID detected: {case_id}")
        self._seen_ids.add(case_id)
        self._node_to_caseid[nodeid] = case_id

    def get_case_id(self, nodeid: str) -> str:
        return self._node_to_caseid.get(nodeid, "UNASSIGNED")


class FailureCollector:
    """Collects failed test results."""

    def __init__(self):
        self._failures: List[Dict[str, str]] = []

    def record_failure(self, nodeid: str, case_id: str, error: str):
        self._failures.append(
            {
                "case_id": case_id,
                "nodeid": nodeid,
                "error": error,
            }
        )

    @property
    def failures(self) -> List[Dict[str, str]]:
        return self._failures
