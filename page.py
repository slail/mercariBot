from locator import *
from element import BasePageElement
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk.errors import SlackApiError
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from discord_webhook import DiscordWebhook
from selenium.webdriver.support import expected_conditions as EC
import time


class SearchTextElement(BasePageElement):
    locator = 'input[type="search"]'


class getTextElement(BasePageElement):
    locator = 'a[class="Text__LinkText-sc-441b8d37-0-a Link__StyledAnchor-sc-c96f6437-0 Link__StyledPlainLink-sc-c96f6437-3 eSSYiT eqUXag"]'


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

            print("\nJust closed welcome\n")
            self.click_go_button()
        except:
            self.click_go_button()

    def click_go_button(self):
        searchAction = ActionChains(self.driver)
        element = self.driver.find_element(
            *MainPageLocators.SEARCH_BUTTON)
        searchAction.move_to_element(element).click()
        searchAction.perform()
        print("\n...item searched...\n")


class SearchResultPage(BasePage):
    itemInfo = None
    itemElement = None
    resultUrl = None
    get_text_element = getTextElement()

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

    def wait_for_change(self, second):
        time.sleep(5)
        seconds = second
        print("...waiting for deal...\n")
        print(
            f"We're starting off with: \n ** {self.itemInfo} ** \n\nNow waiting {seconds} seconds")
        previousRecentItem = self.itemInfo
        i = 0
        while previousRecentItem == self.itemInfo:
            # Change time to refresh after how much minutes!
            time.sleep(seconds)
            i += 1
            if i > 1:
                prefix = "s"
            else:
                prefix = ""
            print(f"We waited {seconds} seconds: {i} time{prefix}\n")
            self.driver.refresh()
            self.find_most_recent()

        minutes = (60 * i) // 60
        if minutes > 1:
            prefix = "s"
        else:
            prefix = ""
        print(
            f"Our item has changed! After waiting {minutes} minute{prefix}\n")
        print(f'{self.itemInfo}\n')

    def grabs_url(self):
        time.sleep(1)
        grabAction = ActionChains(self.driver)
        mostRecentItem = WebDriverWait(self.driver, 30).until(
            lambda x: x.find_element(*SearchResultsPageLocators.MOST_RECENT_ITEM))
        href_link = mostRecentItem.get_attribute("href")
        self.resultUrl = href_link
        print(self.resultUrl)

    def discord_bot(self):
        webhook = DiscordWebhook(
            url="")  # !IMPORTANT: BETWEEN EMPTY QUOTES, ADD YOUR DISCORD WEBHOOK! ##
        webhook.set_content(self.resultUrl)
        webhook.execute()

    def slack_bot(self, url):
        app = App(token="")
        channel_id = ""
        try:
            response = app.client.chat_postMessage(channel=channel_id, text=url)
        except SlackApiError as e:
            raise RuntimeError(f"Error Processing submissions: {e}")

    def wait_for_change_forever(self, seconds):
        previous_items = []

        print("\nStarting the process...\n")
        mostRecentListings = WebDriverWait(self.driver, 30).until(
            lambda x: x.find_elements(*SearchResultsPageLocators.MOST_RECENT_ITEM)
        )

        # Extract URLs and add to previous_items
        # item_url = item.get_attribute("href"

        self.itemInfo = mostRecentListings[0].get_attribute("href")
        self.itemElement = mostRecentListings[0]
        # previous_items.append(self.itemInfo)
        print(f"First item found: {self.itemInfo}\n")

        # Will break if say the lister deletes listing as I'm refreshing and searching for the self.itemInfo
        while True:
            print(f"Waiting allotted time...\n")
            time.sleep(seconds)
            print("Refreshing the page...\n")
            self.driver.refresh()
            mostRecentListings = WebDriverWait(self.driver, 30).until(
                lambda x: x.find_elements(*SearchResultsPageLocators.MOST_RECENT_ITEM)
            )
            RecentListings = [item.get_attribute("href") for item in mostRecentListings]
            self.itemInfo_new = RecentListings[0]

            # Identify new items by comparing with the previous list
            if self.itemInfo != self.itemInfo_new:
                new_items = []
                index_of_og = RecentListings.index(self.itemInfo)
                for item in RecentListings[:index_of_og][::-1]:
                    # print(f"Added {item} to new items list.")
                    new_items.append(item)

                print(f"New item(s) detected: {new_items}\n")
                # Notify in chronological order of appearance
                for item in new_items:
                    # Assuming the item is a WebElement or you can locate it by an identifier
                    # item_url = item.get_attribute("href")  # Get the URL from the href attribute
                    self.slack_bot(item)  # Send the URL to Slack
                self.itemInfo = new_items[-1]
                new_items.clear()

            print("Waiting for the next change...\n")

class ThirdPageResults(BasePage):
    def is_results_found(self):
        return "No result found." not in self.driver.page_source
