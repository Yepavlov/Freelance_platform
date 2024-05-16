from core.models import City, Country, State


def sample_country(country_name: str):
    return Country.objects.create(
        name=country_name,
    )


def sample_state(country_name: str, state_name: str, **params):
    country_instance = sample_country(country_name)
    default = {"country": country_instance}
    default.update(params)
    return State.objects.create(name=state_name, **default)


def sample_city(country_name: str, state_name: str, city_name: str, **params):
    state_instance = sample_state(country_name, state_name)
    default = {"state": state_instance}
    default.update(params)
    return City.objects.create(name=city_name, **default)
