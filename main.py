import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import page
import time


class PythonOrgSearchTTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(
            service=Service('/usp/Local/bin/chromedriver'))
        self.driver.get("https://www.mercari.com/")

    def test_search_python(self):
        mainPage = page.MainPage(self.driver)
        assert mainPage.is_title_matches()
        mainPage.search_text_element = "apple"
        mainPage.close_welcome_message()
        search_result_page = page.SearchResultPage(self.driver)
        assert search_result_page.is_results_found()
        search_result_page.applying_filters("2")
        search_result_page.find_most_recent()
        search_result_page.wait_for_change()
        search_result_page.grabs_url()
        search_result_page.discord_bot()
        third_result_page = page.ThirdPageResults(self.driver)
        assert third_result_page.is_results_found()

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
