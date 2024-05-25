from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     RetrieveAPIView, UpdateAPIView)
from rest_framework.viewsets import ModelViewSet

from api.permissions import IsClient, IsFreelancer
from api.serializers import (CitySerializer, ClientProfileCreateSerializer,
                             ClientProfileSerializer, CountrySerializer,
                             FreelancerProfileCreateSerializer,
                             FreelancerProfileSerializer, StateSerializer)
from clients.models import ClientProfile
from core.models import City, Country, State
from freelancers.models import FreelancerProfile


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


class CreateFreelancerProfileAPIView(CreateAPIView):
    permission_classes = [IsFreelancer]
    serializer_class = FreelancerProfileCreateSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class FreelancerProfileRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsFreelancer]
    serializer_class = FreelancerProfileSerializer

    def get_object(self):
        return FreelancerProfile.objects.get(user=self.request.user)


class CreateClientProfileAPIView(CreateAPIView):
    permission_classes = [IsClient]
    serializer_class = ClientProfileCreateSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class ClientProfileRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsClient]
    serializer_class = ClientProfileSerializer

    def get_object(self):
        return ClientProfile.objects.get(user=self.request.user)
