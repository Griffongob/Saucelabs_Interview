import pytest


@pytest.mark.usefixtures("setup")
def test_invalid_crentials_error(setup):
    browser, login = setup[0], setup[5]
    browser.go_to_url('http://www.saucedemo.com')
    login.enter_username('locked_out_user')
    login.enter_password('secret_sauce')
    login.click_submit(expect_error=True)
    assert login.is_error_displayed()
