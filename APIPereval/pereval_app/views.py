from django.db import DatabaseError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Pereval, Level, Images, Coords, User
from .serializers import PerevalSerializer, LevelSerializer, ImagesSerializer, CoordsSerializer, \
    UserSerializer

class PerevalViewSet(ModelViewSet):
    queryset = Pereval.objects.all()
    serializer_class = PerevalSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            if not serializer.is_valid():
                return Response(
                    {
                        "status": 400,
                        "message": serializer.errors,
                        "id": None
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer.save()
            return Response(
                {
                    "status": 200,
                    "message": None,
                    "id": serializer.instance.id
                }
            )
        except DatabaseError:
            return Response(
                {
                    "status": 500,
                    "message": "Ошибка подключения к базе данных",
                    "id": None
                }
            )

class LevelViewSet(ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer

class ImageViewSet(ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer

class CoordsViewSet(ModelViewSet):
    queryset = Coords.objects.all()
    serializer_class = CoordsSerializer

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer