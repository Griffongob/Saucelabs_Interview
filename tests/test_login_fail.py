import pytest


@pytest.mark.usefixtures("driver", "setup")
def test_valid_crentials_login(driver, setup):
    browser, inventory, cart = setup
    # driver.get('http://www.saucedemo.com')
    browser.go_to_url('http://www.saucedemo.com')

    driver.find_element_by_id('user-name').send_keys('locked_out_user')
    driver.find_element_by_id('password').send_keys('secret_sauce')
    driver.find_element_by_css_selector('.btn_action').click()

    assert driver.find_element_by_css_selector('.error-button').is_displayed()
