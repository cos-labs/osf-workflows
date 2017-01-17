# -*- coding: utf-8 -*-
"""REST API URLs"""


from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_nested import routers

from workflow import views

router = routers.SimpleRouter(trailing_slash=False)

router.register(r'workflows', views.Workflow)
router.register(r'operations', views.Operation)
router.register(r'values', views.Value)
router.register(r'messages', views.Message)
router.register(r'contexts', views.Context)
router.register(r'services', views.Service)
router.register(r'resources', views.Resource)
router.register(r'roles', views.Role)
router.register(r'users', views.User)
router.register(r'groups', views.Group)


operation_router = routers.NestedSimpleRouter(router, r'operations', lookup='operation')
operation_router.register(r'prerequisites', views.Operation, base_name='task-prerequisite')
