import pytest

from errodex.handlers.collection import FailureCollector, TestCaseRegistry
from errodex.handlers.reporting import ReportGenerator


class PluginManager:
    """Coordinates registry, failures, and reporting."""

    def __init__(self, config):
        self.registry = TestCaseRegistry()
        self.collector = FailureCollector()
        self.report_path = config.getoption("--defect-report")
        self.reporter = ReportGenerator(self.report_path)


# ------------------------
# Pytest Hook Implementations
# ------------------------


def pytest_addoption(parser):
    parser.addoption(
        "--defect-report",
        action="store",
        default="defect_report.txt",
        help="Path to write the defect report file",
    )


def pytest_configure(config):
    # Attach PluginManager to config for session-wide access
    config._testcase_plugin = PluginManager(config)

    # Register marker
    config.addinivalue_line("markers", "caseid(id): assign a unique test case ID")


def pytest_collection_modifyitems(config, items):
    manager: PluginManager = config._testcase_plugin
    for item in items:
        caseid_marker = item.get_closest_marker("caseid")
        if caseid_marker:
            case_id = caseid_marker.args[0]
            manager.registry.register(item.nodeid, case_id)


def pytest_runtest_makereport(item, call):
    if call.when == "call":
        report = pytest.TestReport.from_item_and_call(item, call)
        if report.failed:
            manager: PluginManager = item.config._testcase_plugin
            case_id = manager.registry.get_case_id(item.nodeid)
            manager.collector.record_failure(
                nodeid=item.nodeid,
                case_id=case_id,
                error=str(call.excinfo.value),
            )
        return report


def pytest_sessionfinish(session, exitstatus):
    manager: PluginManager = session.config._testcase_plugin
    manager.reporter.write_report(manager.collector.failures)

    if manager.collector.failures:
        tr = session.config.pluginmanager.get_plugin("terminalreporter")
        tr.write_line(f"\nDefect report generated: {manager.report_path}\n")
