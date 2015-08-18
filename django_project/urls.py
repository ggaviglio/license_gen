from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'license_generator_form.views.home_page', name='site_root'),
    url(r'^generate/$', 'license_generator_form.views.generate_license', name='generate_license'),
    #
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
