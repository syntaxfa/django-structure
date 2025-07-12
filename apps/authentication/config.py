from dataclasses import dataclass

from django.conf import settings


@dataclass
class TokenConfig:
    prefix_user_auth_cache_key: str = "users:auths"
    user_auth_cache_exp_in_seconds: int = 86400 # one day
    access_token_lifetime: int = settings.JWT_ACCESS_TOKEN_LIFETIME_IN_SECONDS
    refresh_token_lifetime: int = settings.JWT_REFRESH_TOKEN_LIFETIME_IN_DAYS
