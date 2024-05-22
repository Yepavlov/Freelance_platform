from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from core.models import City, Country, State


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
