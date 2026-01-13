import allure
import time
from ui_tests.pages.home_page import HomePage
from ui_tests.pages.jobs_page import JobsPage


@allure.feature("Jobs filtering")
class TestHappyPath:
    
    @allure.story("Happy path for jobs filtering")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_jobs_filtering(self, driver):
        home_page = HomePage(driver)
        home_page.open_home_page()
        assert home_page.is_home_page_opened(), "Home page is not opened"
        
        qa_jobs_page = JobsPage(driver)
        qa_jobs_page.open_qa_jobs_page()
        qa_jobs_page.click_see_all_qa_jobs()
        qa_jobs_page.filter_by_department("Quality Assurance")
        qa_jobs_page.filter_by_location("Istanbul, Turkiye")
        assert qa_jobs_page.is_jobs_list_present(), "Jobs list is not present"
        
        jobs = qa_jobs_page.get_jobs_list()
        assert len(jobs) > 0, "No jobs found after filtering"
        
        for job in jobs:
            job_details = qa_jobs_page.get_job_details(job)
            
            assert "Quality Assurance" in job_details["position"], \
                f"Position does not contain 'Quality Assurance': {job_details['position']}"
            
            assert "Quality Assurance" in job_details["department"], \
                f"Department does not contain 'Quality Assurance': {job_details['department']}"
            
            assert "Istanbul, Turkiye" in job_details["location"], \
                f"Location does not contain 'Istanbul, Turkiye': {job_details['location']}"
        
        if len(jobs) > 0:
            qa_jobs_page.click_view_role(jobs[0])
            assert qa_jobs_page.is_lever_page_opened(), \
                "Did not redirect to Lever Application form page"
