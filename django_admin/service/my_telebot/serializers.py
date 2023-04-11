from rest_framework import serializers
from my_telebot.models import Spots, User, Cities


class SpotsSerializers(serializers.ModelSerializer):
    city_name = serializers.CharField(source='city.name')

    class Meta:
        model = Spots
        fields = '__all__'


class UserSerializers(serializers.ModelSerializer):
    city_name = serializers.CharField(source='city.name')

    class Meta:
        model = User
        fields = '__all__'


class CitySerializers(serializers.ModelSerializer):
    class Meta:
        model = Cities
        fields = '__all__'
