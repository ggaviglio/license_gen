from .base import FunctionalTest


class GenerateLicenseTest(FunctionalTest):

    def view_alfresco_generate_button(self):
        # Alfrescan goes to the main alfresco tab
        self.browser.find_element_by_css_selector('#myTab li [href="#alfresco_tab"]').click()
        # Alfrescan go right to the 'generate and download' button
        self.browser.find_element_by_css_selector("#alfresco_form #generate_form").click()

    def view_activiti_generate_button(self):
        # Alfrescan goes to the main activiti tab
        self.browser.find_element_by_css_selector('#myTab li [href="#activiti_tab"]').click()
        # Alfrescan go right to the 'generate and download' button
        self.browser.find_element_by_css_selector("#activiti_form #generate_form").click()


    def test_a(self):
        self.view_activiti_generate_button()
        self.view_alfresco_generate_button()
        print("done")