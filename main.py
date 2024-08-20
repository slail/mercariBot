import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import page
import time


class PythonOrgSearchTTest(unittest.TestCase):

    def setUp(self):
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument(f'user-agent={user_agent}')
        options.add_argument("--window-size=1920,1080")
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--allow-running-insecure-content')
        options.add_argument("--disable-extensions")
        options.add_argument("--proxy-server='direct://'")
        options.add_argument("--proxy-bypass-list=*")
        options.add_argument("--start-maximized")
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-browser-side-navigation')
        options.add_argument('enable-features=NetworkServiceInProcess')
        self.driver = webdriver.Chrome(options=options)
        self.driver.get("https://www.mercari.com/")

    def test_search_python(self):
        searchItem = input("\nWhat item are you looking to buy: ")
        sortBy = input(
            "\nHow would you like to sort your item by?\n(1) best match \n(2) newest first \n(3) lowest price first \n(4) highest price first \nEnter Number: ")
        secondsWait = float(
            input("\nHow much minutes would you like to wait in between refresh: "))
        secondsWait = secondsWait * 60

        mainPage = page.MainPage(self.driver)
        assert mainPage.is_title_matches()
        mainPage.search_text_element = searchItem
        mainPage.close_welcome_message()
        search_result_page = page.SearchResultPage(self.driver)
        assert search_result_page.is_results_found()
        search_result_page.applying_filters(sortBy)
        foreverOrNot = input("Do you want to run forever or not? Y or N: ")
        if foreverOrNot.lower() == "n":
            search_result_page.find_most_recent()
            search_result_page.wait_for_change(secondsWait)
            # search_result_page.grabs_url()
            search_result_page.slack_bot()
        else:
            search_result_page.find_most_recent()
            search_result_page.wait_for_change_forever(secondsWait)

        third_result_page = page.ThirdPageResults(self.driver)
        assert third_result_page.is_results_found()

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
