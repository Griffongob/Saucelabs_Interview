class LoginPage(object):
    def __init__(self, browser):
        self.browser = browser

    def enter_username(self, requested_username):
        username_field = self.browser.select('#user-name')
        username_field.clear()
        username_field.send_keys(requested_username)

    def enter_password(self, requested_password):
        username_field = self.browser.select('#password')
        username_field.clear()
        username_field.send_keys(requested_password)

    def click_submit(self, expect_error=False):
        button = self.browser.select('.btn_action')
        button.click()
        if not expect_error:
            self.browser.wait_for_element_to_display('.inventory_item_price')

    def is_error_displayed(self):
        return self.browser.is_element_displayed('.error-button')