from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     RetrieveAPIView, UpdateAPIView)
from rest_framework.viewsets import ModelViewSet

from api.serializers import CitySerializer, CountrySerializer, StateSerializer
from core.models import City, Country, State


class CountryViewSet(ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class StateCreateAPIView(CreateAPIView):
    serializer_class = StateSerializer


class StateUpdateAPIView(UpdateAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer


class StateRetrieveAPIView(RetrieveAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer


class StateDestroyAPIView(DestroyAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer


class CityViewSet(ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
