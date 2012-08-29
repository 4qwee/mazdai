from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mazdai.views.home', name='home'),
    # url(r'^mazdai/', include('mazdai.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ajax/get-positions-list/$', 'mazdai_app.views.get_positions_list', name = 'get_positions_list'),
    url(r'^ajax/get-sales-list/$', 'mazdai_app.views.get_sales_list', name = 'get_sales_list'),
    url(r'^sales/report/$', 'mazdai_app.views.sales_report', name='sales_report'),
    url(r'^sales/$', 'mazdai_app.views.sales', name='sales'),
    url(r'^$', 'mazdai_app.views.default'),
)
