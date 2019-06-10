import pytest
from os import environ
from lib.inventory import Inventory
from lib.cart import Cart
from lib.browser import Browser
from lib.product import Product
from lib.checkout import Checkout
from lib.login_page import LoginPage
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.remote_connection import RemoteConnection

import urllib3
urllib3.disable_warnings()


def pytest_addoption(parser):
    parser.addini('platform', help='OS that saucelabs will run test on')
    parser.addini('browser', help='Browser that saucelabs will run on')
    parser.addini('browserVersion', help='Browser version number that saucelabs will run tests on')
    parser.addini('seleniumVersion', help='Selenium version that saucelabs will run tests with')
    parser.addini('window_size', help='What size the browser window should be.')
    parser.addoption('--platform', action='store', dest='platform')
    parser.addoption('--browser', action='store', dest='browser')
    parser.addoption('--browserVersion', action='store', dest='browserVersion')


@pytest.fixture(scope='function')
def browser_config(request):
    browser = {
        'platform': request.config.getoption('platform') if request.config.getoption('platform') else request.config.getini('platform'),
        'browserName': request.config.getoption('browser') if request.config.getoption('browser') else request.config.getini('browser'),
        'browserVersion': request.config.getoption('browserVersion') if request.config.getoption('browserVersion') else request.config.getini('browserVersion'),
        'screenResolution': request.config.getini('window_size'),
        'seleniumVersion': request.config.getini('seleniumVersion')
    }
    return browser


@pytest.yield_fixture(scope='function')
def driver(request, browser_config):
    # if the assignment below does not make sense to you please read up on object assignments.
    # The point is to make a copy and not mess with the original test spec.
    desired_caps = dict()
    desired_caps.update(browser_config)
    test_name = request.node.name
    build_tag = environ.get('BUILD_TAG', None)
    tunnel_id = environ.get('TUNNEL_IDENTIFIER', None)
    username = environ.get('SAUCE_USERNAME', None)
    access_key = environ.get('SAUCE_ACCESS_KEY', None)

    selenium_endpoint = "https://%s:%s@ondemand.saucelabs.com:443/wd/hub" % (username, access_key)
    desired_caps['build'] = build_tag
    # we can move this to the config load or not, also messing with this on a test to test basis is possible :)
    desired_caps['tunnelIdentifier'] = tunnel_id
    desired_caps['name'] = test_name

    executor = RemoteConnection(selenium_endpoint, resolve_ip=False)
    browser = webdriver.Remote(
        command_executor=executor,
        desired_capabilities=desired_caps, 
        keep_alive=True
    )

    # This is specifically for SauceLabs plugin.
    # In case test fails after selenium session creation having this here will help track it down.
    # creates one file per test non ideal but xdist is awful
    if browser is not None:
        with open("%s.testlog" % browser.session_id, 'w') as f:
            f.write("SauceOnDemandSessionID=%s job-name=%s\n" % (browser.session_id, test_name))
    else:
        raise WebDriverException("Never created!")

    yield browser
    # Teardown starts here
    # report results
    # use the test result to send the pass/fail status to Sauce Labs
    sauce_result = "failed" if request.node.rep_call.failed else "passed"
    browser.execute_script("sauce:job-result={}".format(sauce_result))
    browser.quit()


@pytest.fixture(scope='function')
def setup(request, driver):
    browser = Browser(driver)
    inventory = Inventory(browser)
    cart = Cart(browser)
    product = Product(browser)
    checkout = Checkout(browser)
    login = LoginPage(browser)
    return browser, inventory, product, cart, checkout, login


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    # this sets the result as a test attribute for Sauce Labs reporting.
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # set an report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"
    setattr(item, "rep_" + rep.when, rep)

