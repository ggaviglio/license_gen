from .base import FunctionalTest
from unittest import skip


class HomePageTest(FunctionalTest):


    def get_form_elements(self, brand):
        form_elements = {}
        form_elements['notes'] = self.browser.find_element_by_css_selector("#"+brand+"_form #notes")
        form_elements['external_id'] = self.browser.find_element_by_css_selector("#"+brand+"_form #external_id")
        form_elements['external_id_type'] = self.browser.find_element_by_css_selector("#"+brand+"_form #external_id_type")

        form_elements['checkboxes'] = self.browser.find_elements_by_css_selector("#"+brand+"_form #tag_license_types input")

        form_elements['account_holder_name'] = self.browser.find_element_by_css_selector("#"+brand+"_form #field_holder_name")

        form_elements['license_filename'] = self.browser.find_element_by_css_selector("#"+brand+"_form #output_filename")

        if brand == "alfresco":
            form_elements['release_key'] = self.browser.find_element_by_css_selector("#"+brand+"_form select#release_key > option[selected='selected']")

            form_elements['expiry_days'] = self.browser.find_element_by_css_selector("#"+brand+"_form #field_days")
            form_elements['maximum_users'] = self.browser.find_element_by_css_selector("#"+brand+"_form #field_max_users")
            form_elements['no_heartbeat']  = self.browser.find_element_by_css_selector("#"+brand+"_form #field_no_heartbeat")
            form_elements['heartbeat_url'] = self.browser.find_element_by_css_selector("#"+brand+"_form #field_heartbeat_url")
            form_elements['cluster_enabled'] = self.browser.find_element_by_css_selector("#"+brand+"_form #field_cluster_enabled")
            form_elements['license_type'] = self.browser.find_element_by_css_selector("select#field_license_type > option[selected='selected']")

            form_elements['maximum_documents'] = self.browser.find_element_by_css_selector("#"+brand+"_form #field_max_docs")
            form_elements['cloud_sync_enabled'] = self.browser.find_element_by_css_selector("#"+brand+"_form #field_cloud_sync")
            form_elements['cryptodoc_enabled'] = self.browser.find_element_by_css_selector("#"+brand+"_form #field_cryptodoc_enabled")
        else:   #Activiti
            form_elements['number_admins'] = self.browser.find_element_by_css_selector("#activiti_form #field_number_of_admins")
            form_elements['number_editors'] = self.browser.find_element_by_css_selector("#activiti_form #field_number_of_editors")
            form_elements['multi_tenant'] = self.browser.find_element_by_css_selector("select#field_multi_tenant > option[selected='selected']")
            form_elements['version'] = self.browser.find_element_by_css_selector("select#field_version > option[selected='selected']")
            form_elements['number_licenses'] = self.browser.find_element_by_css_selector("#activiti_form #field_number_of_licenses")
            form_elements['number_processes'] = self.browser.find_element_by_css_selector("#activiti_form #field_number_of_processes")
            form_elements['default_tenant'] = self.browser.find_element_by_css_selector("#activiti_form #field_default_tenant")

        return form_elements

    def check_form_elements_empty(self, brand, form_elements):
        self.assertEqual(form_elements['notes'].get_attribute('value'), "")
        self.assertEqual(form_elements['external_id'].get_attribute('value'), "")
        self.assertEqual(form_elements['external_id_type'].get_attribute('value'), "")

        num_selected_checkboxes = 0
        for checkbox in form_elements['checkboxes']:
            if checkbox.is_selected() == True:
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
            self.assertEqual(form_elements['license_type'].get_attribute('value'), 'team')

            self.assertEqual(form_elements['maximum_documents'].get_attribute('value'), "")
            self.assertEqual(form_elements['cloud_sync_enabled'].is_selected(), False)
            self.assertEqual(form_elements['cryptodoc_enabled'].is_selected(), False)
        else:   #Activiti
            self.assertEqual(form_elements['number_admins'].get_attribute('value'), "")
            self.assertEqual(form_elements['number_editors'].get_attribute('value'), "")
            self.assertEqual(form_elements['multi_tenant'].get_attribute('value'), "false")
            self.assertEqual(form_elements['version'].get_attribute('value'), '1.0ent')
            self.assertEqual(form_elements['number_licenses'].get_attribute('value'), "")
            self.assertEqual(form_elements['number_processes'].get_attribute('value'), "")
            self.assertEqual(form_elements['default_tenant'].get_attribute('value'), "")

        self.assertEqual(form_elements['license_filename'].get_attribute('value'), "")

    def check_form_elements_filled(self, brand, form_elements):
        self.assertEqual(form_elements['notes'].get_attribute('value'), "some notes")
        self.assertEqual(form_elements['external_id'].get_attribute('value'), "some external id")
        self.assertEqual(form_elements['external_id_type'].get_attribute('value'), "some external id type")

        num_selected_checkboxes = 0
        for checkbox in form_elements['checkboxes']:
            if checkbox.is_selected() == True:
                num_selected_checkboxes = num_selected_checkboxes + 1

        self.assertEqual(num_selected_checkboxes, len( form_elements['checkboxes']))

        self.assertEqual(form_elements['account_holder_name'].get_attribute('value'), "some account holder name")

        if brand == "alfresco":
            self.assertEqual(form_elements['release_key'].get_attribute('value'), "ent31")

            self.assertEqual(form_elements['expiry_days'].get_attribute('value'), "3")
            self.assertEqual(form_elements['maximum_users'].get_attribute('value'), "3")
            self.assertEqual(form_elements['no_heartbeat'].is_selected(), True)
            self.assertEqual(form_elements['heartbeat_url'].get_attribute('value'), "some heartbeat url")
            self.assertEqual(form_elements['cluster_enabled'].is_selected(), True)
            self.assertEqual(form_elements['license_type'].get_attribute('value'), 'enterprise')

            self.assertEqual(form_elements['maximum_documents'].get_attribute('value'), "3")
            self.assertEqual(form_elements['cloud_sync_enabled'].is_selected(), True)
            self.assertEqual(form_elements['cryptodoc_enabled'].is_selected(), True)
        else:   #Activiti
            self.assertEqual(form_elements['number_admins'].get_attribute('value'), "3")
            self.assertEqual(form_elements['number_editors'].get_attribute('value'), "3")
            self.assertEqual(form_elements['multi_tenant'].get_attribute('value'), "true")
            self.assertEqual(form_elements['version'].get_attribute('value'), "1.0ent")
            self.assertEqual(form_elements['number_licenses'].get_attribute('value'), "3")
            self.assertEqual(form_elements['number_processes'].get_attribute('value'), "3")
            self.assertEqual(form_elements['default_tenant'].get_attribute('value'), "some tenant")

        self.assertEqual(form_elements['license_filename'].get_attribute('value'), "some license filename")

    def fill_in_form_elements(self, brand, form_elements):
        form_elements['notes'].send_keys('some notes')
        form_elements['external_id'].send_keys('some external id')
        form_elements['external_id_type'].send_keys('some external id type')

        for checkbox in form_elements['checkboxes']:
            checkbox.click()

        form_elements['account_holder_name'].send_keys('some account holder name')

        if brand == "alfresco":
            form_elements['release_key'] = self.browser.find_element_by_css_selector("#"+brand+"_form select#release_key > option[value='ent31']")
            form_elements['release_key'].click()

            form_elements['expiry_days'].send_keys('3')
            form_elements['maximum_users'].send_keys('3')
            form_elements['no_heartbeat'].click()
            form_elements['heartbeat_url'] .send_keys('some heartbeat url')
            form_elements['cluster_enabled'].click()
            form_elements['license_type'] = self.browser.find_element_by_css_selector("select#field_license_type > option[value='enterprise']")
            form_elements['license_type'].click()

            form_elements['maximum_documents'].send_keys('3')
            form_elements['cloud_sync_enabled'].click()
            form_elements['cryptodoc_enabled'].click()
        else: #Activiti
            form_elements['number_admins'].send_keys('3')
            form_elements['number_editors'].send_keys('3')
            form_elements['multi_tenant'] = self.browser.find_element_by_css_selector("select#field_multi_tenant > option[value='true']")
            form_elements['multi_tenant'].click()

            form_elements['version'] = self.browser.find_element_by_css_selector("select#field_version > option[selected='selected']")
            form_elements['version'].click()
            form_elements['number_licenses'].send_keys('3')
            form_elements['number_processes'].send_keys('3')
            form_elements['default_tenant'].send_keys('some tenant')

        form_elements['license_filename'].send_keys('some license filename')

    def test_site_loads(self):
        # Alfrescan wants to generate a license, visits the URL
        # They notice the page title and header mention the license generator
        self.assertIn("License Generator", self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertEqual("License Generator", header_text)

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
        # Alfrescan procedes to fill in each form elements within the tab selected
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
        # Alfrescan procedes to fill in each form elements within the tab selected
        self.fill_in_form_elements("activiti", form_elements_activiti)
        # Alfrescan sees how every form element hold some information
        self.check_form_elements_filled("activiti", form_elements_activiti)
        # Alfrescan goes to the Clear form button and click over this
        self.browser.find_element_by_css_selector("#activiti_form #clear_form").click()

        # Alfrescan check all form elements available to be filled
        form_elements_activiti = self.get_form_elements("activiti")
        # Alfrescan sees how every form element is empty
        self.check_form_elements_empty("activiti", form_elements_activiti)
