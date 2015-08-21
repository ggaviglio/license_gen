from .base import FunctionalTest


class HomePageTest(FunctionalTest):

    def test_site_loads(self):
        # Alfrescan wants to generate a license, visits the URL
        # They notice the page title mention the license generator
        self.assertIn("License Generator", self.browser.title)

    def test_home_page_contains_tabbed_form(self):
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

    def test_home_page_has_tabs_to_switch_between_each_other(self):
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
        default_tab_selected = self.browser.find_element_by_css_selector('#myTab li.active a')
        self.browser.find_element_by_css_selector('#myTab li [href="#alfresco_tab"]').click()
        new_tab_selected = self.browser.find_element_by_css_selector('#myTab li.active a')

        self.assertEqual(default_tab_selected, new_tab_selected)

        self.browser.find_element_by_css_selector('#myTab li [href="#activiti_tab"]').click()
        last_tab_selected = self.browser.find_element_by_css_selector('#myTab li.active a')

        self.assertNotEqual(new_tab_selected, last_tab_selected)

    def test_home_page_has_tabs_to_change_visible_form_content(self):
        default_content = self.browser.find_element_by_css_selector('div.active .panel')

        # Alfrescan clicks on the Alfresco tab
        self.browser.find_element_by_css_selector('#myTab li [href="#alfresco_tab"]').click()
        new_content = self.browser.find_element_by_css_selector('div.active .panel')
        self.assertEqual(default_content, new_content)

        # Alfrescan clicks on the Activiti tab
        self.browser.find_element_by_css_selector('#myTab li [href="#activiti_tab"]').click()
        last_content = self.browser.find_element_by_css_selector('div.active.in .panel')
        self.assertNotEqual(new_content, last_content)

    def test_user_can_clear_info_from_alfresco_form(self):
        # Alfrescan notices how all the input form elements are empty -Alfresco form-
        self.browser.find_element_by_css_selector('#myTab li [href="#alfresco_tab"]').click()
        form_elements_alfresco = {}

        # Alfrescan check all form elements available to be filled
        form_elements_alfresco = self.get_form_elements("alfresco")
        # Alfrescan sees how every form element is empty
        self.check_form_elements_empty("alfresco", form_elements_alfresco)
        # Alfrescan procedes to fill in each form elements in the tab selected
        self.fill_in_form_elements("alfresco", form_elements_alfresco)
        # Alfrescan sees how every form element hold some information
        self.check_form_elements_filled("alfresco", form_elements_alfresco)
        # Alfrescan goes to the Clear form button and click over this
        self.browser.find_element_by_css_selector("#alfresco_form #clear_form").click()

        # Alfrescan check all form elements available to be filled
        form_elements_alfresco = self.get_form_elements("alfresco")
        # Alfrescan sees how every form element is empty
        self.check_form_elements_empty("alfresco", form_elements_alfresco)

    def test_user_can_clear_info_from_activiti_form(self):
        # Alfrescan notices how all the input form elements are empty -Alfresco form-
        self.browser.find_element_by_css_selector('#myTab li [href="#activiti_tab"]').click()
        form_elements_activiti = {}

        # Alfrescan check all form elements available to be filled
        form_elements_activiti = self.get_form_elements("activiti")
        # Alfrescan sees how every form element is empty
        self.check_form_elements_empty("activiti", form_elements_activiti)
        # Alfrescan procedes to fill in each form elements in the tab selected
        self.fill_in_form_elements("activiti", form_elements_activiti)
        # Alfrescan sees how every form element hold some information
        self.check_form_elements_filled("activiti", form_elements_activiti)
        # Alfrescan goes to the Clear form button and click over this
        self.browser.find_element_by_css_selector("#activiti_form #clear_form").click()

        # Alfrescan check all form elements available to be filled
        form_elements_activiti = self.get_form_elements("activiti")
        # Alfrescan sees how every form element is empty
        self.check_form_elements_empty("activiti", form_elements_activiti)

    def test_user_can_clear_empty_alfresco_form(self):
        # Alfrescan goes to the alfresco tab
        self.browser.find_element_by_css_selector('#myTab li [href="#alfresco_tab"]').click()
        form_elements_alfresco = {}

        # Alfrescan checks all form elements available to be filled
        form_elements_alfresco = self.get_form_elements("alfresco")
        # Alfrescan sees how every form element is empty
        self.check_form_elements_empty("alfresco", form_elements_alfresco)

        # Knowing that all form elements are empty, Alfrescan goes straight
        # to click the Clear form button
        self.browser.find_element_by_css_selector("#alfresco_form #clear_form").click()

        #Alfrescan sees how the form is still empty after click the clear form button
        self.check_form_elements_empty("alfresco", form_elements_alfresco)

    def test_user_can_clear_empty_activiti_form(self):
        # Alfrescan clicks on the activiti tab
        self.browser.find_element_by_css_selector('#myTab li [href="#activiti_tab"]').click()
        form_elements_activiti = {}

        # Alfrescan checks all form elements available to be filled
        form_elements_activiti = self.get_form_elements("activiti")
        # Alfrescan sees how every form element is empty
        self.check_form_elements_empty("activiti", form_elements_activiti)

        # Knowing that all form elements are empty, Alfrescan goes straight
        # to click the Clear form button
        self.browser.find_element_by_css_selector("#activiti_form #clear_form").click()

        #Alfrescan sees how the form is still empty after click the clear form button
        self.check_form_elements_empty("activiti", form_elements_activiti)
