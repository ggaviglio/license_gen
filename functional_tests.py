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

	def test_filename_updates(self):
		# Alfrescan adds a holder name, filename should include it
		self.browser.get("http://docker.local.com")
		input_holder_name = self.browser.find_element_by_id('holder_name')
		self.assertEqual(
			input_holder_name.get_attribute('placeholder'),
			'Enter an account holder name'
		)

		#They add 'Alfresco' to the holder name box
		input_holder_name.send_keys('Alfresco')

		#The filename inputbox automatically updates to include the account holder name
		input_filename = self.browser.find_element_by_id('filename')
		self.assertEqual(
			input_filename.get_attribute('value'),
			'Alfresco.lic'
		)

		self.fail('Finish the test!')

if __name__ == '__main__':
	unittest.main(warnings='ignore')