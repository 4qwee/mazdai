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
    url(r'^ajax/get-moves-list/$', 'mazdai_app.views.get_moves_list', name = 'get_moves_list'),
    url(r'^ajax/get-credits-list/$', 'mazdai_app.views.get_credits_list', name = 'get_credits_list'),
    url(r'^ajax/get-orders-list/$', 'mazdai_app.views.get_orders_list', name = 'get_orders_list'),
    url(r'^ajax/get-refills-list/$', 'mazdai_app.views.get_refills_list', name = 'get_refills_list'),
    url(r'^ajax/get-refunds-list/$', 'mazdai_app.views.get_refunds_list', name = 'get_refunds_list'),
    url(r'^sales/$', 'mazdai_app.views.sales', name='sales'),
    url(r'^moves/$', 'mazdai_app.views.moves', name='moves'),
    url(r'^credits/$', 'mazdai_app.views.credits', name='credits'),
    url(r'^credits/tool/$', 'mazdai_app.views.credits_tool', name='credits_tool'),
    url(r'^orders/$', 'mazdai_app.views.orders', name='orders'),
    url(r'^orders/tool/$', 'mazdai_app.views.orders_tool', name='orders_tool'),
    url(r'^refills/$', 'mazdai_app.views.refills', name='refills'),
    url(r'^refunds/$', 'mazdai_app.views.refunds', name='refunds'),
    url(r'^report/$', 'mazdai_app.views.report', name='report'),
    url(r'^$', 'mazdai_app.views.default'),
)