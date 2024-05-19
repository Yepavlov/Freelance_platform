from core.models import City, Country, State


def sample_country(country_name: str):
    country_instance, created = Country.objects.get_or_create(name=country_name)
    return country_instance


def sample_state(country_name: str, state_name: str, **params):
    country_instance = sample_country(country_name)
    default = {"country": country_instance}
    default.update(params)
    state_instance, created = State.objects.get_or_create(name=state_name, **default)
    return state_instance


def sample_city(country_name: str, state_name: str, city_name: str, **params):
    state_instance = sample_state(country_name, state_name)
    default = {"state": state_instance}
    default.update(params)
    city_instance, created = City.objects.get_or_create(name=city_name, **default)
    return city_instance
