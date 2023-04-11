from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.viewsets import ReadOnlyModelViewSet

from my_telebot.models import Spots, User, Cities
from my_telebot.serializers import SpotsSerializers, UserSerializers, CitySerializers
from rest_framework.response import Response
from rest_framework import viewsets, generics, permissions


class SpotsView(generics.ListAPIView):
    serializer_class = SpotsSerializers

    def get_queryset(self):
        queryset = Spots.objects.all().order_by('name')
        city_id = self.request.query_params.get('city_id', None)
        if city_id is not None:
            queryset = queryset.filter(city=city_id)
            return queryset
        return queryset

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)



class UserView(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = User.objects.all()
    serializer_class = UserSerializers


class CityView(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Cities.objects.all().order_by('name')
    serializer_class = CitySerializers
