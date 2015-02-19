from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):
	def setUp(self):
		self.browser = webdriver.Remote("http://docker.local.com:4444/wd/hub", webdriver.DesiredCapabilities.FIREFOX)
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()

	def test_site_loads(self):
		# Alfrescan wants to generate a license, visits the URL
		self.browser.get("http://docker.local.com")

		# They notice the page title and header mention the license generator
		self.assertIn("License Generator", self.browser.title)
		self.fail("Finish the test!")

if __name__ == '__main__':
	unittest.main(warnings='ignore')