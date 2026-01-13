import pytest
import logging
import allure
from selenium import webdriver
from ui_tests.utils.driver_factory import create_driver, BrowserType
from ui_tests.utils.screenshot import take_screenshot

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# Track which driver instances have had cookies set
_cookies_set_for_drivers = set()


@pytest.fixture(scope="function", params=["chrome", "firefox"])
def driver(request) -> webdriver.Remote:
    browser: BrowserType = request.param
    allure.dynamic.label("browser", browser)
    driver = create_driver(browser)
    yield driver
    driver_id = id(driver)
    if driver_id in _cookies_set_for_drivers:
        _cookies_set_for_drivers.remove(driver_id)
    driver.quit()


@pytest.fixture(autouse=True)
def set_cookies(driver):
    driver_id = id(driver)
    
    if driver_id in _cookies_set_for_drivers:
        yield
        return
    
    original_driver = driver.get
    
    def get_with_cookies(url, *args, **kwargs):
        original_driver(url, *args, **kwargs)
        
        if driver_id not in _cookies_set_for_drivers:
            try:
                existing_cookies = {cookie['name'] for cookie in driver.get_cookies()}
                if "viewed_cookie_policy" not in existing_cookies:
                    cookies = [
                        {"name": "viewed_cookie_policy", "value": "yes"},
                        {"name": "cookielawinfo-checkbox-advertisement", "value": "yes"},
                        {"name": "cookielawinfo-checkbox-analytics", "value": "yes"},
                        {"name": "cookielawinfo-checkbox-functional", "value": "yes"},
                        {"name": "cookielawinfo-checkbox-necessary", "value": "yes"},
                        {"name": "cookielawinfo-checkbox-non-necessary", "value": "yes"},
                        {"name": "cookielawinfo-checkbox-others", "value": "yes"},
                        {"name": "cookielawinfo-checkbox-performance", "value": "yes"},
                    ]
                    for cookie in cookies:
                        driver.add_cookie(cookie)
                    driver.refresh()
                    _cookies_set_for_drivers.add(driver_id)
                    driver.get = original_driver
                    logger.info("Cookies set successfully")
            except Exception as e:
                logger.warning(f"Failed to set cookies: {e}")
    
    driver.get = get_with_cookies
    yield
    if driver.get == get_with_cookies:
        driver.get = original_driver


@pytest.fixture(autouse=True)
def log_test_start(request):
    logger.info(f"Starting UI test: {request.node.name}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        if "driver" in item.fixturenames:
            driver = item.funcargs.get("driver")
            if driver:
                try:
                    screenshot_path = take_screenshot(driver, item.name)
                    logger.error(f"Screenshot saved: {screenshot_path}")
                    
                    with open(screenshot_path, "rb") as screenshot_file:
                        allure.attach(
                            screenshot_file.read(),
                            name="Screenshot on Failure",
                            attachment_type=allure.attachment_type.PNG
                        )
                except Exception as e:
                    logger.error(f"Failed to attach screenshot to Allure: {e}")


def pytest_configure(config):
    config.addinivalue_line("markers", "smoke: Smoke tests")
    config.addinivalue_line("markers", "regression: Regression tests")
