from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from license_generator_form.views import home_page
from license_generator_form.views import handler404, handler500

from unittest.mock import patch, Mock


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_root_url_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)

    def test_wrong_url_returns_404(self):
        request = HttpRequest()
        response = handler404(request)
        self.assertEqual(response.status_code, 404)

    def test_internal_server_error_returns_500(self):
        request = HttpRequest()
        response = handler500(request)
        self.assertEqual(response.status_code, 500)


class GenerateLicenseTest(TestCase):

    @patch('license_generator_form.views.generate')
    def test_calls_license_generator_with_good_alfresco_data(
            self, mock_license
    ):

        mock_license.generate.return_value = b'Stream of bytes to receive'

        alfresco_data = {
            'alfresco_generate_btn': '1',
            'release_key': 'ent30',
            'notes': 'some notes',
            'external_id': 'some external id',
            'external_id_type': 'salesforce',
            'tag_trial': '1',
            'tag_internal_use_only': '1',
            'tag_proof_of_concept': '1',
            'tag_extension': '1',
            'tag_perpetual': '1',
            'field_holder_name': 'Sebastian',
            'field_days': 20,
            'field_max_users': 10,
            'field_no_heartbeat': '1',
            'field_heartbeat_url': 'some url',
            'field_cluster_enabled': '1',
            'field_license_type': 'enterprise',
            'field_end_date': '17-08-2015',
            'field_max_docs': 3,
            'field_cloud_sync': '1',
            'field_ats_end_date': '17-08-2015',
            'field_cryptodoc_enabled': '1',
            'output_filename': 'Alfresco-ent30-.lic',
        }

        user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
        response = self.client.post('/generate/', alfresco_data, HTTP_USER_AGENT=user_agent)

        mock_license.assert_called_once_with(alfresco_data)
        self.assertEqual(26, len(mock_license.generate(alfresco_data)))
        self.assertEqual(b'Stream of bytes to receive', mock_license.generate(alfresco_data))

        self.assertEqual(response['Content-Type'], 'application/octet-stream')
        self.assertEqual(response['Content-Length'], '502')
        self.assertIn('Alfresco-ent30-.lic', response['Content-Disposition'])


    @patch('license_generator_form.views.generate')
    def test_calls_license_generator_with_good_activiti_data(
        self, mock_license
    ):
        mock_license.generate.return_value = b'Stream of bytes to receive'

        activiti_data = {
            'activiti_generate_btn': '1',
            'notes': 'some notes',
            'external_id': 'some external id',
            'external_id_type': 'salesforce',
            'tag_trial': '1',
            'tag_internal_use_only': '1',
            'tag_proof_of_concept': '1',
            'tag_extension': '1',
            'tag_perpetual': '1',
            'field_holder_name': 'Sebastian',
            'field_start_day': '18-08-2015',
            'field_number_of_admins': 5,
            'field_number_of_editors': 3,
            'field_multi_tenant': 'true',
            'field_version': '1.0ent',
            'field_end_date': '20-08-2015',
            'field_number_of_licenses': 5,
            'field_number_of_processes': 6,
            'field_default_tenant': 'Seb',
            'output_filename': 'Activiti-ent50-.lic',
        }

        user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
        response = self.client.post('/generate/', activiti_data, HTTP_USER_AGENT=user_agent)

        self.assertTrue(mock_license.called)
        mock_license.assert_called_once_with(activiti_data)
        self.assertEqual(26, len(mock_license.generate(activiti_data)))
        self.assertEqual(b'Stream of bytes to receive', mock_license.generate(activiti_data))

        self.assertEqual(response['Content-Type'], 'application/octet-stream')
        self.assertEqual(response['Content-Length'], '458')
        self.assertIn('Activiti-ent50-.lic', response['Content-Disposition'])
    

    @patch('license_generator_form.views.generate')
    def test_calls_license_generator_with_no_alfresco_data(
        self, mock_license
    ):
        mock_license.generate.side_effect = Exception('dictionary is empty or incompleted!')
        alfresco_data = {
            'alfresco_generate_btn': '1',
            'field_max_users': 0,
            'release_key': 'ent50',
            'field_end_date': '',
            'tag_trial': 'None',
            'tag_internal_use_only': 'None',
            'tag_proof_of_concept': 'None',
            'tag_perpetual': 'None',
            'external_id': '',
            'field_heartbeat_url': '',
            'field_ats_end_date': '',
            'tag_extension': 'None',
            'field_days': 0,
            'output_filename': '',
            'external_id_type': '',
            'field_no_heartbeat': 'None',
            'field_cloud_sync': 'None',
            'field_max_docs': 0,
            'notes': '',
            'field_cryptodoc_enabled': 'None',
            'field_license_type': 'team',
            'field_holder_name': '',
            'field_cluster_enabled': 'None',
        }

        user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
        self.client.post('/generate/', alfresco_data, HTTP_USER_AGENT=user_agent)

        mock_license.assert_called_with(alfresco_data)
        self.assertRaises(Exception, mock_license.generate)

    @patch('license_generator_form.views.generate')
    def test_calls_license_generator_with_no_activiti_data(
        self, mock_license
    ):
        mock_license.generate.side_effect = Exception('dictionary is empty or incompleted!')
        activiti_data = {
            'activiti_generate_btn': '1',
            'external_id_type': '',
            'tag_proof_of_concept': 'None',
            'field_holder_name': '',
            'tag_perpetual': 'None',
            'field_number_of_admins': 0,
            'tag_extension': 'None',
            'output_filename': '',
            'tag_internal_use_only': 'None',
            'field_default_tenant': '',
            'field_version': '1.0ent',
            'field_start_day': 'None',
            'field_number_of_editors': 0,
            'field_multi_tenant': 'false',
            'field_end_date': '',
            'field_number_of_licenses': 0,
            'notes': '',
            'tag_trial': 'None',
            'external_id': '',
            'field_number_of_processes': 0,

        }

        user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
        response = self.client.post('/generate/', activiti_data, HTTP_USER_AGENT=user_agent)

        mock_license.assert_called_with(activiti_data)
        self.assertRaises(Exception, mock_license.generate)

    @patch('license_generator_form.views.generate')
    def test_calls_license_generator_with_bad_alfresco_data(
            self, mock_license
    ):
        mock_license.generate.side_effect = Exception('dictionary does contain bad data!')

        alfresco_data = {
            'alfresco_generate_btn': '1'
            'release_key': 'ent30',
            'notes': 'some notes',
            'external_id': 'some external id',
            'external_id_type': 'salesforce',
            'tag_trial': '1',
            'tag_internal_use_only': '1',
            'tag_proof_of_concept': '1',
            'tag_extension': '1',
            'tag_perpetual': '1',
            'field_holder_name': 'Sebastian',
            'field_days': '20',  # Here is the bad alfresco data. It should be a number
            'field_max_users': 10,
            'field_no_heartbeat': '1',
            'field_heartbeat_url': 'some url',
            'field_cluster_enabled': '1',
            'field_license_type': 'enterprise',
            'field_end_date': '17-08-2015',
            'field_max_docs': 3,
            'field_cloud_sync': '1',
            'field_ats_end_date': '17-08-2015',
            'field_cryptodoc_enabled': '1',
            'output_filename': 'Alfresco-ent50-.lic',
        }

        user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
        response = self.client.post('/generate/', alfresco_data, HTTP_USER_AGENT=user_agent)

        mock_license.alfresco.generate.assert_called_with(alfresco_data)
        self.assertRaises(Exception, mock_license.generate)


    @patch('license_generator_form.views.generate')
    def test_calls_license_generator_with_bad_activiti_data(
        self, mock_license
    ):
        mock_license.generate.side_effect = Exception('dictionary does contain bad data!')

        activiti_data = {
            'activiti_generate_btn': '1'
            'notes': 'some notes',
            'external_id': 'some external id',
            'external_id_type': 'salesforce',
            'tag_trial': '1',
            'tag_internal_use_only': '1',
            'tag_proof_of_concept': '1',
            'tag_extension': '1',
            'tag_perpetual': '1',
            'field_holder_name': 'Sebastian',
            'field_start_day': '18-08-2015',
            'field_number_of_admins': 5,
            'field_number_of_editors': 3,
            'field_multi_tenant': 'tru',  # Here is the bad activiti data. It should be 'true'
            'field_version': '1.0ent',
            'field_end_date': '20-08-2015',
            'field_number_of_licenses': 5,
            'field_number_of_processes': '6',  # Here another bad data. It should be a number
            'field_default_tenant': 'Seb',
            'output_filename': 'Activiti-ent50-.lic',
        }

        user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
        response = self.client.post('/generate/', activiti_data, HTTP_USER_AGENT=user_agent)

        mock_license.activiti.generate.assert_called_with(activiti_data)
        self.assertRaises(Exception, mock_license.generate)
