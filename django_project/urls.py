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
            r'^generate/$',
            'license_generator_form.views.generate_license',
            name='generate_license'
        ),
    url(
            r'^api/alfresco_license/$',
            'license_generator_form.views.rest_generate_alfresco_license',
            name='rest_generate_alfresco_license'
        ),
    url(
            r'^api/activiti_license/$',
            'license_generator_form.views.rest_generate_activiti_license',
            name='rest_generate_activiti_license'
        ),

    url(r'^admin/', include(admin.site.urls)),
)
