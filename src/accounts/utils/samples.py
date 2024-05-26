from django.contrib.auth import get_user_model


def sample_user(
    email: str, first_name: str, last_name: str, is_staff: bool, is_active: bool, user_type: int, **params
) -> get_user_model():
    default = {
        "password": "some_password1",
        "phone_number": "+15305667788",
    }
    default.update(params)
    return get_user_model().objects.create(
        email=email,
        first_name=first_name,
        last_name=last_name,
        is_staff=is_staff,
        is_active=is_active,
        user_type=user_type,
        **default,
    )
