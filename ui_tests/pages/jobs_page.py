import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ui_tests.pages.base_page import BasePage
from ui_tests.config.settings import settings
from typing import List, Dict


class JobsPage(BasePage):
    
    SEE_ALL_QA_JOBS_BUTTON = (By.XPATH, "//a[contains(text(), 'See all QA jobs')]")
    LOCATION_FILTER = (By.ID, "filter-by-location")
    DEPARTMENT_FILTER = (By.ID, "filter-by-department")
    JOB_LIST = (By.ID, "jobs-list")
    JOB_LIST_ITEM = (By.CSS_SELECTOR, ".position-list-item")
    JOB_POSITION = (By.CSS_SELECTOR, ".position-title")
    JOB_DEPARTMENT = (By.CSS_SELECTOR, ".position-department")
    JOB_LOCATION = (By.CSS_SELECTOR, ".position-location")
    VIEW_ROLE_BUTTON = (By.XPATH, ".//a[contains(text(), 'View Role')]")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = settings.QA_JOBS_PAGE_URL
    
    @allure.step("Open QA jobs page")
    def open_qa_jobs_page(self) -> None:
        self.open(self.url)
        self.wait_for_page_loaded()
    

    @allure.step("Click 'See all QA jobs' button")
    def click_see_all_qa_jobs(self) -> None:
        self.click(self.SEE_ALL_QA_JOBS_BUTTON)
    
    @allure.step("Filter jobs by location: {location}")
    def filter_by_location(self, location: str) -> None:
        location_filter = self.find_element(self.LOCATION_FILTER)
        select = Select(location_filter)
        
        def options_loaded(driver):
            select_obj = Select(location_filter)
            return len(select_obj.options) > 1
        
        self.wait.until(options_loaded)
        select.select_by_visible_text(location)
    
    @allure.step("Filter jobs by department: {department}")
    def filter_by_department(self, department: str) -> None:
        dept_filter = self.find_element(self.DEPARTMENT_FILTER)
        
        def options_loaded(driver):
            select_obj = Select(dept_filter)
            return len(select_obj.options) > 1
        
        self.wait.until(options_loaded)
        select = Select(dept_filter)
        select.select_by_visible_text(department)
    
    
    @allure.step("Get jobs list")
    def get_jobs_list(self) -> List:
        return self.find_elements(self.JOB_LIST_ITEM)
    
    @allure.step("Check if jobs list is present")
    def is_jobs_list_present(self) -> bool:
        return self.is_element_present(self.JOB_LIST)
    
    @allure.step("Get job details")
    def get_job_details(self, job_element) -> Dict[str, str]:
        try:
            position = job_element.find_element(*self.JOB_POSITION).text
        except:
            position = ""
        
        try:
            department = job_element.find_element(*self.JOB_DEPARTMENT).text
        except:
            department = ""
        
        try:
            location = job_element.find_element(*self.JOB_LOCATION).text
        except:
            location = ""
        
        return {
            "position": position,
            "department": department,
            "location": location
        }
    
    @allure.step("Click 'View Role' button")
    def click_view_role(self, job_element) -> None:
        original_window = self.driver.current_window_handle
        view_role_btn = job_element.find_element(*self.VIEW_ROLE_BUTTON)
        view_role_btn.click()
        self.wait.until(lambda driver: len(driver.window_handles) > 1)
        for window_handle in self.driver.window_handles:
            if window_handle != original_window:
                self.driver.switch_to.window(window_handle)
                break

    
    @allure.step("Check if redirected to Lever Application form page")
    def is_lever_page_opened(self) -> bool:
        """Check if current page is Lever Application form page.
        
        Note: This method should be called after click_view_role(),
        which switches to the new tab.
        """
        return "jobs.lever.co" in self.driver.current_url or "lever.co" in self.driver.current_url
