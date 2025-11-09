from rest_framework.viewsets import ModelViewSet

from .models import Pereval, Level, Images, Coords, User
from .serializers import PerevalSerializer, LevelSerializer, ImagesSerializer, CoordsSerializer, \
    UserSerializer


class PerevalViewSet(ModelViewSet):
    queryset = Pereval.objects.all()
    serializer_class = PerevalSerializer

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