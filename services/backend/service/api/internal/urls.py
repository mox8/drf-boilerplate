from django.urls import path

from apps.internal.views import CeleryTaskDebugApiView

urlpatterns = [
    path('debug-celery/', CeleryTaskDebugApiView.as_view()),
]
