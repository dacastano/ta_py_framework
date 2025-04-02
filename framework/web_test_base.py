import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeDriverManager


class BaseTest:
    def __init__(self, browser="chrome"):
        self.driver = None
        self.browser = browser.lower()

    def setup_driver(self):
        """Initialize WebDriver based on the browser"""
        if self.browser == "chrome":
            self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        elif self.browser == "firefox":
            self.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        elif self.browser == "edge":
            self.driver = webdriver.Edge(service=EdgeService(EdgeDriverManager().install()))
        else:
            raise ValueError(f"Unsupported browser: {self.browser}")

        self.driver.maximize_window()

    def teardown_driver(self):
        """Teardown WebDriver"""
        if self.driver:
            self.driver.quit()

    def setup(self):
        """Setup for the test run"""
        self.setup_driver()

    def teardown(self):
        """Teardown after the test run"""
        self.teardown_driver()


# Fixtures for pytest
@pytest.fixture(scope="function")
def base_test(request):
    """Base fixture to be used in the test cases"""
    browser = request.config.getoption("--browser", default="chrome")
    test = BaseTest(browser)
    test.setup()
    yield test
    test.teardown()


# Command-line options for pytest to select the browser
def pytest_addoption(parser):
    """Add browser option to pytest CLI"""
    parser.addoption(
        "--browser", action="store", default="chrome", help="Select browser: chrome, firefox, edge"
    )