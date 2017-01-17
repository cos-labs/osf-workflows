# -*- coding: utf-8 -*-
"""REST API URLs"""


from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_nested import routers

from api import views
from workflow.routers import router, operation_router


urlpatterns = format_suffix_patterns([
    url(r'^$', views.api_root),
    url(r'^', include(router.urls)),
    url(r'^', include(operation_router.urls)),
])
