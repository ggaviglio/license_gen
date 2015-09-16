from .base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):

    def test_layout_and_styling(self):
        self.browser.set_window_size(1024, 768)

        # Alfrescan notices the logo is positioned to the right
        logo_element = self.browser.find_element_by_css_selector(
            ".navbar-header img"
        )
        navbar_width = self.browser.find_element_by_css_selector(
            ".navbar-header"
        ).size['width']

        self.assertLess(logo_element.location['x'], navbar_width / 2)

    def test_responsive_layout_top_navbar(self):
        self.browser.set_window_size(1024, 768)

        # Alfrescan sees how the top navegation bar has some options
        actual_options_top_navbar = self.browser.find_elements_by_css_selector(
            '.navbar-nav li a'
        )
        expected_options_top_navbar = [
            "Raise a JIRA ticket for this app",
            "Upload and check an existing license"
        ]
        for options in actual_options_top_navbar[:2]:
            self.assertIn(options.text, expected_options_top_navbar)

        # At the minute the browser get resized into a smaller view
        self.browser.set_window_size(600, 322)

        # Alfrescan will not see previous elements. They will vanished
        refresh_options_top_navbar = self.browser.\
            find_elements_by_css_selector('.navbar-nav li.active a')
        self.assertEqual(len(refresh_options_top_navbar), 0)
