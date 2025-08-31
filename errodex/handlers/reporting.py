from typing import Dict, List


class ReportGenerator:
    """Generates human-readable defect reports."""

    def __init__(self, path: str):
        self._path = path

    def write_report(self, failures: List[Dict[str, str]]):
        if not failures:
            return

        with open(self._path, "w", encoding="utf-8") as f:
            f.write("=== DEFECT REPORT ===\n\n")
            for failure in failures:
                f.write(f"Test Case ID: {failure['case_id']}\n")
                f.write(f"Test: {failure['nodeid']}\n")
                f.write(f"Error: {failure['error']}\n")
                f.write("-" * 50 + "\n")
