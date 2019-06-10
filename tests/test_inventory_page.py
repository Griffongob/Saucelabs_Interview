import pytest
import requests

@pytest.mark.usefixtures("setup")
def test_number_products(setup):
    browser,inventory, product, cart = setup[0], setup[1], setup[2], setup[3]
    browser.go_to_url('http://www.saucedemo.com/inventory.html')
    inventory_items = inventory.get_inventory_items()
    assert len(inventory_items) == 6, "WARNING: Was expecting 6 but saw: {} instead".format(len(inventory_items))

@pytest.mark.usefixtures("setup")
def test_inventory_item_attributes(setup):
    browser,inventory, product, cart = setup[0], setup[1], setup[2], setup[3]
    browser.go_to_url('http://www.saucedemo.com/inventory.html')
    inventory_items = inventory.get_inventory_items()
    item = inventory_items[0]

    assert item.item_name == "Sauce Labs Backpack"
    assert item.item_price == "$29.99"
    assert item.item_description == "carry.allTheThings() with the sleek, streamlined Sly " \
                                    "Pack that melds uncompromising style with unequaled laptop and tablet protection."

    img_load_status_code = requests.get(item.item_image).status_code
    assert img_load_status_code == requests.codes.ok, "WARNING: Image link returned {}".format(img_load_status_code)

@pytest.mark.usefixtures("setup")
def test_add_to_cart_from_inventory(setup):
    browser,inventory, product, cart = setup[0], setup[1], setup[2], setup[3]
    browser.go_to_url('http://www.saucedemo.com/inventory.html')
    inventory_item = inventory.get_inventory_items()[0]
    inventory_item_name = inventory_item.item_name
    inventory_item.click_add_to_cart()

    assert inventory.header.get_cart_count() == '1'

    inventory.header.click_cart()

    assert cart.is_item_in_cart(inventory_item_name), "Item not seen in cart"



@pytest.mark.usefixtures("setup")
def test_add_multiples_items_to_cart_from_inventory(setup):
    browser,inventory, product, cart = setup[0], setup[1], setup[2], setup[3]
    browser.go_to_url('http://www.saucedemo.com/inventory.html')
    inventory_items = inventory.get_inventory_items()
    inventory_items[0].click_add_to_cart()
    inventory_items[1].click_add_to_cart()
    item_1_name = inventory_items[0].item_name
    item_2_name = inventory_items[1].item_name

    assert inventory.header.get_cart_count() == '2'

    inventory.header.click_cart()

    assert cart.is_item_in_cart(item_1_name), "Item not seen in cart"
    assert cart.is_item_in_cart(item_2_name), "Item not seen in cart"


@pytest.mark.usefixtures("setup")
def test_remove_from_cart_from_inventory(setup):
    browser,inventory, product, cart = setup[0], setup[1], setup[2], setup[3]
    browser.go_to_url('http://www.saucedemo.com/inventory.html')
    inventory_item = inventory.get_inventory_items()[0]

    inventory_item.click_add_to_cart()

    assert inventory.header.get_cart_count() == '1'

    inventory_item.click_remove()

    assert inventory.header.get_cart_count() == '0'