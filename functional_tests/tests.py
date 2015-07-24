from django.test import LiveServerTestCase
from selenium import webdriver

MY_IP = "http://192.168.59.103"


class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Remote(MY_IP + ":4444/wd/hub", webdriver.DesiredCapabilities.FIREFOX)
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_site_loads(self):
        # Alfrescan wants to generate a license, visits the URL
        self.browser.get(MY_IP)

        # They notice the page title and header mention the license generator
        self.assertIn("License Generator", self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertEqual("License Generator", header_text)

    def test_home_page_contains_a_tabbed_form(self):
        # Alfrescan visits the main page
        self.browser.get(MY_IP)

        # There are two tabs above a form
        tabs_form = self.browser.find_elements_by_css_selector("[role='tab']")
        self.assertEqual(len(tabs_form), 2)

        # Alfrescan notices that one tab for Alfresco licenses
        self.assertIn("Alfresco License", tabs_form[0].text)

        # Alfrescan also notices that the other one is for Activiti licenses
        self.assertIn("Activiti License", tabs_form[1].text)

        # Beneath both previous tabs Alfrescan sees one form -either Alfresco or Activiti-
        main_form = self.browser.find_element_by_tag_name("form")
        self.assertTrue(main_form)

        # The form contains 4 main information panels:
        # Generate a new license, License types, License arguments, Generate
        actual_headers = self.browser.find_elements_by_css_selector('.panel h3 b')
        expected_headers = ['Generate a new license', 'License types', 'License arguments', 'Generate']
        for header in actual_headers[:4]:
            self.assertIn(header.text, expected_headers)

        # There are also 2 main buttons - Generate and download & Clear Form -
        self.fail('Finish the test!')

    def test_layout_and_styling(self):
        # Alfrescan goes to the home page
        self.browser.get(MY_IP)
        self.browser.set_window_size(1024, 768)

        # Alfrescan notices the header is centered
        header_element = self.browser.find_element_by_tag_name('h1')

        self.assertAlmostEqual(
            header_element.location['x'] + header_element.size['width'] / 2,
            512,
            delta=5
        )
