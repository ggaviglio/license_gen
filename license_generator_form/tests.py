from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from license_generator_form.views import generator_selection


class RootURLTest(TestCase):
    def test_root_url_resolves_to_generator_selection_view(self):
        found = resolve('/')
        self.assertEqual(found.func, generator_selection)

    def test_root_url_returns_correct_html(self):
        request = HttpRequest()
        response = generator_selection(request)
        expected_html = render_to_string('web_form.html')
        self.assertEqual(response.content.decode(), expected_html)
