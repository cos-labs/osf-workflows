# -*- coding: utf-8 -*-
"""REST API URLs"""


from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_nested import routers

from api import views


router = routers.SimpleRouter(trailing_slash=False)

router.register(r'workflows', views.Workflow)
router.register(r'tasks', views.Task)
router.register(r'submissions', views.Submission)
router.register(r'assignments', views.Assignment)
router.register(r'roles', views.Role)
router.register(r'users', views.User)


task_router = routers.NestedSimpleRouter(router, r'tasks', lookup='task')
task_router.register(r'prerequisites', views.Task, base_name='task-prerequisite')

urlpatterns = format_suffix_patterns([
    url(r'^$',views.api_root),
    url(r'^', include(router.urls)),
    url(r'^', include(task_router.urls)),
    url(r'^tasks/(?P<pk>[^/.]+)/relationships/(?P<related_field>[^/.]+)/$', views.TaskRelationship.as_view(), name='task-relationships')
])
