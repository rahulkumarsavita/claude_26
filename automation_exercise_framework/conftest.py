import base64
import os
from datetime import datetime

import pytest

from utils.driver_factory import get_driver

SCREENSHOTS_DIR = os.path.join(os.path.dirname(__file__), "screenshots")


@pytest.fixture(scope="function")
def driver():
    drv = get_driver()
    yield drv
    drv.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        drv = item.funcargs.get("driver")
        if drv is None:
            return

        os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{item.name}_{timestamp}.png"
        filepath = os.path.join(SCREENSHOTS_DIR, filename)
        drv.save_screenshot(filepath)

        pytest_html = item.config.pluginmanager.getplugin("html")
        if pytest_html is not None:
            extras = getattr(report, "extras", [])
            with open(filepath, "rb") as image_file:
                encoded = base64.b64encode(image_file.read()).decode("ascii")
            extras.append(pytest_html.extras.image(encoded, mime_type="image/png"))
            report.extras = extras
