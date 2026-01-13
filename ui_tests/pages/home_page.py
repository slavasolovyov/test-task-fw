import allure
from ui_tests.pages.base_page import BasePage
from ui_tests.config.settings import settings


class HomePage(BasePage):
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = settings.HOME_PAGE_URL
    
    @allure.step("Open home page")
    def open_home_page(self) -> None:
        self.open(self.url)
    
    @allure.step("Check if home page is opened")
    def is_home_page_opened(self) -> bool:
        return self.driver.current_url == self.url or settings.BASE_URL in self.driver.current_url
