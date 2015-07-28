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

    def test_home_page_contains_tabbed_form(self):
        # Alfrescan visits the main page
        self.browser.get(MY_IP)

        # There are two tabs above a form
        tabs_form = self.browser.find_elements_by_css_selector("[role='tab']")
        self.assertEqual(len(tabs_form), 2)

        # Alfrescan notices that one tab is for Alfresco licenses
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

    def test_home_page_has_tabs_to_change_visible_license_form(self):
        # Alfrescan visits the main page
        self.browser.get(MY_IP)

        # Alfrescan sees tabs for the different data licenses
        license_tabs = self.browser.find_elements_by_css_selector('#myTab li a')
        self.assertEqual(len(license_tabs), 2)

        # Alfrescan can see the title of both tabs as follows:
        expected_tabs = ['Alfresco License Generator', 'Activiti License Generator']
        first_tab = self.browser.find_elements_by_css_selector('#myTab li a')[0]
        second_tab = self.browser.find_elements_by_css_selector('#myTab li a')[1]

        self.assertEqual(first_tab.text, expected_tabs[0])
        self.assertEqual(second_tab.text, expected_tabs[1])

        # Clicking the tabs changes the active tab from one to another
        default_tab_selected = self.browser.find_element_by_css_selector('#myTab li.active a').text
        self.browser.find_elements_by_css_selector('#myTab li a')[0].click()
        new_tab_selected = self.browser.find_element_by_css_selector('#myTab li.active a').text

        self.assertEqual(default_tab_selected, new_tab_selected)

        self.browser.find_elements_by_css_selector('#myTab li a')[1].click()
        last_tab_selected = self.browser.find_element_by_css_selector('#myTab li.active a').text

        self.assertNotEqual(new_tab_selected, last_tab_selected)


        # Clicking the tabs changes the form sticky title
        initial_topbar_title = self.browser.find_element_by_css_selector('.navbar-brand').text    
        self.browser.find_elements_by_css_selector('#myTab li a')[0].click()
        new_topbar_title = self.browser.find_element_by_css_selector('.navbar-brand').text

        self.assertNotEqual(initial_topbar_title, new_topbar_title)

        self.browser.find_elements_by_css_selector('#myTab li a')[1].click()
        last_topbar_title = self.browser.find_element_by_css_selector('.navbar-brand').text

        self.assertNotEqual(new_topbar_title, last_topbar_title)        

        # Clicking the tabs changes the visible data
        original_content = self.browser.find_elements_by_css_selector('.panel')
        self.browser.find_elements_by_css_selector('#myTab li a')[0].click()
        new_content = self.browser.find_elements_by_css_selector('.panel')
        self.assertEqual(original_content, new_content)
        final_content = self.browser.find_elements_by_css_selector('#myTab li a')[1].click()
        self.assertNotEqual(new_content, final_content)

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
            delta=10
        )
