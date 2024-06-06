import logging
from django.contrib.auth.hashers import BasePasswordHasher
from django.utils.crypto import constant_time_compare, get_random_string
from django.utils.translation import gettext_noop as _
from django.contrib.auth.hashers import make_password

logger = logging.getLogger(__name__)


class CustomHasher(BasePasswordHasher):
    algorithm = "custom"

    def encode(self, password, salt):
        reversed_password = password[::-1] + "s@lt"
        encoded_password = make_password(reversed_password, salt=salt)
        logger.debug(f"Reversed Password: {reversed_password}")
        logger.debug(f"Encoded Password: {encoded_password}")
        return encoded_password

    def verify(self, password, encoded):
        reversed_password = password[::-1] + "s@lt"
        encoded_2 = self.encode(reversed_password, encoded.split('$')[1])
        return constant_time_compare(encoded, encoded_2)

    def safe_summary(self, encoded):
        return {
            _('algorithm'): self.algorithm,
            _('salt'): encoded.split('$')[1],
            _('hash'): encoded.split('$')[2],
        }


