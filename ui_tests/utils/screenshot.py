import os
from datetime import datetime
from pathlib import Path
from selenium import webdriver


def take_screenshot(driver: webdriver.Remote, test_name: str) -> str:
 
    screenshots_dir = Path(__file__).parent.parent.parent / "ui_tests" / "reports" / "screenshots"
    screenshots_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{test_name}_{timestamp}.png"
    screenshot_path = screenshots_dir / filename
    
    driver.save_screenshot(str(screenshot_path))
    return str(screenshot_path)
