from .base import FunctionalTest, LOGIN


class LoginPageTest(FunctionalTest):

    def view_login_page(self):
        self.browser.find_element_by_css_selector('[data-original-title="log out"]').click()

    def test_login_windows_loads(self):
        # Alfrescan wants to generate a new license
        self.view_login_page()
        login_form = self.browser.find_element_by_css_selector(".main-login")
        self.assertTrue(login_form.is_displayed())

    def test_submitting_login_with_invalid_information_displays_error_message(self):
        # Alfrescan submit an invalid information, therefore an informative
        # error message will be displayed
        self.view_login_page()
        username_input = self.browser.find_element_by_id('username')
        password_input = self.browser.find_element_by_id('password')
        username_input.send_keys('wrong username')
        password_input.send_keys('wrong password')
        self.browser.find_element_by_class_name('btn').click()

        auth_error = self.browser.find_element_by_id('auth_error')
        self.assertTrue(auth_error.is_displayed())
        self.assertIn(
            "Your authentication details have not been recognized",
            auth_error.text
        )

    def test_submitting_login_with_valid_information_succesfully_logins(self):
        # Alfrescan submit a valid information, so it will be
        # successfully logged in and it could be seen the navbar navigation
        # as usual...
        self.view_login_page()
        username_input = self.browser.find_element_by_id('username')
        password_input = self.browser.find_element_by_id('password')
        username_input.send_keys(LOGIN['USERNAME'])
        password_input.send_keys(LOGIN['PASSWORD'])
        self.browser.find_element_by_class_name('btn').click()

        # After being logged in successfully, it can be seen the navbar
        nav_bar = self.browser.find_element_by_class_name('navbar')
        self.assertTrue(nav_bar.is_displayed())
