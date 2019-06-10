from header import Header


class Cart(object):
    def __init__(self, browser):
        self.browser = browser
        self.header = Header(browser)

    def get_cart_items(self):
        cart_item_elems = self.browser.select('.cart_item', multiples=True)
        cart_items = [CartItem(elem, self.browser) for elem in cart_item_elems]
        return cart_items


class CartItem(object):
    def __init__(self, elem, browser):
        self.elem = elem
        self.browser = browser

    @property
    def quantity(self):
        return self.elem.find_element_by_css_selector('.cart_quantity').text

    @property
    def item_name(self):
        return self.elem.find_element_by_css_selector('.inventory_item_name').text

    @property
    def item_description(self):
        return self.elem.find_element_by_css_selector('.inventory_item_desc').text

    @property
    def item_price(self):
        return self.elem.find_element_by_css_selector('.inventory_item_price').text

    def click_remove_item(self):
        button = self.elem.find_element_by_css_selector('.cart_button')
        button.click()

    def click_item_name(self):
        self.elem.find_element_by_css_selector('.inventory_item_name').click()
        self.browser.wait_for_element_to_display('.inventory_details_name')

    def click_continue_shopping(self):
        button = self.elem.find_element_by_css_selector('.cart_footer > .btn_secondary')
        button.click()
        self.browser.wait_for_element_to_display('.inventory_item_name')

    def click_checkout(self):
        button = self.elem.find_element_by_css_selector('.checkout_button')
        button.click()
        self.browser.wait_for_element_to_display('.checkout_info_container')