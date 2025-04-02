import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


class DriverBase:
    def __init__(self):
        self.driver = None

    def setup_driver(self):
        """Initialize Chrome WebDriver"""
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
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
def base_test():
    """Base fixture for test cases"""
    test = DriverBase()
    test.setup()
    yield test
    test.teardown()