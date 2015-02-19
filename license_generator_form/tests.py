from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest

from license_generator_form.views import generator_selection

class RootURLTest(TestCase):
	def test_root_url_resolves_to_generator_selection_view(self):
		found = resolve('/')
		self.assertEqual(found.func, generator_selection)

	def test_root_url_returns_correct_html(self):
		request = HttpRequest()
		response = generator_selection(request)
		self.assertTrue(response.content.startswith(b'<html>'))
		self.assertIn(b'<title>License Generator</title>', response.content)
		self.assertTrue(response.content.endswith(b'</html>'))