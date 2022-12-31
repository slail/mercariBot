import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import page


class PythonOrgSearchTTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(
            service=Service('/usp/Local/bin/chromedriver'))
        self.driver.get("https://www.python.org/")

    def test_search_python(self):
        mainPage = page.MainPage(self.driver)
        assert mainPage.is_title_matches()
        mainPage.search_text_element = "pycon"
        mainPage.click_go_button()
        search_result_page = page.SearchResultPage(self.driver)
        assert search_result_page.is_results_found()

    def tearDown(self):

        self.driver.close()


if __name__ == "__main__":
    unittest.main()
