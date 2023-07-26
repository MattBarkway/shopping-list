import pytest


def pytest_addoption(parser):
    # add a pytest flag to skip integration tests
    parser.addoption(
        "--integration",
        action="store_true",
        default=False,
        help="run integration tests",
    )


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "integration: mark test as a slow-running integration test"
    )


def pytest_collection_modifyitems(config, items):
    if config.getoption("--integration"):
        return
    skip_integration = pytest.mark.skip(reason="need --integration flag to run")
    for item in items:
        if "integration" in item.keywords:
            item.add_marker(skip_integration)
