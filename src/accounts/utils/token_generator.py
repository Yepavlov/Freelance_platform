from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user: get_user_model(), timestamp):
        return text_type(user.uuid) + text_type(timestamp) + text_type(user.is_active)
