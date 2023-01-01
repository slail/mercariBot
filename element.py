from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


class BasePageElement(object):
    # Represents one element of the page at a time
    def __set__(self, obj, value):
        driver = obj.driver
        WebDriverWait(driver, 100).until(
            lambda driver: driver.find_element(By.CSS_SELECTOR, self.locator))
        # Changed from By.NAME, to By.CSS_Selector!
        driver.find_element(By.CSS_SELECTOR, self.locator).clear()
        driver.find_element(By.CSS_SELECTOR, self.locator).send_keys(value)

    def __get__(self, obj, owner):
        driver = obj.driver
        WebDriverWait(driver, 100).until(
            lambda driver: driver.find_element(By.CSS_SELECTOR, self.locator))
        element = driver.find_element(By.CSS_SELECTOR, self.locator)
        return element.get_attribute("href")
