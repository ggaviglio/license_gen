from django.test import TestCase
from license_generator_form.models import License


class LicenseSavingTest(TestCase):

    def test_saving_and_retrieving_alfresco_details(self):
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
        #test_License.expiry_date = '3/4/2016'
        test_License.max_docs = 24
        test_License.cloud_sync = False
        test_License.server_end_date = '5/3/2017'
        test_License.crypto_doc = True

        test_License.save()
        saved_license = License.objects.first()
        self.assertEqual(test_License, saved_license)

        # self.assertEqual(saved_license.release_key, '123456789')
        # self.assertEqual(saved_license.notes, 'this is a test')
        # self.assertEqual(saved_license.external_id, 'abcdefg')
        # self.assertEqual(saved_license.external_id_type, 'salesforce')
        # self.assertEqual(saved_license.license_type, 'Trial')
        # self.assertEqual(saved_license.account_holder, 'Random Roddy')
        # self.assertEqual(saved_license.expiry_days, 24)
        # self.assertEqual(saved_license.max_users, 1)
        # self.assertEqual(saved_license.no_heartbeat, True )
        # self.assertEqual(saved_license.cluster_enabled, False)
        # self.assertEqual(saved_license.license_group, 'Team')
        # #assert date
        # self.assertEqual(saved_license.max_docs, 24)
        # self.assertEqual(saved_license.cloud_sync, False)
        # self.assertEqual(saved_license.crypto_doc, True)
        #heartbeat url, server end

        self.fail("Finish test for date!")


