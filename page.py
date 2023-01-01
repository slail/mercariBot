from locator import *
from element import BasePageElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import time


class SearchTextElement(BasePageElement):
    locator = 'input[type="search"]'


class BasePage(object):
    def __init__(self, driver):
        self.driver = driver


class MainPage(BasePage):

    search_text_element = SearchTextElement()

    def is_title_matches(self):
        return "Mercari" in self.driver.title

    def close_welcome_message(self):
        try:
            close = WebDriverWait(self.driver, 10).until(
                lambda x: x.find_element(*MainPageLocators.CLOSE_WELCOME_MESSAGE))
            closeAction = ActionChains(self.driver)
            closeAction.move_to_element(close).click()
            closeAction.perform()

            print("Just closed welcome")
            self.click_go_button()
        except:
            self.click_go_button()

    def click_go_button(self):
        time.sleep(2)
        searchAction = ActionChains(self.driver)
        element = self.driver.find_element(
            *MainPageLocators.SEARCH_BUTTON)
        searchAction.move_to_element(element).click()
        searchAction.perform()
        print("just searched")


class SearchResultPage(BasePage):

    def is_results_found(self):
        return "No result found." not in self.driver.page_source
