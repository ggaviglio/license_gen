from django.core.urlresolvers import resolve
from django.test import TestCase
from license_generator_form.views import generator_selection

class RootURLTest(TestCase):
	def test_root_url_resolves_to_generator_selection_view(self):
		found = resolve('/')
		self.assertEqual(found.func, generator_selection)