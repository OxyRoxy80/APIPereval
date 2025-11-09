from django.db import DatabaseError
from django.forms import model_to_dict
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Pereval, Level, Images, Coords, User
from .serializers import PerevalSerializer, LevelSerializer, ImagesSerializer, CoordsSerializer, \
    UserSerializer


class PerevalViewSet(ModelViewSet):
    queryset = Pereval.objects.all()
    serializer_class = PerevalSerializer
    http_method_names = ['get', 'post', 'patch']
    filterset_fields = ['user__email']

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

    def partial_update(self, request, *args, **kwargs):
        pereval = self.get_object()
        serializer = self.get_serializer(pereval, data=request.data, partial=True)
        if pereval.status != 'new':
            return Response(
                {
                    'state': 0,
                    'message': "Обновлять можно только запись со статусом 'new'!"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        pereval_user_dict = model_to_dict(pereval.user)
        pereval_user_dict.pop('id')
        if request.data.get('user'):
            pereval_user_data = request.data.get('user')
            if pereval_user_dict != pereval_user_data:
                return Response(
                    {
                        'state': 0,
                        'message': 'Нельзя изменять данные пользователя!'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        serializer.is_valid()
        serializer.save()
        return Response(
            {
                'state': 1,
                'message': 'Запись успешно обновлена!'
            },
            status=status.HTTP_200_OK
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