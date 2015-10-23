from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns(
    '',
    # Examples:
    url(
            r'^$',
            'license_generator_form.views.home_page',
            name='site_root'
        ),
    url(
            r'^generate/alfresco/$',
            'license_generator_form.views.form_generate_alfresco',
            name='form_generate_alfresco'
        ),
    url(
            r'^generate/activiti/$',
            'license_generator_form.views.form_generate_activiti',
            name='form_generate_activiti'
        ),
    url(
            r'^api/license/alfresco/$',
            'license_generator_form.views.rest_generate_alfresco',
            name='rest_generate_alfresco'
        ),
    url(
            r'^api/license/activiti/$',
            'license_generator_form.views.rest_generate_activiti',
            name='rest_generate_activiti'
        ),
)
