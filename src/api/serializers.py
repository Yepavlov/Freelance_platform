from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from clients.models import ClientProfile
from core.models import City, Country, State
from freelancers.models import FreelancerProfile

User = get_user_model()


class CountrySerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = ("name",)


class StateSerializer(ModelSerializer):
    country_name = SerializerMethodField()

    class Meta:
        model = State
        fields = (
            "name",
            "country",
            "country_name",
        )

    def get_country_name(self, obj):
        return obj.country.name


class CitySerializer(ModelSerializer):
    state_name = SerializerMethodField()

    class Meta:
        model = City
        fields = (
            "name",
            "state",
            "state_name",
        )

    def get_state_name(self, obj):
        return obj.state.name


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "password",
            "is_staff",
            "phone_number",
            "user_type",
            "password",
            "re_password",
        )


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "is_staff",
            "phone_number",
            "user_type",
        )


class FreelancerProfileCreateSerializer(ModelSerializer):
    class Meta:
        model = FreelancerProfile
        fields = (
            "position",
            "description",
            "birth_date",
            "hourly_rate",
            "country",
            "state",
            "city",
            "photo",
            "sex",
            "resume",
            "skill",
        )


class FreelancerProfileSerializer(ModelSerializer):
    country_name = SerializerMethodField()
    state_name = SerializerMethodField()
    city_name = SerializerMethodField()

    class Meta:
        model = FreelancerProfile
        fields = (
            "position",
            "description",
            "birth_date",
            "hourly_rate",
            "country",
            "country_name",
            "state",
            "state_name",
            "city",
            "city_name",
            "photo",
            "sex",
            "resume",
            "skill",
            "user",
        )

    def get_country_name(self, obj):
        return obj.country.name if obj.country else None

    def get_state_name(self, obj):
        return obj.state.name if obj.state else None

    def get_city_name(self, obj):
        return obj.city.name if obj.city else None


class ClientProfileCreateSerializer(ModelSerializer):
    class Meta:
        model = ClientProfile
        fields = (
            "company",
            "company_description",
            "country",
            "state",
            "city",
            "image",
        )


class ClientProfileSerializer(ModelSerializer):
    country_name = SerializerMethodField()
    state_name = SerializerMethodField()
    city_name = SerializerMethodField()

    class Meta:
        model = ClientProfile
        fields = (
            "company",
            "company_description",
            "country",
            "country_name",
            "state",
            "state_name",
            "city",
            "city_name",
            "image",
            "user",
        )

    def get_country_name(self, obj):
        return obj.country.name if obj.country else None

    def get_state_name(self, obj):
        return obj.state.name if obj.state else None

    def get_city_name(self, obj):
        return obj.city.name if obj.city else None
