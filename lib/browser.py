from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotVisibleException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Browser(object):

    def __init__(self, driver):
        self.driver = driver

    def go_to_url(self, url):
        self.driver.get(url)

    def current_url(self):
        return self.driver.current_url

    def refresh(self):
        self.driver.refresh()

    def back(self):
        self.driver.back()

    def select(self, selector, multiples=False, wait_for_elem_to_be_visible=True, timeout=5, wait_for_elem_to_be_present=False):
        try:
            if wait_for_elem_to_be_present:
                self.wait_for_element_to_be_present(selector, timeout=timeout)
            if wait_for_elem_to_be_visible:
                self.wait_for_element_to_display(selector, timeout=timeout)
            if multiples:
                element = self.driver.find_elements_by_css_selector(selector)
            else:
                element = self.driver.find_element_by_css_selector(selector)
        except TimeoutException:
            raise NoSuchElementException
        return element

    def wait_for_element_to_display(self, selector, timeout=5, step=0.05):
        try:
            WebDriverWait(self.driver, timeout, step).until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
        except TimeoutException:
            raise NoSuchElementException(selector)

    def wait_for_element_to_be_present(self, selector, timeout=5, step=0.05):
        try:
            WebDriverWait(self.driver, timeout, step).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector)))
        except TimeoutException:
            raise NoSuchElementException(selector)

    def wait_for_element_to_be_clickable(self, selector, timeout=5, step=0.05):
        try:
            WebDriverWait(self.driver, timeout, step).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
        except TimeoutException:
            raise NoSuchElementException(selector)

    def wait_for_element_to_not_display(self, selector, timeout=5, step=0.05):
        try:
            WebDriverWait(self.driver, timeout, step).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, selector)))
        except TimeoutException:
            raise NoSuchElementException

    def is_element_displayed(self, selector, timeout=1):
        try:
            WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            return True
        except TimeoutException:
            return False