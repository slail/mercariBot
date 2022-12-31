from selenium.webdriver.common.by import By

# Classes that represents object we want to find.


# Will have all locators for the stuff on our "main" page
class MainPageLocators(object):
    GO_BUTTON = (By.ID, "submit")  # (How we acess, what the value is)


class SearchResultsPageLocators(object):
    pass
