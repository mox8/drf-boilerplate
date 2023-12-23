from rest_framework import generics, status
from rest_framework.response import Response

from libs.drf.serializers import ObjectsCountsSerializer


class ObjectsCountsApiView(generics.ListAPIView):
    pagination_class = None
    serializer_class = ObjectsCountsSerializer

    def get_queryset(self):
        raise NotImplementedError


class PostWithSimpleResponseAPIView(generics.CreateAPIView):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return self.build_response(serializer)

    def build_response(self, serializer):
        return Response({'status': 'OK'}, status=status.HTTP_200_OK)
