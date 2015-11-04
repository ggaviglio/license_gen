from .base import FunctionalTest
from unittest import skip
import time


class NavTest(FunctionalTest):

    def test_nav_is_visible(self):
        # Alfrescan sees a navegation bar in the top of the page
        nav_bar = self.browser.find_element_by_css_selector(".navbar")
        self.assertTrue(nav_bar.is_displayed())

    def test_nav_has_four_links(self):
        # Alfrescan sees the nav bar has 4 clickable elements
        self.assertEqual(
            len(self.browser.find_elements_by_css_selector(".navbar a")),
            4
        )

    def test_nav_has_logo(self):
        # Alfrescan sees a logo
        logo_element = self.browser.find_element_by_css_selector(
            ".navbar-header img"
        )
        self.assertTrue(logo_element)

    def test_home_link_redirects_to_top_home_page(self):
        # Alfrescan clicks the home link -Alfresco/Activiti license generator-
        home_url = self.browser.current_url
        self.browser.find_element_by_css_selector(
            'nav [data-original-title="top home"]'
        ).click()
        # Alfrescan is redirected to the home page
        self.assertEqual(home_url+"#", self.browser.current_url)

    def test_jira_link_redirects_to_jira(self):
        # Alfrescan clicks the jira link
        self.browser.find_element_by_css_selector(
            'nav [data-original-title="raise jira ticket"]'
        ).click()
        self.browser.switch_to.window(self.browser.window_handles[1])
        # Alfrescan is redirected to the jira ticket page
        self.assertIn("jira", self.browser.current_url)

    def test_home_link_keeps_same_name_as_clicked_alfresco_tab(self):
        # Alfrescan sees the default nav and tab title
        default_topbar_title = self.browser.find_element_by_css_selector(
            '.navbar-brand'
        ).text
        default_selected_tab = self.browser.find_element_by_css_selector(
            '#tabSwitcher li.active a'
        ).text
        self.assertEqual(default_topbar_title, default_selected_tab)

        # Alfrescan clicks on the Alfresco tab
        self.browser.find_element_by_css_selector(
            '#tabSwitcher li [href="#alfresco_tab"]'
        ).click()
        new_selected_tab = self.browser.find_element_by_css_selector(
            '#tabSwitcher li.active a'
        ).text
        self.assertEqual(default_selected_tab, new_selected_tab)

        # Title of that tab matches with the text that appears on the navbar
        new_topbar_title = self.browser.find_element_by_css_selector(
            '.navbar-brand'
        ).text
        self.assertEqual(default_topbar_title, new_topbar_title)
        self.assertEqual(new_selected_tab, new_topbar_title)

    def test_home_link_keeps_same_name_as_clicked_activiti_tab(self):
        # Alfrescan sees the default nav and tab title
        default_topbar_title = self.browser.find_element_by_css_selector(
            '.navbar-brand'
        ).text
        default_selected_tab = self.browser.find_element_by_css_selector(
            '#tabSwitcher li.active a'
        ).text
        self.assertEqual(default_topbar_title, default_selected_tab)

        # Alfrescan clicks on the Activiti tab
        self.browser.find_element_by_css_selector(
            '#tabSwitcher li [href="#activiti_tab"]'
        ).click()
        new_selected_tab = self.browser.find_element_by_css_selector(
            '#tabSwitcher li.active a'
        ).text
        self.assertNotEqual(default_selected_tab, new_selected_tab)

        # Title of that tab matches with the text that appears on the navbar
        new_topbar_title = self.browser.find_element_by_css_selector(
            '.navbar-brand'
        ).text
        self.assertNotEqual(default_topbar_title, new_topbar_title)
        self.assertEqual(new_selected_tab, new_topbar_title)

    def test_license_check_link_shows_upload_dialog(self):
        # Alfrescan clicks on the link
        self.browser.find_element_by_css_selector(
            '[data-original-title="upload and check license"]'
        ).click()
        time.sleep(0.5)
        # Alfrescan sees a file upload dialog
        upload_dialog = self.browser.find_element_by_css_selector(
            '.modal-dialog'
        )
        self.assertTrue(upload_dialog.is_displayed())
        # Alfrescan checks the text of this dialog
        text_dialog = self.browser.\
            find_element_by_css_selector('#AlfrescoModalLicense').text
        self.assertEqual(
            "Upload and check an existing Alfresco license", text_dialog
        )

    def test_license_check_dialog_turns_up_as_excepted(self):
        upload_dialog = self.browser.find_element_by_css_selector(
            '.modal-dialog'
        )
        # There is no upload dialog
        self.assertFalse(upload_dialog.is_displayed())

        # Alfrescan clicks on the license link
        self.browser.find_element_by_css_selector(
            '[data-original-title="upload and check license"]'
        ).click()
        time.sleep(0.5)

        # Alfrescan sees the dialog
        self.assertTrue(upload_dialog.is_displayed())

        #Alfrescan closes the upload dialog
        self.browser.find_element_by_css_selector('#licenseClose').click()
        time.sleep(0.5)

        # Alfrescan checks dialog is not visible anymore
        self.assertFalse(upload_dialog.is_displayed())

    def test_license_check_dialog_has_upload_button_disabled(self):
        # Alfrescan clicks on the link
        self.browser.find_element_by_css_selector(
            '[data-original-title="upload and check license"]'
        ).click()
        time.sleep(0.5)

        choose_btn = self.browser.find_element_by_css_selector(
            '#licenseChooseFile'
        )
        upload_btn = self.browser.find_element_by_css_selector(
            '#licenseCheckUpload'
        )

        # choosefile btn is enable
        self.assertTrue(choose_btn.is_enabled())
        # upload btn is disabled when no file selected
        self.assertFalse(upload_btn.is_enabled())

    def test_license_check_dialog_keeps_same_name_as_clicked_radio_btn(self):
        # Alfrescan clicks on the link
        self.browser.find_element_by_css_selector(
            '[data-original-title="upload and check license"]'
        ).click()
        time.sleep(0.5)

        # Alfrescan sees the default Modal title
        default_topbar_title = self.browser.find_element_by_css_selector(
            '#AlfrescoModalLicense'
        ).text

        default_selected_radio = self.browser.find_element_by_css_selector(
            "#radioalternative input[checked='checked']"
        ).get_attribute('value')

        self.assertIn(default_selected_radio, default_topbar_title)

        # Alfrescan select the Activiti radio button
        self.browser.find_element_by_css_selector(
            "#radioalternative input[value='Activiti']"
        ).click()
        new_selected_radio = self.browser.find_element_by_css_selector(
            '#AlfrescoModalLicense'
        ).text

        self.assertNotEqual(default_selected_radio, new_selected_radio)

        #Alfrescan sees the new Modal title
        new_topbar_title = self.browser.find_element_by_css_selector(
            '#AlfrescoModalLicense'
        ).text

        self.assertIn(new_selected_radio, new_topbar_title)

    def test_submitting_logout_successfully_logout(self):
        # Alfrescan wants to log out of the system, so the
        # logout link is clicked
        self.browser.find_element_by_css_selector(
            '[data-original-title="log out"]'
        ).click()

        # We can see how the main login form it turns up
        login_form = self.browser.find_element_by_class_name('main-login')
        self.assertTrue(login_form.is_displayed())
        self.assertIn("login", self.browser.current_url)
