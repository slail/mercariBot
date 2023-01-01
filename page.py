from locator import *
from element import BasePageElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from discord_webhook import DiscordWebhook
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

            print("Just closed welcome\n")
            self.click_go_button()
        except:
            self.click_go_button()

    def click_go_button(self):
        searchAction = ActionChains(self.driver)
        element = self.driver.find_element(
            *MainPageLocators.SEARCH_BUTTON)
        searchAction.move_to_element(element).click()
        searchAction.perform()
        print("Item searched\n")


class SearchResultPage(BasePage):
    itemInfo = None
    itemElement = None
    resultUrl = None

    def is_results_found(self):
        return "No result found." not in self.driver.page_source

    def applying_filters(self, sortBy):
        print("...applying filters...\n")
        filters = ActionChains(self.driver)
        sortOptions = WebDriverWait(self.driver, 30).until(
            lambda x: x.find_element(*SearchResultsPageLocators.SORT_OPTIONS))
        filters.move_to_element(sortOptions).click()
        filters.perform()

        filtersSecond = ActionChains(self.driver)
        sortObject = SearchResultsPageLocators(sortBy)
        specificOption = WebDriverWait(self.driver, 30).until(
            lambda x: x.find_element(*sortObject.SORT_OPTION))
        filtersSecond.move_to_element(specificOption).click()
        filtersSecond.perform()
        print("...filters applied...\n")

    def find_most_recent(self):
        time.sleep(5)
        waitChain = ActionChains(self.driver)
        mostRecentListing = WebDriverWait(self.driver, 30).until(
            lambda x: x.find_element(*SearchResultsPageLocators.MOST_RECENT_ITEM))

        self.itemInfo = mostRecentListing.text
        self.itemElement = mostRecentListing

        waitChain.perform()

    def wait_for_change(self):
        seconds = 60
        print("...waiting for deal...\n")
        print(
            f"We're starting off: \n ** {self.itemInfo}** \n\nNow waiting {seconds} seconds")
        previousRecentItem = self.itemInfo
        i = 0
        while previousRecentItem == self.itemInfo:
            # Change time to refresh after how much minutes!
            time.sleep(seconds)
            i += 1
            print(f"We waited 60 seconds: {i} times\n")
            self.driver.refresh()
            self.find_most_recent()

        minutes = (60 * i) // 60
        print(f"Our item has changed! After waiting {minutes} minutes\n")
        print(f'{self.itemInfo}\n')

    def grabs_url(self):
        grabAction = ActionChains(self.driver)
        grabAction.move_to_element(self.itemElement).click()

        grabAction.perform()

        grabActionSecond = ActionChains(self.driver)
        shareButton = WebDriverWait(self.driver, 30).until(
            lambda x: x.find_element(*SearchResultsPageLocators.SHARE_BUTTON))  # Just a Random Element on landing page to get the right URL!

        get_url = self.driver.current_url
        self.resultUrl = get_url

        grabActionSecond.perform()

        print(type(get_url))

    def discord_bot(self):
        webhook = DiscordWebhook(
            url="https://discord.com/api/webhooks/1059131886573731860/Sgi8Yhxdnbn-soPv2AtiuHBF1hNa3dkM92wGPPtUxJEKd9B6ctKH2xJD53R3vtBmjq1f")

        # webhook.set_content(
        #     "Hey guys, Studiex posted a new video on YouTube! Go check it out : sunglasses: @everyone")

        webhook.set_content(self.resultUrl)
        response = webhook.execute()


class ThirdPageResults(BasePage):
    def is_results_found(self):
        return "No result found." not in self.driver.page_source
