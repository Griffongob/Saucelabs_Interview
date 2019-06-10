from lib.cart import CartItem


class Checkout(object):
    def __init__(self, browser):
        self.checkout_info = CheckoutInfo(browser)
        self.checkout_summary = CheckoutSummary(browser)
        self.checkout_complete = CheckoutComplete(browser)


class CheckoutInfo(object):
    def __init__(self, browser):
        self.browser = browser

    def enter_first_name(self, text):
        field_elem = self.browser.select('#first-name')
        field_elem.clear()
        field_elem.send_keys(text)

    def enter_last_name(self, text):
        field_elem = self.browser.select('#last-name')
        field_elem.clear()
        field_elem.send_keys(text)

    def enter_zip(self, text):
        field_elem = self.browser.select('#postal-code')
        field_elem.clear()
        field_elem.send_keys(text)

    def click_cancel(self):
        button = self.browser.select('.cart_cancel_link')
        button.click()
        self.browser.wait_for_element_to_display('.cart_list')

    def click_continue(self, expect_error=False):
        button = self.browser.select('.cart_button')
        button.click()
        if not expect_error:
            self.browser.wait_for_element_to_display('.summary_info')
        else:
            self.browser.wait_for_element_to_display('[data-test="error"]')

    def get_error_message(self):
        error_field = self.browser.select('[data-test="error"]')
        return error_field.text


class CheckoutSummary(object):
    def __init__(self, browser):
        self.browser = browser

    def get_item_list(self):
        item_elems = self.browser.select('.cart_item', multiples=True)
        items = [CartItem(elem, self.browser) for elem in item_elems]
        return items

    def get_payment_info(self):
        return self.browser.select('.summary_value_label:nth-child(2)').text

    def get_shipping_info(self):
        return self.browser.select('.summary_value_label:nth-child(4)').text

    def get_subtotal(self):
        total_text = self.browser.select('.summary_subtotal_label').text
        final_text = total_text[total_text.index(':')+1:]
        return final_text

    def get_tax(self):
        total_text = self.browser.select('.summary_tax_label').text
        final_text = total_text[total_text.index(':') + 1:]
        return final_text

    def get_total(self):
        total_text = self.browser.select('.summary_total_label').text
        final_text = total_text[total_text.index(':') + 1:]
        return final_text

    def click_cancel(self):
        button = self.browser.select('.cart_cancel_link')
        button.click()
        self.browser.wait_for_element_to_display('.cart_list')

    def click_finish(self):
        button = self.browser.select('.cart_button')
        button.click()
        self.browser.wait_for_element_to_display('.checkout_complete_container')


class CheckoutComplete(object):
    def __init__(self, browser):
        self.browser = browser

    def get_success_text(self):
        return self.browser.select('.checkout_complete_container').text

    def is_pony_present(self):
        return self.browser.is_element_displayed('.pony_express')