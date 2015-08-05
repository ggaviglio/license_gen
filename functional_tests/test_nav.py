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

    def test_home_link_redirects_to_home_page(self):
        # Alfrescan clicks the home link -Alfresco/Activiti license generator-
        home_url = self.browser.current_url
        self.browser.find_element_by_id('home_link').click()
        # Alfrescan is redirected to the home page
        self.assertEqual(home_url, self.browser.current_url)

    def test_jira_link_redirects_to_jira(self):
        # Alfrescan clicks the jira link
        self.browser.find_element_by_id('jira_link').click()
        # Alfrescan is redirected to the jira ticket page
        self.assertIn("jira", self.browser.current_url)
    @skip
    def test_license_check_link_shows_popup(self):
        pass

    @skip
    def test_logout_link_redirects_to_login_page(self):
        # Alfrescan click the log out link
        self.browser.find_element_by_id('log_out_link').click()
        self.assertIn("login", self.browser.current_url)
