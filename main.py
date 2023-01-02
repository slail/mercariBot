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
        searchItem = input("What item are you looking to buy: ")
        sortBy = input(
            "How would you like to sort your item by?\n(1) best match \n(2) newest first \n(3) lowest price first \n(4) highest price first \nEnter Number: ")
        mainPage = page.MainPage(self.driver)
        assert mainPage.is_title_matches()
        mainPage.search_text_element = searchItem
        mainPage.close_welcome_message()
        search_result_page = page.SearchResultPage(self.driver)
        assert search_result_page.is_results_found()
        search_result_page.applying_filters(sortBy)
        foreverOrNot = input("Do you want to run forever or not? Y or N: ")
        if foreverOrNot == "N":
            search_result_page.find_most_recent()
            search_result_page.wait_for_change()
            search_result_page.grabs_url()
            search_result_page.discord_bot()
        else:
            search_result_page.find_most_recent()
            search_result_page.wait_for_change_forever()

        third_result_page = page.ThirdPageResults(self.driver)
        assert third_result_page.is_results_found()

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
