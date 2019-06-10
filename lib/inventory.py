from selenium.webdriver.support.select import Select
from header import Header


class Inventory(object):
    def __init__(self, browser):
        self.browser = browser
        self.header = Header(browser)

    def get_inventory_items(self):
        inv_item_elems = self.browser.select('.inventory_item', multiples=True)
        return [InventoryItem(elem, self.browser) for elem in inv_item_elems]

    def change_sort(self, requested_sort):
        elem = self.browser.select('.product_sort_container')
        sort_dropdown = Select(elem)
        sort_dropdown.select_by_visible_text(requested_sort)


class InventoryItem(object):

    def __init__(self, elem, browser):
        self.elem = elem
        self.browser = browser

    @property
    def item_name(self):
        return self.elem.find_element_by_css_selector('.inventory_item_name').text

    @property
    def item_description(self):
        return self.elem.find_element_by_css_selector('.inventory_item_desc').text

    @property
    def item_image(self):
        img_elem = self.elem.find_element_by_css_selector('.inventory_item_img')
        return img_elem.get_attribute('src')

    @property
    def item_price(self):
        return self.elem.find_element_by_css_selector('.inventory_item_price').text

    @property
    def button_text(self):
        return self.elem.find_element_by_css_selector('.btn_inventory').text

    def click_add_to_cart(self):
        add_button = self.elem.find_element_by_css_selector('.btn_inventory')
        add_button.click()
        self.browser.wait_for_element_to_not_display('.btn_primary')

    def click_remove(self):
        remove_button = self.elem.find_element_by_css_selector('.btn_inventory')
        remove_button.click()
        self.browser.wait_for_element_to_not_display('.btn_secondary')

    def click_item_name(self):
        self.elem.find_element_by_css_selector('.inventory_item_name').click()

    def click_item_image(self):
        self.elem.find_element_by_css_selector('.inventory_item_img').click()