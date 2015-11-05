from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from license_generator_form.views import \
    home_page, rest_generate_alfresco, rest_generate_activiti,\
    _upload_validate_request
from license_generator_form.views import handler404, handler500
from unittest.mock import patch
from alfresco_license_generators import (
    JavaNotFoundError,
    GeneratorCommandError
)
import json
from django.core.urlresolvers import reverse
import tempfile
from django.contrib.auth.models import User
from django.contrib.auth import SESSION_KEY


GENERATOR_ERROR_MESSAGE = 'Your message could not be delivered.'\
                          + ' Generator Command Error message!'

JAVA_ERROR_MESSAGE = 'Please make sure Java is installed'

GENERAL_ERROR_MESSAGE = 'Your message could not be delivered.'\
                        + ' General Error message!'

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.'\
             + '36\ (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'

UPLOAD_ERROR = "\nAn error was thrown by the license dumping "\
               + "tool. Please check the uploaded file and "\
               + "try again, or raise a ticket with ITS if "\
               + "you feel this is an error."


ALFRESCO_DATA = {
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

ACTIVITI_DATA = {
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

REST_ALFRESCO_DATA = {
    'release_key': 'ent30',
    'holder_name': 'Sebastian',
    'max_users': 10,
    'no_heartbeat': '1',
    'heartbeat_url': 'www.alfresco.com',
    'cluster_enabled': '1',
    'license_type': 'TEAM',
    'end_date': '17/08/2015',
    'max_docs': 3,
    'cloud_sync': '1',
    'ats_end_date': '17/08/2015',
    'cryptodoc_enabled': '1'
}

REST_ACTIVITI_DATA = {
    'holder_name': 'Sebastian',
    'start_date': '18/08/2015',
    'number_of_admins': 5,
    'number_of_editors': 3,
    'multi_tenant': True,
    'version': '1.0ent',
    'end_date': '20/08/2015',
    'number_of_licenses': 5,
    'number_of_processes': 6,
    'number_of_apps': 2,
    'default_tenant': 'Seb'
}


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_root_url_returns_correct_html(self):
        request = HttpRequest()
        fake_user = User.objects.create_user(
            'AnonymousUser', 'anonymous@alfresco.com', 'anonymous'
        )
        fake_user.is_anonymous = True
        request.user = fake_user
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

        response = self.client.post(
            '/generate/alfresco/',
            ALFRESCO_DATA,
            HTTP_USER_AGENT=USER_AGENT
        )

        mock_license.generate.assert_called_once_with(
            h='Sebastian',
            noheartbeat=True,
            clusterenabled=True,
            release='ent30',
            l='TEAM',
            md='3',
            heartbeaturl='www.alfresco.com',
            e="17/08/2015",
            mu='10',
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

        response = self.client.post(
            '/generate/activiti/',
            ACTIVITI_DATA,
            HTTP_USER_AGENT=USER_AGENT
        )

        mock_license.generate.assert_called_with(
            v='1.0ent',
            multiTenant=True,
            numberOfProcesses='6',
            numberOfAdmins='5',
            defaultTenant='Seb',
            h='Sebastian',
            numberOfLicenses='5',
            numberOfEditors='3',
            numberOfApps='2',
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

        response = self.client.post(
            '/generate/alfresco/',
            ALFRESCO_DATA,
            HTTP_USER_AGENT=USER_AGENT
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

        response = self.client.post(
            '/generate/activiti/',
            ACTIVITI_DATA,
            HTTP_USER_AGENT=USER_AGENT
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

        response = self.client.post(
            '/generate/alfresco/',
            ALFRESCO_DATA,
            HTTP_USER_AGENT=USER_AGENT
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

        response = self.client.post(
            '/generate/activiti/',
            ACTIVITI_DATA,
            HTTP_USER_AGENT=USER_AGENT
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

        alfresco_data = json.dumps(REST_ALFRESCO_DATA)
        response = self.client.post(
            '/api/license/alfresco/',
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
        returned_values = json.loads(response.content.decode('utf-8'))
        self.assertEqual(
            'Alfresco output message',
            returned_values['stdout']
        )
        self.assertEqual(
            'Stream of bytes to receive',
            returned_values['binary']
        )
        self.assertEqual(response.status_code, 200)

    @patch('alfresco_license_generators.Activiti')
    def test_rest_bytes_returned_activiti_license(
            self, mock_license
    ):

        mock_license.generate.return_value = (
            'Activiti output message',
            'Stream of bytes to receive'
        )

        activiti_data = json.dumps(REST_ACTIVITI_DATA)
        response = self.client.post(
            '/api/license/activiti/',
            activiti_data,
            'application/json'
        )

        self.assertTrue(mock_license.generate.called)
        mock_license.generate.assert_called_once_with(
            v='1.0ent',
            multiTenant=True,
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
        returned_values = json.loads(response.content.decode('utf-8'))
        self.assertEqual(
            'Activiti output message',
            returned_values['stdout']
        )
        self.assertEqual(
            'Stream of bytes to receive',
            returned_values['binary']
        )
        self.assertEqual(response.status_code, 200)

    @patch('alfresco_license_generators.Alfresco')
    def test_rest_java_exception_raised_on_alfresco_license(
        self, mock_license
    ):

        mock_license.generate.side_effect = \
            JavaNotFoundError(JAVA_ERROR_MESSAGE)

        alfresco_data = json.dumps(REST_ALFRESCO_DATA)

        response = self.client.post(
            '/api/license/alfresco/',
            alfresco_data,
            'application/json'
        )

        self.assertTrue(mock_license.generate.called)
        self.assertTrue(response.status_code, 500)
        self.assertRaises(JavaNotFoundError, mock_license.generate)
        self.assertIn(JAVA_ERROR_MESSAGE.encode('utf-8'), response.content)

    @patch('alfresco_license_generators.Activiti')
    def test_rest_java_exception_raised_on_activiti_license(
        self, mock_license
    ):

        mock_license.generate.side_effect = \
            JavaNotFoundError(JAVA_ERROR_MESSAGE)

        activiti_data = json.dumps(REST_ACTIVITI_DATA)

        response = self.client.post(
            '/api/license/activiti/',
            activiti_data,
            'application/json'
        )

        self.assertTrue(mock_license.generate.called)
        self.assertRaises(JavaNotFoundError, mock_license.generate)
        self.assertEqual(response.status_code, 500)
        self.assertIn(JAVA_ERROR_MESSAGE.encode('utf-8'), response.content)

    @patch('alfresco_license_generators.Alfresco')
    def test_rest_generator_command_exception_raised_on_alfresco_license(
        self, mock_license
    ):

        mock_license.generate.side_effect = \
            GeneratorCommandError(GENERATOR_ERROR_MESSAGE)

        alfresco_data = json.dumps(REST_ALFRESCO_DATA)

        response = self.client.post(
            '/api/license/alfresco/',
            alfresco_data,
            'application/json'
        )

        self.assertTrue(mock_license.generate.called)
        self.assertEqual(response.status_code, 500)
        self.assertRaises(GeneratorCommandError, mock_license.generate)
        self.assertIn(
            GENERATOR_ERROR_MESSAGE.encode('utf-8'),
            response.content
        )

    @patch('alfresco_license_generators.Activiti')
    def test_rest_generator_command_exception_raised_on_activiti_license(
        self, mock_license
    ):

        mock_license.generate.side_effect = \
            GeneratorCommandError(GENERATOR_ERROR_MESSAGE)

        activiti_data = json.dumps(REST_ACTIVITI_DATA)

        response = self.client.post(
            '/api/license/activiti/',
            activiti_data,
            'application/json'
        )

        self.assertTrue(mock_license.generate.called)
        self.assertRaises(GeneratorCommandError, mock_license.generate)
        self.assertEqual(response.status_code, 500)
        self.assertIn(
            GENERATOR_ERROR_MESSAGE.encode('utf-8'),
            response.content
        )

    def test_rest_api_page_not_found(self):

        request = HttpRequest()
        request.path = '/api/license/wrong_location/'

        response = self.client.post(
            request.path
        )

        self.assertEqual(response.status_code, 404)

    def test_rest_alfresco_license_method_not_allowed(self):

        request = HttpRequest()
        request.path = '/api/license/alfresco/'
        request.method = 'GET'

        response = rest_generate_alfresco(request)

        self.assertEqual(response.status_code, 405)

    def test_rest_activiti_license_method_not_allowed(self):

        request = HttpRequest()
        request.path = '/api/license/activiti/'
        request.method = 'GET'

        response = rest_generate_activiti(request)

        self.assertEqual(response.status_code, 405)

    def test_rest_alfresco_license_unsupported_media_file(self):

        request = HttpRequest()
        request.path = '/api/license/alfresco/'
        request.method = 'POST'
        request.META['CONTENT_TYPE'] = 'application/xml'

        response = rest_generate_alfresco(request)

        self.assertEqual(response.status_code, 415)

    def test_rest_activiti_license_unsupported_media_file(self):

        request = HttpRequest()
        request.path = '/api/license/activiti/'
        request.method = 'POST'
        request.META['CONTENT_TYPE'] = 'application/xml'

        response = rest_generate_activiti(request)

        self.assertEqual(response.status_code, 415)


class UploadLicenseTest(TestCase):

    @patch('alfresco_license_generators.Alfresco')
    def test_dump_output_returned_on_upload_alfresco_license(
        self, mock_license
    ):

        mock_license.dump.return_value = b"Alfresco license already checked"

        fake_file = tempfile.NamedTemporaryFile(delete=False)

        response = self.client.post(
            reverse('upload_alfresco_license'),
            data={
                'file': fake_file
            },
            format='multipart',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        self.assertTrue(mock_license.dump.called)
        fake_file.close()

        returned_value = json.loads(response.content.decode('utf-8'))

        self.assertEqual(
            "Alfresco license already checked", returned_value['message']
        )

    @patch('logging.error')
    @patch('alfresco_license_generators.Alfresco')
    def test_java_exception_raised_on_upload_alfresco_license(
        self, mock_license, mock_error
    ):

        mock_license.dump.side_effect = \
            JavaNotFoundError(UPLOAD_ERROR)

        fake_file = tempfile.NamedTemporaryFile(delete=False)

        response = self.client.post(
            reverse('upload_alfresco_license'),
            data={
                'file': fake_file
            },
            format='multipart',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        self.assertTrue(mock_license.dump.called)
        self.assertTrue(mock_error.called)
        self.assertRaises(JavaNotFoundError, mock_license.dump)
        fake_file.close()

        self.assertIn(UPLOAD_ERROR.encode('utf-8'), response.content)

    @patch('logging.error')
    @patch('alfresco_license_generators.Alfresco')
    def test_generatorcommand_exception_raised_on_upload_alfresco_license(
        self, mock_license, mock_error
    ):

        mock_license.dump.side_effect = \
            GeneratorCommandError(UPLOAD_ERROR)

        fake_file = tempfile.NamedTemporaryFile(delete=False)

        response = self.client.post(
            reverse('upload_alfresco_license'),
            data={
                'file': fake_file
            },
            format='multipart',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        self.assertTrue(mock_license.dump.called)
        self.assertTrue(mock_error.called)
        self.assertRaises(GeneratorCommandError, mock_license.dump)
        fake_file.close()

        self.assertIn(UPLOAD_ERROR.encode('utf-8'), response.content)

    @patch('alfresco_license_generators.Activiti')
    def test_dump_output_returned_on_upload_activiti_license(
        self, mock_license
    ):
        mock_license.dump.return_value = b"Activiti license already checked"

        fake_file = tempfile.NamedTemporaryFile(delete=False)

        response = self.client.post(
            reverse('upload_activiti_license'),
            data={
                'file': fake_file
            },
            format='multipart',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        self.assertTrue(mock_license.dump.called)
        fake_file.close()

        returned_value = json.loads(response.content.decode('utf-8'))

        self.assertEqual(
            "Activiti license already checked", returned_value['message']
        )

    @patch('logging.error')
    @patch('alfresco_license_generators.Activiti')
    def test_java_exception_raised_on_upload_activiti_license(
        self, mock_license, mock_error
    ):

        mock_license.dump.side_effect = \
            JavaNotFoundError(UPLOAD_ERROR)

        fake_file = tempfile.NamedTemporaryFile(delete=False)

        response = self.client.post(
            reverse('upload_activiti_license'),
            data={
                'file': fake_file
            },
            format='multipart',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        self.assertTrue(mock_license.dump.called)
        self.assertTrue(mock_error.called)
        self.assertRaises(JavaNotFoundError, mock_license.dump)
        fake_file.close()

        self.assertIn(UPLOAD_ERROR.encode('utf-8'), response.content)

    @patch('logging.error')
    @patch('alfresco_license_generators.Activiti')
    def test_generatorcommand_exception_raised_on_upload_activiti_license(
        self, mock_license, mock_error
    ):

        mock_license.dump.side_effect = \
            GeneratorCommandError(UPLOAD_ERROR)

        fake_file = tempfile.NamedTemporaryFile(delete=False)

        response = self.client.post(
            reverse('upload_activiti_license'),
            data={
                'file': fake_file
            },
            format='multipart',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        self.assertTrue(mock_license.dump.called)
        self.assertTrue(mock_error.called)
        self.assertRaises(GeneratorCommandError, mock_license.dump)
        fake_file.close()

        self.assertIn(UPLOAD_ERROR.encode('utf-8'), response.content)

    def test_upload_license_method_not_allowed(self):

        request = HttpRequest()
        request.path = reverse('upload_alfresco_license')
        request.method = 'GET'
        request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'

        response = _upload_validate_request(request)

        self.assertEqual(response.status_code, 405)

    def test_upload_license_method_not_allowed_ajax(self):

        request = HttpRequest()
        request.path = reverse('upload_alfresco_license')
        request.method = 'POST'
        request.META['HTTP_X_REQUESTED_WITH'] = 'NO_AJAX'

        response = _upload_validate_request(request)

        self.assertEqual(response.status_code, 405)


class LoginPageTest(TestCase):

    @patch('license_generator_form.views.authenticate')
    def test_calls_authenticate_with_data_from_post(
        self, mock_authenticate
    ):
        mock_authenticate.return_value = None
        self.client.post(
            '/login/',
            {'username': 'assert username', 'password': 'assert password'}
        )
        mock_authenticate.assert_called_once_with(
            username='assert username',
            password='assert password'
        )

    @patch('license_generator_form.views.authenticate')
    def test_gets_logged_in_session_authenticate_returns_a_user(
        self, mock_authenticate
    ):
        user = User.objects.create(username='username', password='password')
        user.backend = ''
        mock_authenticate.return_value = user
        self.client.post(
            '/login/', {'username': 'username', 'password': 'password'}
        )
        self.assertEqual(int(self.client.session[SESSION_KEY]), user.pk)

    @patch('license_generator_form.views.authenticate')
    def test_does_not_get_logged_in_if_authenticate_returns_None(
        self, mock_authenticate
    ):
        mock_authenticate.return_value = None
        self.client.post(
            '/login/', {'username': 'username', 'password': 'password'}
        )
        self.assertNotIn(SESSION_KEY, self.client.session)
