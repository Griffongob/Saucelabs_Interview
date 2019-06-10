class Header(object):
    def __init__(self, browser):
        self.browser = browser

    def get_cart_count(self):
        return self.browser.select('.shopping_cart_badge').text

    def is_logo_present(self):
        return self.browser.is_element_displayed('.app_logo')

    def click_cart(self):
        self.browser.select('#shopping_cart_container').click()