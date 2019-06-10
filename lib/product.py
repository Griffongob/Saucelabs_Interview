from lib.header import Header


class Product(object):
    def __init__(self, browser):
        self.browser = browser
        self.header = Header(browser)

    def product_image_url(self):
        img_elem = self.browser.select('img.inventory_details_img')
        img_url = img_elem.get_attribute('src')
        return img_url

    def product_name(self):
        return self.browser.select('.inventory_details_name').text

    def product_description(self):
        return self.browser.select('.inventory_details_desc').text

    def product_price(self):
        return self.browser.select('.inventory_details_price').text

    def click_back_button(self):
        self.browser.select('.inventory_details_back_button').click()
        self.browser.wait_for_element_to_not_display('.inventory_details_name')

    def click_add_to_cart(self):
        button = self.browser.select('.btn_inventory')
        button.click()
        self.browser.wait_for_element_to_display('.btn_secondary')

    def click_remove(self):
        button = self.browser.select('.btn_inventory')
        button.click()
        self.browser.wait_for_element_to_display('.btn_primary')