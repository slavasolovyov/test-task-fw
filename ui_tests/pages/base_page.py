import logging
import json
import time
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from typing import List
from ui_tests.config.settings import settings

logger = logging.getLogger(__name__)


class BasePage:

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, settings.IMPLICIT_WAIT)
    
    def open(self, url: str) -> None:
        self.driver.get(url)
    
    def find_element(self, locator: tuple):
        element = self.driver.find_element(*locator)
        self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});",
                element      
            )
        return self.wait.until(EC.visibility_of(element))
    
    def find_elements(self, locator: tuple) -> List:
        def elements_loaded(driver):
            elements = driver.find_elements(*locator)
            return elements if len(elements) > 0 else False
        
        elements = self.wait.until(elements_loaded)
        return elements
        
    
    def click(self, locator: tuple) -> None:
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
    
    def get_text(self, locator: tuple) -> str:
        element = self.find_element(locator)
        return element.text
    
    def is_element_present(self, locator: List) -> bool:
        try:
            self.wait.until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    def wait_for_page_loaded(self) -> None:
        self.wait.until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
