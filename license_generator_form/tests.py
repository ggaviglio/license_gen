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

    @patch('license_generator_form.views.license_generator')
    def test_calls_license_generator_with_good_alfresco_data(
            self, mock_license
    ):
        mock_license.return_value = None

        alfresco_data = {
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
            'output_filename': 'Alfresco-ent50-.lic',
        }

        self.client.post('/generate/', {'alfresco-data': alfresco_data})
        mock_license.assert_called_once_with({'alfresco-data': alfresco_data})

    @patch('license_generator_form.views.license_generator')
    def test_calls_license_generator_with_good_activiti_data(
        self, mock_license
    ):
        mock_license.return_value = None

        activiti_data = {
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

        self.client.post('/generate/', {'activiti-data': activiti_data})
        mock_license.assert_called_once_with({'activiti-data': activiti_data})

    @patch('license_generator_form.views.license_generator')
    def test_calls_license_generator_with_no_alfresco_data(
        self, mock_license
    ):
        mock_license.return_value = None
        alfresco_data = {}
        response = self.client.post('/generate/', {'no-data-alfresco': alfresco_data})
        expected_error = "There is no alfresco data to deal with"
        self.assertContains(response, expected_error)

    @patch('license_generator_form.views.license_generator')
    def test_calls_license_generator_with_no_activiti_data(
        self, mock_license
    ):
        mock_license.return_value = None
        activiti_data = {}
        response = self.client.post('/generate/', {'no-activiti-data': activiti_data})
        expected_error = "There is no activiti data to deal with"
        self.assertContains(response, expected_error)

    @patch('license_generator_form.views.license_generator')
    def test_calls_license_generator_with_bad_alfresco_data(
            self, mock_license
    ):
        mock_license.return_value = None

        alfresco_data = {
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

        response = self.client.post('/generate/', {'bad-alfresco-data': alfresco_data})
        expected_error = "BAD DATA!?"
        self.assertContains(response, expected_error)

    @patch('license_generator_form.views.license_generator')
    def test_calls_license_generator_with_bad_activiti_data(
        self, mock_license
    ):
        mock_license.return_value = None

        activiti_data = {
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

        response = self.client.post('/generate/', {'bad-activiti-data': activiti_data})
        expected_error = "BAD DATA!?"
        self.assertContains(response, expected_error)
