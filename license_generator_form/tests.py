from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from license_generator_form.views import home_page
from license_generator_form.views import handler404, handler500
from unittest.mock import patch


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

    @patch('alfresco_license_generators.Alfresco')
    def test_bytes_returned_alfresco_license(
            self, mock_license
    ):
        mock_license.generate.return_value = ('Alfresco output message', b'Stream of bytes to receive')

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
            'field_heartbeat_url': 'www.alfresco.com',
            'field_cluster_enabled': '1',
            'field_license_type': 'TEAM',
            'field_end_date': '17/08/2015',
            'field_max_docs': 3,
            'field_cloud_sync': '1',
            'field_ats_end_date': '17/08/2015',
            'field_cryptodoc_enabled': '1',
            'output_filename': 'Alfresco-ent30-.lic'
        }

        user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36\ (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
        response = self.client.post('/generate/', alfresco_data, HTTP_USER_AGENT=user_agent)

        mock_license.generate.assert_called_once_with(
            h='Sebastian',
            noheartbeat=True,
            clusterenabled=True,
            release='ent30',
            l='TEAM',
            md=3,
            heartbeaturl='www.alfresco.com',
            e="17/08/2015",
            mu=10,
            ats='17/08/2015',
            cryptodocenabled=True,
            cloudsync=True
        )

        stdout, binary = mock_license.generate(
            h='Sebastian',
            noheartbeat=True,
            clusterenabled=True,
            release='ent30',
            l='TEAM',
            md=3,
            heartbeaturl='www.alfresco.com',
            e="17/08/2015",
            mu=10,
            ats='17/08/2015',
            cryptodocenabled=True,
            cloudsync=True
        )

        self.assertEqual(
            ('Alfresco output message', b'Stream of bytes to receive'),
            (stdout, binary)
        )

        self.assertEqual(response['Content-Type'], 'application/octet-stream')
        self.assertEqual(response['Content-Length'], '26')
        self.assertIn('Alfresco-ent30-.lic', response['Content-Disposition'])

    @patch('alfresco_license_generators.Activiti')
    def test_bytes_returned_activiti_license(
        self, mock_license
    ):
        mock_license.generate.return_value = ('Activiti output message', b'Stream of bytes to receive')

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
            'field_start_date': '18/08/2015',
            'field_number_of_admins': 5,
            'field_number_of_editors': 3,
            'field_multi_tenant': 'true',
            'field_version': '1.0ent',
            'field_end_date': '20/08/2015',
            'field_number_of_licenses': 5,
            'field_number_of_processes': 6,
            'field_number_of_apps': 2,
            'field_default_tenant': 'Seb',
            'output_filename': 'Activiti-ent50-.lic',
        }

        user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
        response = self.client.post('/generate/', activiti_data, HTTP_USER_AGENT=user_agent)

        mock_license.generate.assert_called_with(
            v='1.0ent',
            multiTenant='true',
            numberOfProcesses=6,
            numberOfAdmins=5,
            defaultTenant='Seb',
            h='Sebastian',
            numberOfLicenses=5,
            numberOfEditors=3,
            numberOfApps=2,
            s='20150818',
            e='20150820'
        )

        self.assertTrue(mock_license.generate.called)

        stdout, binary = mock_license.generate(
            v='1.0ent',
            multiTenant='true',
            numberOfProcesses=6,
            numberOfAdmins=5,
            defaultTenant='Seb',
            h='Sebastian',
            numberOfLicenses=5,
            numberOfEditors=3,
            numberOfApps=2,
            s='20150818',
            e='20150820'
        )

        self.assertEqual(
            ('Activiti output message', b'Stream of bytes to receive'),
            (stdout, binary)
        )

        self.assertEqual(response['Content-Type'], 'application/octet-stream')
        self.assertEqual(response['Content-Length'], '26')
        self.assertIn('Activiti-ent50-.lic', response['Content-Disposition'])

    @patch('alfresco_license_generators.Alfresco')
    def test_exception_raised_on_alfresco_license(
        self, mock_license
    ):

        mock_license.generate.side_effect = Exception('dictionary is empty or incompleted!')

        with self.assertRaises(Exception):
            stdout, binary = mock_license.generate(
                release="ent50",
                badargument="wontwork"
            )
        self.assertTrue(mock_license.generate.called)

    @patch('alfresco_license_generators.Activiti')
    def test_exception_raised_on_activiti_license(
        self, mock_license
    ):

        mock_license.generate.side_effect = Exception('dictionary is empty or incompleted!')

        with self.assertRaises(Exception):
            stdout, binary = mock_license.generate(
                badargument="wontwork"
            )
        self.assertTrue(mock_license.generate.called)
