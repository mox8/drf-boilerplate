from rest_framework import generics, status
from rest_framework.response import Response


class PostWithSimpleResponseAPIView(generics.CreateAPIView):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return self.build_response(serializer)

    def build_response(self, serializer):
        return Response({'status': 'OK'}, status=status.HTTP_200_OK)
