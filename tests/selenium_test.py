"""Integration + UI tests for the search web app, driven through a
remote Selenium server over HTTP (no direct backend calls)."""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = "http://localhost:5000"
SELENIUM_URL = "http://localhost:4444"
WAIT_SECONDS = 10


def new_driver():
    options = Options()
    options.add_argument("--headless=new")
    return webdriver.Remote(command_executor=SELENIUM_URL, options=options)


def test_valid_search_reaches_result_page(driver):
    """Integration test: browser -> Flask -> Postgres -> rendered result."""
    driver.get(BASE_URL)
    driver.find_element(By.ID, "search_term").send_keys("Selenium Test")
    driver.find_element(By.CSS_SELECTOR, "button[type=submit]").click()

    WebDriverWait(driver, WAIT_SECONDS).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Back to Home"))
    )
    assert "Selenium Test" in driver.page_source


def test_frontend_blocks_xss_payload(driver):
    """UI test: client-side validation stops the request and clears the field."""
    driver.get(BASE_URL)
    field = driver.find_element(By.ID, "search_term")
    field.send_keys("<script>alert(1)</script>")
    driver.find_element(By.CSS_SELECTOR, "button[type=submit]").click()

    WebDriverWait(driver, WAIT_SECONDS).until(EC.alert_is_present())
    driver.switch_to.alert.accept()

    field = driver.find_element(By.ID, "search_term")
    assert field.get_attribute("value") == ""


def test_backend_rejects_sqli_payload(driver):
    """Integration test: bypass the frontend JS and confirm the backend
    independently rejects the payload (defense in depth)."""
    driver.get(BASE_URL)
    driver.find_element(By.ID, "search_term").send_keys("' OR '1'='1' --")
    driver.execute_script("document.getElementById('search-form').submit();")

    WebDriverWait(driver, WAIT_SECONDS).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Invalid search term")
    )
    field = driver.find_element(By.ID, "search_term")
    assert field.get_attribute("value") == ""


TESTS = [
    test_valid_search_reaches_result_page,
    test_frontend_blocks_xss_payload,
    test_backend_rejects_sqli_payload,
]


def main():
    driver = new_driver()
    try:
        for test in TESTS:
            test(driver)
            print(f"PASS: {test.__name__}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
