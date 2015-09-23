from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from license_generator_form.views import home_page
from license_generator_form.views import handler404, handler500
from unittest.mock import patch
from alfresco_license_generators import (
    JavaNotFoundError,
    GeneratorCommandError
)
import json


JAVA_ERROR_MESSAGE = 'Your message could not being delivered.'\
                     + ' Java not found Error message!'
GENERATOR_ERROR_MESSAGE = 'Your message could not being delivered.'\
                          + ' Generator Command Error message!'


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
        expected_404 = render_to_string('404.html')
        self.assertEqual(response.content.decode(), expected_404)
        self.assertEqual(response.status_code, 404)

    def test_internal_server_error_returns_500(self):
        request = HttpRequest()
        response = handler500(request)
        expected_505 = render_to_string('500.html')
        self.assertEqual(response.content.decode(), expected_505)
        self.assertEqual(response.status_code, 500)


class GenerateLicenseTest(TestCase):

    @patch('alfresco_license_generators.Alfresco')
    def test_bytes_returned_alfresco_license(
            self, mock_license
    ):
        mock_license.generate.return_value = (
            'Alfresco output message',
            b'Stream of bytes to receive'
        )

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

        user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.'\
            + '36\ (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
        response = self.client.post(
            '/generate/',
            alfresco_data,
            HTTP_USER_AGENT=user_agent
        )

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

        self.assertEqual(response['Content-Type'], 'application/octet-stream')
        self.assertEqual(response['Content-Length'], '26')
        self.assertIn('Alfresco-ent30-.lic', response['Content-Disposition'])
        self.assertEqual(b'Stream of bytes to receive', response.content)

    @patch('alfresco_license_generators.Activiti')
    def test_bytes_returned_activiti_license(
        self, mock_license
    ):
        mock_license.generate.return_value = (
            'Activiti output message',
            b'Stream of bytes to receive'
        )

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

        user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.'\
            + '36\ (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
        response = self.client.post(
            '/generate/',
            activiti_data,
            HTTP_USER_AGENT=user_agent
        )

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

        self.assertEqual(response['Content-Type'], 'application/octet-stream')
        self.assertEqual(response['Content-Length'], '26')
        self.assertIn('Activiti-ent50-.lic', response['Content-Disposition'])
        self.assertEqual(b'Stream of bytes to receive', response.content)

    @patch('alfresco_license_generators.Alfresco')
    def test_java_exception_raised_on_alfresco_license(
        self, mock_license
    ):

        mock_license.generate.side_effect = \
            JavaNotFoundError(JAVA_ERROR_MESSAGE)

        alfresco_data = {
            'alfresco_generate_btn': '1',
            'field_holder_name': '',
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

        user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.'\
            + '36\ (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'

        response = self.client.post(
            '/generate/',
            alfresco_data,
            HTTP_USER_AGENT=user_agent
        )

        self.assertTrue(mock_license.generate.called)
        self.assertRaises(JavaNotFoundError, mock_license.generate)
        self.assertIn(JAVA_ERROR_MESSAGE.encode('utf-8'), response.content)

    @patch('alfresco_license_generators.Activiti')
    def test_java_exception_raised_on_activiti_license(
        self, mock_license
    ):

        mock_license.generate.side_effect =\
            JavaNotFoundError(JAVA_ERROR_MESSAGE)

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
            'field_holder_name': '',
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

        user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.'\
            + '36\ (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'

        response = self.client.post(
            '/generate/',
            activiti_data,
            HTTP_USER_AGENT=user_agent
        )

        self.assertTrue(mock_license.generate.called)
        self.assertRaises(JavaNotFoundError, mock_license.generate)
        self.assertIn(JAVA_ERROR_MESSAGE.encode('utf-8'), response.content)

    @patch('alfresco_license_generators.Alfresco')
    def test_generatorcommand_exception_raised_on_alfresco_license(
        self, mock_license
    ):

        mock_license.generate.side_effect =\
            GeneratorCommandError(GENERATOR_ERROR_MESSAGE)

        alfresco_data = {
            'alfresco_generate_btn': '1',
            'field_holder_name': '',
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

        user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.'\
            + '36\ (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'

        response = self.client.post(
            '/generate/',
            alfresco_data,
            HTTP_USER_AGENT=user_agent
        )

        self.assertTrue(mock_license.generate.called)
        self.assertRaises(GeneratorCommandError, mock_license.generate)
        self.assertIn(
            GENERATOR_ERROR_MESSAGE.encode('utf-8'),
            response.content
        )

    @patch('alfresco_license_generators.Activiti')
    def test_generatorcommand_exception_raised_on_activiti_license(
        self, mock_license
    ):

        mock_license.generate.side_effect =\
            GeneratorCommandError(GENERATOR_ERROR_MESSAGE)

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
            'field_holder_name': '',
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

        user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.'\
            + '36\ (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'

        response = self.client.post(
            '/generate/',
            activiti_data,
            HTTP_USER_AGENT=user_agent
        )

        self.assertTrue(mock_license.generate.called)
        self.assertRaises(GeneratorCommandError, mock_license.generate)
        self.assertIn(
            GENERATOR_ERROR_MESSAGE.encode('utf-8'),
            response.content
        )


class RestGenerateLicenseTest(TestCase):

    @patch('alfresco_license_generators.Alfresco')
    def test_rest_bytes_returned_alfresco_license(
            self, mock_license
    ):

        mock_license.generate.return_value = (
            'Alfresco output message',
            'Stream of bytes to receive'
        )

        to_json = {
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

        alfresco_data = json.dumps(to_json)
        response = self.client.post(
            '/api/alfresco_license/',
            alfresco_data,
            'application/json'
        )

        self.assertTrue(mock_license.generate.called)
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
        self.assertEqual(2, len(mock_license.generate(alfresco_data)))
        return_values = json.loads(response.content.decode('utf-8'))
        self.assertEqual('Alfresco output message', return_values['stdout'])
        self.assertEqual('Stream of bytes to receive', return_values['binary'])

    @patch('alfresco_license_generators.Activiti')
    def test_rest_bytes_returned_activiti_license(
            self, mock_license
    ):

        mock_license.generate.return_value = (
            'Activiti output message',
            'Stream of bytes to receive'
        )

        to_json = {
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

        activiti_data = json.dumps(to_json)
        response = self.client.post(
            '/api/activiti_license/',
            activiti_data,
            'application/json'
        )

        self.assertTrue(mock_license.generate.called)
        mock_license.generate.assert_called_once_with(
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
        self.assertEqual(2, len(mock_license.generate(activiti_data)))
        return_values = json.loads(response.content.decode('utf-8'))
        self.assertEqual('Activiti output message', return_values['stdout'])
        self.assertEqual('Stream of bytes to receive', return_values['binary'])

    @patch('alfresco_license_generators.Alfresco')
    def test_rest_java_exception_raised_on_alfresco_license(
        self, mock_license
    ):

        mock_license.generate.side_effect = \
            JavaNotFoundError(JAVA_ERROR_MESSAGE)

        to_json = {
            'release_key': 'ent30',
            'field_cloud_sync': '1',
            'field_holder_name': 'Sebastian',
            'field_end_date': '17/08/2015',
            'field_heartbeat_url': 'www.alfresco.com',
            'field_ats_end_date': '17/08/2015',
            'field_max_users': 10,
            'field_no_heartbeat': '1',
            'field_license_type': 'TEAM',
            'field_cluster_enabled': '1',
            'field_max_docs': 3,
            'field_cryptodoc_enabled': '1'
        }

        alfresco_data = json.dumps(to_json)

        response = self.client.post(
            '/api/alfresco_license/',
            alfresco_data,
            'application/json'
        )

        self.assertTrue(mock_license.generate.called)
        self.assertRaises(JavaNotFoundError, mock_license.generate)
        self.assertIn(JAVA_ERROR_MESSAGE.encode('utf-8'), response.content)

    @patch('alfresco_license_generators.Activiti')
    def test_rest_java_exception_raised_on_activiti_license(
        self, mock_license
    ):

        mock_license.generate.side_effect = \
            JavaNotFoundError(JAVA_ERROR_MESSAGE)

        to_json = {
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
            'output_filename': 'Activiti-ent50-.lic'
        }

        activiti_data = json.dumps(to_json)

        response = self.client.post(
            '/api/activiti_license/',
            activiti_data,
            'application/json'
        )

        self.assertTrue(mock_license.generate.called)
        self.assertRaises(JavaNotFoundError, mock_license.generate)
        self.assertIn(JAVA_ERROR_MESSAGE.encode('utf-8'), response.content)

    @patch('alfresco_license_generators.Alfresco')
    def test_rest_generatorcommand_exception_raised_on_alfresco_license(
        self, mock_license
    ):

        mock_license.generate.side_effect = \
            GeneratorCommandError(GENERATOR_ERROR_MESSAGE)

        to_json = {
            'release_key': 'ent30',
            'field_cloud_sync': '1',
            'field_holder_name': 'Sebastian',
            'field_end_date': '17/08/2015',
            'field_heartbeat_url': 'www.alfresco.com',
            'field_ats_end_date': '17/08/2015',
            'field_max_users': 10,
            'field_no_heartbeat': '1',
            'field_license_type': 'TEAM',
            'field_cluster_enabled': '1',
            'field_max_docs': 3,
            'field_cryptodoc_enabled': '1'
        }

        alfresco_data = json.dumps(to_json)

        response = self.client.post(
            '/api/alfresco_license/',
            alfresco_data,
            'application/json'
        )

        self.assertTrue(mock_license.generate.called)
        self.assertRaises(GeneratorCommandError, mock_license.generate)
        self.assertIn(
            GENERATOR_ERROR_MESSAGE.encode('utf-8'),
            response.content
        )

    @patch('alfresco_license_generators.Activiti')
    def test_rest_generatorcommand_exception_raised_on_activiti_license(
        self, mock_license
    ):

        mock_license.generate.side_effect = \
            GeneratorCommandError(GENERATOR_ERROR_MESSAGE)

        to_json = {
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
            'output_filename': 'Activiti-ent50-.lic'
        }

        activiti_data = json.dumps(to_json)

        response = self.client.post(
            '/api/activiti_license/',
            activiti_data,
            'application/json'
        )

        self.assertTrue(mock_license.generate.called)
        self.assertRaises(GeneratorCommandError, mock_license.generate)
        self.assertIn(
            GENERATOR_ERROR_MESSAGE.encode('utf-8'),
            response.content
        )
