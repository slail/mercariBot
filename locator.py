from selenium.webdriver.common.by import By

# Classes that represents object we want to find.


# Will have all locators for the stuff on our "main" page
class MainPageLocators(object):
    CLOSE_WELCOME_MESSAGE = (
        By.CSS_SELECTOR, 'button[aria-label="Close Message"]')
    SEARCH_BUTTON = (
        By.CSS_SELECTOR, 'button[data-testid="SearchIcon"]')


class SearchResultsPageLocators(object):
    SORT_OPTIONS = (By.ID, "Select sort by ")

    def __init__(self, sortBy=None):
        self.sortBy = sortBy
        self.SORT_OPTION = (By. ID, f"sortBy-{sortBy}")
