from .base import FunctionalTest
from unittest import skip


class NavTest(FunctionalTest):

    def test_nav_is_visible(self):
        # Alfrescan sees a navegation bar in the top of the page
        nav_bar = self.browser.find_element_by_css_selector(".navbar")
        self.assertTrue(nav_bar.is_displayed())

    def test_nav_has_four_links(self):
        # Alfrescan sees the nav bar has 4 clickable elements
        self.assertEqual(len(self.browser.find_elements_by_css_selector(".navbar a")), 4)

    def test_home_link_redirects_to_top_home_page(self):
        # Alfrescan clicks the home link -Alfresco/Activiti license generator-
        home_url = self.browser.current_url
        #self.browser.find_element_by_id('home_link').click()
        self.browser.find_element_by_css_selector('nav [data-original-title="top home"]').click()
        # Alfrescan is redirected to the home page
        self.assertEqual(home_url+"#", self.browser.current_url)

    def test_jira_link_redirects_to_jira(self):
        # Alfrescan clicks the jira link
        self.browser.find_element_by_css_selector('nav [data-original-title="raise jira ticket"]').click()
        self.browser.switch_to.window(self.browser.window_handles[1])
        # Alfrescan is redirected to the jira ticket page
        self.assertIn("jira", self.browser.current_url)

    def test_home_link_keeps_same_name_as_clicked_alfresco_tab(self):
        # Alfrescan sees the Alfresco tab and click on it
        self.browser.find_element_by_css_selector('#myTab li [href="#alfresco_tab"]').click()
        selected_tab = self.browser.find_element_by_css_selector('#myTab li.active a')
        # Title of that tab matches with the text that appears on the navbar
        nav_title = self.browser.find_element_by_css_selector('.navbar-brand')

        self.assertEqual(selected_tab.text, nav_title.text)

    def test_home_link_keeps_same_name_as_clicked_activiti_tab(self):
        # Alfrescan sees the Activiti tab and click on it
        self.browser.find_element_by_css_selector('#myTab li [href="#activiti_tab"]').click()
        selected_tab = self.browser.find_element_by_css_selector('#myTab li.active a')
        # Title of that tab matches with the text that appears on the navbar
        nav_title = self.browser.find_element_by_css_selector('.navbar-brand')
        self.assertEqual(selected_tab.text, nav_title.text)

    @skip
    def test_license_check_link_shows_popup(self):
        pass

    @skip
    def test_logout_link_redirects_to_login_page(self):
        # Alfrescan click the log out link
        self.browser.find_element_by_css_selector('nav [data-original-title="log out"]').click()
        self.assertIn("login", self.browser.current_url)
