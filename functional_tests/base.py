from django.test import LiveServerTestCase
from selenium import webdriver

MY_IP = "http://192.168.59.103"


class FunctionalTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Remote(MY_IP + ":4444/wd/hub", webdriver.DesiredCapabilities.FIREFOX)
        self.browser.implicitly_wait(3)
        # Alfrescan wants to generate a license, visits the URL
        self.browser.get(MY_IP)

    def tearDown(self):
        self.browser.quit()

    def get_form_elements(self, brand):
        form_elements = {}
        form_elements['notes'] = self.browser.find_element_by_css_selector("#"+brand+"_form #notes")
        form_elements['external_id'] = self.browser.find_element_by_css_selector("#"+brand+"_form #external_id")
        form_elements['external_id_type'] = self.browser.find_element_by_css_selector("#"+brand+"_form #external_id_type")
        form_elements['checkboxes'] = self.browser.find_elements_by_css_selector("#"+brand+"_form #tag_license_types input")
        form_elements['account_holder_name'] = self.browser.find_element_by_css_selector("#"+brand+"_form #field_holder_name")
        form_elements['license_filename'] = self.browser.find_element_by_css_selector("#"+brand+"_form #output_filename")

        if brand == "alfresco":
            form_elements['release_key'] = self.browser.find_element_by_css_selector("#alfresco_form select#release_key > option[selected='selected']")
            form_elements['expiry_days'] = self.browser.find_element_by_css_selector("#alfresco_form #field_days")
            form_elements['maximum_users'] = self.browser.find_element_by_css_selector("#alfresco_form #field_max_users")
            form_elements['no_heartbeat'] = self.browser.find_element_by_css_selector("#alfresco_form #field_no_heartbeat")
            form_elements['heartbeat_url'] = self.browser.find_element_by_css_selector("#alfresco_form #field_heartbeat_url")
            form_elements['cluster_enabled'] = self.browser.find_element_by_css_selector("#alfresco_form #field_cluster_enabled")
            form_elements['license_type'] = self.browser.find_element_by_css_selector("select#field_license_type > option[selected='selected']")
            form_elements['maximum_documents'] = self.browser.find_element_by_css_selector("#alfresco_form #field_max_docs")
            form_elements['cloud_sync_enabled'] = self.browser.find_element_by_css_selector("#alfresco_form #field_cloud_sync")
            form_elements['cryptodoc_enabled'] = self.browser.find_element_by_css_selector("#alfresco_form #field_cryptodoc_enabled")
        else:   # Activiti
            form_elements['number_admins'] = self.browser.find_element_by_css_selector("#activiti_form #field_number_of_admins")
            form_elements['number_editors'] = self.browser.find_element_by_css_selector("#activiti_form #field_number_of_editors")
            form_elements['multi_tenant'] = self.browser.find_element_by_css_selector("select#field_multi_tenant > option[selected='selected']")
            form_elements['version'] = self.browser.find_element_by_css_selector("select#field_version > option[selected='selected']")
            form_elements['number_licenses'] = self.browser.find_element_by_css_selector("#activiti_form #field_number_of_licenses")
            form_elements['number_processes'] = self.browser.find_element_by_css_selector("#activiti_form #field_number_of_processes")
            form_elements['default_tenant'] = self.browser.find_element_by_css_selector("#activiti_form #field_default_tenant")
            form_elements['number_apps'] = self.browser.find_element_by_css_selector("#activiti_form #field_number_of_apps")

        return form_elements

    def check_form_elements_empty(self, brand, form_elements):
        self.assertEqual(form_elements['notes'].get_attribute('value'), "")
        self.assertEqual(form_elements['external_id'].get_attribute('value'), "")
        self.assertEqual(form_elements['external_id_type'].get_attribute('value'), "")

        num_selected_checkboxes = 0
        for checkbox in form_elements['checkboxes']:
            if checkbox.is_selected() is True:
                num_selected_checkboxes = num_selected_checkboxes + 1

        self.assertEqual(num_selected_checkboxes, 0)
        self.assertEqual(form_elements['account_holder_name'].get_attribute('value'), "")

        if brand == "alfresco":
            self.assertEqual(form_elements['release_key'].get_attribute('value'), "ent50")
            self.assertEqual(form_elements['expiry_days'].get_attribute('value'), "")
            self.assertEqual(form_elements['maximum_users'].get_attribute('value'), "")
            self.assertEqual(form_elements['no_heartbeat'].is_selected(), False)
            self.assertEqual(form_elements['heartbeat_url'].get_attribute('value'), "")
            self.assertEqual(form_elements['cluster_enabled'].is_selected(), False)
            self.assertEqual(form_elements['license_type'].get_attribute('value'), 'TEAM')
            self.assertEqual(form_elements['maximum_documents'].get_attribute('value'), "")
            self.assertEqual(form_elements['cloud_sync_enabled'].is_selected(), False)
            self.assertEqual(form_elements['cryptodoc_enabled'].is_selected(), False)
        else:   # Activiti
            self.assertEqual(form_elements['number_admins'].get_attribute('value'), "")
            self.assertEqual(form_elements['number_editors'].get_attribute('value'), "")
            self.assertEqual(form_elements['multi_tenant'].get_attribute('value'), "false")
            self.assertEqual(form_elements['version'].get_attribute('value'), '1.0ent')
            self.assertEqual(form_elements['number_licenses'].get_attribute('value'), "")
            self.assertEqual(form_elements['number_processes'].get_attribute('value'), "")
            self.assertEqual(form_elements['default_tenant'].get_attribute('value'), "")
            self.assertEqual(form_elements['number_apps'].get_attribute('value'), "")

        self.assertEqual(form_elements['license_filename'].get_attribute('value'), "")

    def check_form_elements_filled(self, brand, form_elements):
        self.assertEqual(form_elements['notes'].get_attribute('value'), "some notes")
        self.assertEqual(form_elements['external_id'].get_attribute('value'), "some external id")
        self.assertEqual(form_elements['external_id_type'].get_attribute('value'), "some external id type")

        num_selected_checkboxes = 0
        for checkbox in form_elements['checkboxes']:
            if checkbox.is_selected() is True:
                num_selected_checkboxes = num_selected_checkboxes + 1

        self.assertEqual(num_selected_checkboxes, len(form_elements['checkboxes']))
        self.assertEqual(form_elements['account_holder_name'].get_attribute('value'), "some account holder name")

        if brand == "alfresco":
            self.assertEqual(form_elements['release_key'].get_attribute('value'), "ent31")
            self.assertEqual(form_elements['expiry_days'].get_attribute('value'), "3")
            self.assertEqual(form_elements['maximum_users'].get_attribute('value'), "3")
            self.assertEqual(form_elements['no_heartbeat'].is_selected(), True)
            self.assertEqual(form_elements['heartbeat_url'].get_attribute('value'), "some heartbeat url")
            self.assertEqual(form_elements['cluster_enabled'].is_selected(), True)
            self.assertEqual(form_elements['license_type'].get_attribute('value'), 'ENTERPRISE')
            self.assertEqual(form_elements['maximum_documents'].get_attribute('value'), "3")
            self.assertEqual(form_elements['cloud_sync_enabled'].is_selected(), True)
            self.assertEqual(form_elements['cryptodoc_enabled'].is_selected(), True)
        else:   # Activiti
            self.assertEqual(form_elements['number_admins'].get_attribute('value'), "3")
            self.assertEqual(form_elements['number_editors'].get_attribute('value'), "3")
            self.assertEqual(form_elements['multi_tenant'].get_attribute('value'), "true")
            self.assertEqual(form_elements['version'].get_attribute('value'), "1.0ent")
            self.assertEqual(form_elements['number_licenses'].get_attribute('value'), "3")
            self.assertEqual(form_elements['number_processes'].get_attribute('value'), "3")
            self.assertEqual(form_elements['default_tenant'].get_attribute('value'), "some tenant")
            self.assertEqual(form_elements['number_apps'].get_attribute('value'), "25")

        self.assertEqual(form_elements['license_filename'].get_attribute('value'), "some license filename")

    def fill_in_form_elements(self, brand, form_elements):
        form_elements['notes'].send_keys('some notes')
        form_elements['external_id'].send_keys('some external id')
        form_elements['external_id_type'].send_keys('some external id type')

        for checkbox in form_elements['checkboxes']:
            checkbox.click()

        form_elements['account_holder_name'].send_keys('some account holder name')

        if brand == "alfresco":
            form_elements['release_key'] = self.browser.find_element_by_css_selector("#alfresco_form select#release_key > option[value='ent31']")
            form_elements['release_key'].click()
            form_elements['expiry_days'].send_keys('3')
            form_elements['maximum_users'].send_keys('3')
            form_elements['no_heartbeat'].click()
            form_elements['heartbeat_url'] .send_keys('some heartbeat url')
            form_elements['cluster_enabled'].click()
            form_elements['license_type'] = self.browser.find_element_by_css_selector("select#field_license_type > option[value='ENTERPRISE']")
            form_elements['license_type'].click()
            form_elements['maximum_documents'].send_keys('3')
            form_elements['cloud_sync_enabled'].click()
            form_elements['cryptodoc_enabled'].click()
        else:  # Activiti
            form_elements['number_admins'].send_keys('3')
            form_elements['number_editors'].send_keys('3')
            form_elements['multi_tenant'] = self.browser.find_element_by_css_selector("select#field_multi_tenant > option[value='true']")
            form_elements['multi_tenant'].click()
            form_elements['version'] = self.browser.find_element_by_css_selector("select#field_version > option[selected='selected']")
            form_elements['version'].click()
            form_elements['number_licenses'].send_keys('3')
            form_elements['number_processes'].send_keys('3')
            form_elements['default_tenant'].send_keys('some tenant')
            form_elements['number_apps'].send_keys('25')

        form_elements['license_filename'].send_keys('some license filename')
