from django.test import LiveServerTestCase
from selenium import webdriver

MY_IP = "http://192.168.59.103"


class FunctionalTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Remote(MY_IP + ":4444/wd/hub", webdriver.DesiredCapabilities.FIREFOX)
        self.browser.implicitly_wait(3)
        # Alfrescan wants to generate a license, visits the URL
        self.browser.get(MY_IP)

    def tearDown(self):
        self.browser.quit()
