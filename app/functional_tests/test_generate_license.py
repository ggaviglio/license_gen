from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys


class GenerateLicenseTest(FunctionalTest):

    def user_checks_license_has_been_downloaded(self):
        pass

    def test_user_can_generate_alfresco_license(self):
        form_elements_alfresco = {}
        # Alfrescan clicks the alfresco tab
        self.browser.find_element_by_css_selector(
            '#tabSwitcher li [href="#alfresco_tab"]'
        ).click()
        # Alfrescan checks all form elements to be filled out
        form_elements_alfresco = self.get_form_elements("alfresco")
        # Alfrescan sees how all form elements are initially empty
        self.check_form_elements_empty("alfresco", form_elements_alfresco)
        # Alfrescan fills out all form elements with some information
        self.fill_in_form_elements("alfresco", form_elements_alfresco)
        # Alfrescan checks out that all fields have been filled out
        self.check_form_elements_filled("alfresco", form_elements_alfresco)
        # Alfrescan clicks the generate button to get the Alfresco license
        self.browser.find_element_by_css_selector(
            "#alfresco_form #generate_form_btn"
        ).click()
        # Here it is supposed to be testing that there is a file which has
        # been generated/downloaded to control the native window with some
        # window automation software like AutoIt.
        # http://stackoverflow.com/questions/23939702/
        # in-python-how-to-verify-if-file-has-been-downloaded
        # -correctly-before-opening-it
        self.user_checks_license_has_been_downloaded

    def test_user_can_generate_activiti_license(self):
        form_elements_activiti = {}
        # Alfrescan clicks the activiti tab
        self.browser.find_element_by_css_selector(
            '#tabSwitcher li [href="#activiti_tab"]'
        ).click()
        # Alfrescan checks all form elements to be filled out
        form_elements_activiti = self.get_form_elements("activiti")
        # Alfrescan sees how all form elements are initially empty
        self.check_form_elements_empty("activiti", form_elements_activiti)
        # Alfrescan fills out all form elements with some information
        self.fill_in_form_elements("activiti", form_elements_activiti)
        # Alfrescan checks out that all fields have been filled out
        self.check_form_elements_filled("activiti", form_elements_activiti)
        # Alfrescan clicks the generate button to get the activiti license
        self.browser.find_element_by_css_selector(
            "#activiti_form #generate_form_btn"
        ).click()
        # Here it is supposed to be testing that there is a file
        # which has been generated/downloaded to control the native
        # window with some window automation software like AutoIt.
        self.user_checks_license_has_been_downloaded

    def test_user_get_error_message_activiti_license(self):
        form_elements_activiti = {}
        # Alfrescan clicks on the activiti tab
        self.browser.find_element_by_css_selector(
            '#tabSwitcher li [href="#activiti_tab"]'
        ).click()
        # Alfrescan checks all form elements
        form_elements_activiti = self.get_form_elements("activiti")
        # Alfrescan sees how all form elements are initially empty
        self.check_form_elements_empty("activiti", form_elements_activiti)
        # Alfrescan clicks the generate button to get the Activiti license
        self.browser.find_element_by_css_selector(
            "#activiti_form #generate_form_btn"
        ).click()
        # Alfrescan will get an error message
        error_message = self.browser.find_element_by_css_selector(".alert p")\
            .text
        expected_error = \
            'Server error when processing Activiti license request:'
        self.assertEqual(error_message, expected_error)

        # Alfrescan switch to the Alfresco tab
        default_tab_selected = self.browser.\
            find_element_by_css_selector('#tabSwitcher li.active a')
        self.browser.find_element_by_css_selector(
            '#tabSwitcher li [href="#alfresco_tab"]'
        ).click()

        new_tab_selected = self.browser.\
            find_element_by_css_selector('#tabSwitcher li.active a')

        self.assertNotEqual(default_tab_selected, new_tab_selected)

        # Alfrescan will still get the same error message
        error_message = self.browser.find_element_by_css_selector(".alert p")\
            .text
        self.assertEqual(error_message, expected_error)


class GenerateFilenameTest(FunctionalTest):

    def test_default_generate_alfresco_filename(self):
        # Alfrescan goes to the alfresco tab
        self.browser.find_element_by_css_selector(
            '#tabSwitcher li [href="#alfresco_tab"]'
        ).click()

        value = self.browser.\
            find_element_by_css_selector(
                "#alfresco_form #output_filename"
            ).get_attribute('value')

        self.assertEqual("Alfresco-ent50-.lic", value)

    def test_default_generate_activiti_filename(self):
        # Alfrescan goes to the activiti tab
        self.browser.find_element_by_css_selector(
            '#tabSwitcher li [href="#activiti_tab"]'
        ).click()

        value = self.browser.\
            find_element_by_css_selector(
                "#activiti_form #output_filename"
            ).get_attribute('value')

        self.assertEqual("Activiti-1.0ent-.lic", value)

    def test_generate_alfresco_filename(self):
        # Alfrescan goes to the alfresco tab
        self.browser.find_element_by_css_selector(
            '#tabSwitcher li [href="#alfresco_tab"]'
        ).click()

        # Alfrescan decides to type his name
        self.browser.\
            find_element_by_css_selector(
                "#alfresco_form #field_holder_name"
            ).send_keys("Sebastian")

        # Alfrescan decides to tick one box
        self.browser.find_element_by_css_selector(
            "#alfresco_form #tag_internal_use_only"
        ).send_keys(Keys.SPACE)

        value = self.browser.\
            find_element_by_css_selector(
                "#alfresco_form #output_filename"
            ).get_attribute('value')

        self.assertEqual(
            "Alfresco-ent50-Sebastian-internal-use-only.lic",
            value
        )

    def test_generate_activiti_filename(self):
        # Alfrescan goes to the activiti tab
        self.browser.find_element_by_css_selector(
            '#tabSwitcher li [href="#activiti_tab"]'
        ).click()

        # Alfrescan decides to type his name
        self.browser.\
            find_element_by_css_selector(
                "#activiti_form #field_holder_name"
            ).send_keys("Dan")

        # Alfrescan decides to tick one box
        self.browser.find_element_by_css_selector(
            "#activiti_form #tag_extension"
        ).send_keys(Keys.SPACE)

        value = self.browser.\
            find_element_by_css_selector(
                "#activiti_form #output_filename"
            ).get_attribute('value')

        self.assertEqual("Activiti-1.0ent-Dan-temp.lic", value)
