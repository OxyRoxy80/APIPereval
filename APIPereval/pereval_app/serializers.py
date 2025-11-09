from rest_framework import serializers

from drf_writable_nested.serializers import WritableNestedModelSerializer

from pereval_app.models import Coords, User, Level, Images, Pereval


class UserSerializer(WritableNestedModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'fam', 'name', 'otc', 'phone')


class CoordsSerializer(WritableNestedModelSerializer):
    class Meta:
        model = Coords
        fields = ('latitude', 'longitude', 'height')


class LevelSerializer(WritableNestedModelSerializer):
    class Meta:
        model = Level
        fields = ('winter', 'summer', 'autumn', 'spring')


class ImagesSerializer(WritableNestedModelSerializer):
    class Meta:
        model = Images
        fields = ('data', 'title')


class PerevalSerializer(WritableNestedModelSerializer):
    user = UserSerializer()
    coords = CoordsSerializer()
    level = LevelSerializer()
    images = ImagesSerializer(many=True)
    status = serializers.CharField(read_only=True)
    class Meta:
        model = Pereval
        fields = (
            'beauty_title', 'title', 'other_titles', 'connect', 'add_time',
            'user', 'coords', 'level', 'status', 'images'
        )
