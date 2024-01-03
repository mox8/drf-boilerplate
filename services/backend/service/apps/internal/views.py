from rest_framework import generics, status
from rest_framework.response import Response
from settings.celery import debug_task


class CeleryTaskDebugApiView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        debug_task.delay()
        return Response(status=status.HTTP_200_OK)
