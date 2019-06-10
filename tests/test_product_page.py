import pytest
import requests

@pytest.mark.usefixtures("driver", "setup")
def test_product_page_info(setup):
    browser,inventory, product, cart = setup[0], setup[1], setup[2], setup[3]
    browser.go_to_url('http://www.saucedemo.com/inventory.html')
    inventory_item = inventory.get_inventory_items()[0]
    item_name = inventory_item.item_name
    item_desc = inventory_item.item_description
    item_price = inventory_item.item_price
    inventory_item.click_item_name()

    assert product.product_name() == item_name
    assert product.product_description() == item_desc
    assert product.product_price() == item_price


@pytest.mark.usefixtures("setup")
def test_add_to_cart_from_product_page(setup):
    browser,inventory, product, cart = setup[0], setup[1], setup[2], setup[3]
    browser.go_to_url('http://www.saucedemo.com/inventory.html')
    inventory_item = inventory.get_inventory_items()[0]
    inventory_item.click_item_image()
    item_name = product.product_name()

    product.click_add_to_cart()

    assert product.header.get_cart_count() == '1'

    product.header.click_cart()

    assert cart.is_item_in_cart(item_name), "Item not seen in cart"


@pytest.mark.usefixtures("setup")
def test_remove_from_cart_from_product_page(setup):
    browser,inventory, product, cart = setup[0], setup[1], setup[2], setup[3]
    browser.go_to_url('http://www.saucedemo.com/inventory.html')
    inventory_item = inventory.get_inventory_items()[0]
    inventory_item.click_item_image()
    product.click_add_to_cart()
    assert product.header.get_cart_count() == '1'
    product.click_remove()
    assert product.header.get_cart_count() == '0'