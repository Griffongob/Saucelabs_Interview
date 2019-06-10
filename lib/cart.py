from header import Header


class Cart(object):
    def __init__(self, browser):
        self.browser = browser
        self.header = Header(browser)


