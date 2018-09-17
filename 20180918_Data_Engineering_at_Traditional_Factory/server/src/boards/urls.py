# boards/urls.py
from django.conf.urls import url

from rest_framework.urlpatterns import format_suffix_patterns

from boards.api.v1 import api_views
from boards.views import index, DashIndex, DashViewYield

urlpatterns = [
    # view
    url(r'^home/$', index, name='home'),
]

apipattern = [
    # views
    url(r'^dashboard/$', DashIndex.as_view(), name='dashboard'),

    # Option JSON
    url(r'options/dash_yield/', DashViewYield.as_view()),

    # api 
    url(r'^records/$', api_views.DataViews.as_view(), name='records_api'),
    url(r'^records/(?P<factory_id>[0-9a-f-]+)$', api_views.DataViewsDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns + apipattern)