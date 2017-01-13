# -*- coding: utf-8 -*-
"""REST API URLs"""


from django.conf.urls import url, include

from rpc import views

urlpatterns = [
    url(r'^', views.jsonrpc),
]
