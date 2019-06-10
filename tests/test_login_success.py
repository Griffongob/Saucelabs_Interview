import pytest


@pytest.mark.usefixtures("setup")
def test_valid_crentials_login(setup):
    browser, login = setup[0], setup[5]
    browser.go_to_url('http://www.saucedemo.com')
    login.enter_username('standard_user')
    login.enter_password('secret_sauce')
    login.click_submit()
    assert "/inventory.html" in browser.current_url()
