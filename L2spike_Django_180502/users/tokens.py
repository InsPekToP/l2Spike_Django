# users/tokens.py
from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from django.utils import six
from django.utils.http import base36_to_int, int_to_base36
from django.utils.crypto import constant_time_compare, salted_hmac
# from datetime import datetime, timedelta
import time

class TimedEmailTokenGenerator(PasswordResetTokenGenerator):
    timeout_seconds = 300  #На тестах 30 секунд. Можешь поставить 300 для 5 минут

    def _make_hash_value(self, user, timestamp):
        return f"{user.pk}{user.is_active}{timestamp}"

    def make_token(self, user):
        timestamp = int(time.time())
        ts_b36 = int_to_base36(timestamp)
        hash = self._make_hash_value(user, timestamp)
        hash = salted_hmac("django.email.confirm", hash).hexdigest()[::2]
        return f"{ts_b36}-{hash}"

    def check_token(self, user, token):
        if not user or not token:
            return False
        try:
            ts_b36, _hash = token.split("-")
            ts = base36_to_int(ts_b36)
        except (ValueError, IndexError):
            return False

        if (time.time() - ts) > self.timeout_seconds:
            return False

        expected_hash = salted_hmac("django.email.confirm", self._make_hash_value(user, ts)).hexdigest()[::2]
        return constant_time_compare(_hash, expected_hash)


email_token_generator = TimedEmailTokenGenerator()
