# -*- coding: utf-8 -*-
"""REST API URLs"""


from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_nested import routers

from workflow import views

router = routers.SimpleRouter(trailing_slash=False)

router.register(r'nets', views.Net)
router.register(r'transitions', views.Transition)
router.register(r'locations', views.Location)
router.register(r'messages', views.Message)
router.register(r'cases', views.Case)
router.register(r'users', views.User)
router.register(r'groups', views.Group)
router.register(r'tokens', views.Token)
router.register(r'arcs', views.Arc)


#transition_router = routers.NestedSimpleRouter(router, r'transitions', lookup='transition')
#transition_router.register(r'prerequisites', views.transitions, base_name='task-prerequisite')
