from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from license_generator_form.views import home_page
from license_generator_form.views import handler404


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
