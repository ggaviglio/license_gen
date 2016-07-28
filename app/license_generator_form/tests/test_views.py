from django.test import TestCase
from license_generator_form.models import License
from django.contrib.auth.models import User


class NewLicenseTest(TestCase):

    def test_saving_a_POST_request(self):
        self.client.post(
            '/generate/alfresco/',
            data={
                'release_key' : '123456789',
                'notes' : 'this is a test',
                'external_id' : 'abcdefg',
                'external_id_type' : 'salesforce',
                'license_types' : 'Trial',
                'field_holder_name' : 'Random Roddy',
                'field_days' : 24,
                'field_max_users' : 1,
                'field_no_heartbeat' : True ,
                'field_heartbeat_url' : "https://www.yeehee.com",
                'field_cluster_enabled' : False,
                'field_license_group' : 'Team',
                'field_end_date' : '3/4/2017',
                'field_max_docs' : 24,
                'field_cloud_sync' : False,
                'field_ats_end_date' : '5/3/2017',
                'field_cryptodoc_enabled' : True
            }
        )

        self.assertEqual(License.objects.count(), 1)
        
        saved_license = License.objects.first()
        test_License = License()

        test_License.release_key = '123456789'
        test_License.notes = 'this is a test'
        test_License.external_id = 'abcdefg'
        test_License.external_id_type = 'salesforce'
        test_License.license_type = 'Trial'
        test_License.account_holder = 'Random Roddy'
        test_License.expiry_days = 24
        test_License.max_users = 1
        test_License.no_heartbeat = True 
        test_License.heartbeat_url = "https://www.yeehee.com"
        test_License.cluster_enabled = False
        test_License.license_group = 'Team'
        test_License.expiry_date = '3/4/2017'
        test_License.max_docs = 24
        test_License.cloud_sync = False
        test_License.server_end_date = '5/3/2017'
        test_License.crypto_doc = True
        # model._meta.get_all_field_names()

        print("fields")
        for field in saved_license._meta.get_fields():
            print(field.saved_license)           



        # self.assertEqual(Item.objects.count(), 1)
        # new_item = Item.objects.first()
        # self.assertEqual(new_item.text, 'A new list item')


    # def test_redirects_after_POST(self):
    #     response = self.client.post(
    #         '/lists/new',
    #         data={'item_text': 'A new list item'}
    #     )
    #     new_list = List.objects.first()
    #     self.assertRedirects(response, '/lists/%d/' % (new_list.id,))

