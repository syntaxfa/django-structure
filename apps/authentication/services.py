import uuid
from functools import cache

from django.contrib.auth import get_user_model
from django.core.cache import cache as django_cache
from django.utils.timezone import now
from rest_framework_simplejwt.tokens import RefreshToken, Token, AccessToken, UntypedToken

from apps.authentication.config import TokenConfig
from apps.authentication.models import UserAuth
from apps.authentication.param import GenerateTokenResponse
from apps.authentication import codes, constants
from apps.common.raising import err_log
from pkg.client.client import ClientInfo
from pkg.rich_error.error import RichError


class TokenService:
    Op = "authentication.services.TokenService."
    User = get_user_model()

    def __init__(self, config: TokenConfig):
        self.cfg = config

    @staticmethod
    def check_user_auth_is_exist(user_id: int) -> bool:
        return UserAuth.objects.filter(user_id=user_id).exists()

    @staticmethod
    def create_user_auth(user_id: int) -> UserAuth:
        return UserAuth.objects.create(user_id=user_id, access_uuid=uuid.uuid4(), refresh_uuid=uuid.uuid4())

    @staticmethod
    def get_user_auth_by_user_id(user_id: int) -> UserAuth:
        return UserAuth.objects.get(user_id=user_id)

    @staticmethod
    def update_user_auth_access_uuid(user_id: int) -> int:
        return UserAuth.objects.filter(user_id=user_id).update(access_uuid=uuid.uuid4())

    @staticmethod
    def update_user_auth_refresh_uuid(user_id: int) -> int:
        """
        If we update refresh uuid, also we need to update access uuid.
        """
        return UserAuth.objects.filter(user_id=user_id).update(refresh_uuid=uuid.uuid4(), access_uuid=uuid.uuid4())

    def _get_user_auth_cache_key(self, user_id: int) -> str:
        return f"{self.cfg.prefix_user_auth_cache_key}:{user_id}"

    def get_user_auth(self, user_id: int) -> UserAuth:
        key = self._get_user_auth_cache_key(user_id=user_id)

        user_auth = django_cache.get(key=key)
        if not user_auth:
            if not self.check_user_auth_is_exist(user_id=user_id):
                user_auth = self.create_user_auth(user_id=user_id)
            else:
                user_auth = self.get_user_auth_by_user_id(user_id=user_id)
            django_cache.set(key=key, value=user_auth, timeout=self.cfg.user_auth_cache_exp_in_seconds)

        return user_auth

    def generate_token(self, user: User, client_info: ClientInfo) -> GenerateTokenResponse:
        meta = {"user_id": user.id}

        try:
            user_auth = self.get_user_auth(user_id=user.id)

            refresh: Token = RefreshToken.for_user(user=user)
            refresh[constants.IP_ADDRESS] = client_info.ip_address
            refresh[constants.DEVICE_NAME] = client_info.device_name

            access: AccessToken = refresh.access_token

            refresh["uuid"] = str(user_auth.refresh_uuid)
            access["uuid"] = str(user_auth.access_uuid)

            return GenerateTokenResponse(
                refresh_token=str(refresh),
                access_token=str(access),
                expired_at=self.cfg.access_token_lifetime,
            )
        except Exception as err:
            err_log(constants.APP_NAME, err, constants.AUTH_SERVICE,
                    constants.AUTH_SERVICE_GENERATE_TOKEN, meta=meta)
            raise err

    def _validate_refresh_token(self, token: Token, client_info: ClientInfo) -> None:
        op = self.Op + "_validate_refresh_token"
        meta = {"client_info": client_info.__dict__}

        user_auth = self.get_user_auth(user_id=token["user_id"])
        if str(user_auth.refresh_uuid) != token["uuid"]:
            raise (RichError(op).set_msg("refresh token uuid don't math with user auth uuid").
                   set_code(codes.INVALID_REFRESH_TOKEN)).set_meta(meta)

        if token["device_name"] != client_info.device_name:
            raise (RichError(op).set_msg("refresh token device name don't match with request device name").
                   set_code(codes.INVALID_REFRESH_TOKEN)).set_meta(meta)

    def _validate_access_token(self, token: Token, client_info: ClientInfo) -> None:
        op = self.Op + "_validate_access_token"
        meta = {"client_info": client_info.__dict__}

        user_auth = self.get_user_auth(user_id=token["user_id"])
        if str(user_auth.access_uuid) != token["uuid"]:
            raise (RichError(op).set_msg("access token uuid don't math with user auth uuid").
                   set_code(codes.INVALID_ACCESS_TOKEN)).set_meta(meta)

        if token["device_name"] != client_info.device_name or token["ip_address"] != client_info.ip_address:
            raise RichError(op).set_msg("access token device name or ip don't match with request info").set_meta(meta)

    def validate_token(self, token_str: str, client_info: ClientInfo) -> Token:
        op = self.Op + "validate_token"
        meta = {"token_str": token_str, "client_info": client_info.__dict__}

        try:
            try:
                token = UntypedToken(token=token_str)
            except Exception as err:
                raise RichError(op).set_error(err).set_msg("untyped token is not valid").set_code(codes.INVALID_TOKEN)

            if token["token_type"] == "refresh":
                self._validate_refresh_token(token=token, client_info=client_info)
            elif token["token_type"] == "access":
                self._validate_access_token(token=token, client_info=client_info)

            return token
        except Exception as err:
            err_log(constants.APP_NAME, err, constants.AUTH_SERVICE,
                    constants.AUTH_SERVICE_VALIDATE_TOKEN, meta=meta)
            raise err

    def get_user_id_from_token(self, token_str: str) -> str:
        op = self.Op + "get_user_id_from_token"
        meta = {"token": token_str}

        try:
            try:
                token = UntypedToken(token=token_str)
            except Exception as err:
                raise RichError(op).set_error(err).set_msg("untyped token is not valid").set_code(codes.INVALID_TOKEN)

            return token["user_id"]
        except Exception as err:
            err_log(constants.APP_NAME, err, constants.AUTH_SERVICE,
                    constants.AUTH_SERVICE_GET_USER_ID_FROM_TOKEN, meta=meta)
            raise err

    def refresh_access_token(self, refresh_token_str: str, client_info: ClientInfo) -> GenerateTokenResponse:
        op = self.Op + "refresh_access_token"
        meta = {"refresh_token_str": refresh_token_str, "client_info": client_info.__dict__}

        try:
            token = self.validate_token(token_str=refresh_token_str, client_info=client_info)
            if token["token_type"] != "refresh":
                raise RichError(op).set_msg("token type is not refresh token").set_code(codes.INVALID_REFRESH_TOKEN)

            user = self.User.objects.get(id=token["user_id"])
            user.last_login = now()
            user.save()

            token = self.generate_token(user=user, client_info=client_info)

            return token
        except Exception as err:
            err_log(constants.APP_NAME, err, constants.AUTH_SERVICE,
                    constants.AUTH_SERVICE_REFRESH_ACCESS_TOKEN, meta=meta)
            raise err

    def ban_token(self, user_id: int) -> None:
        self.update_user_auth_refresh_uuid(user_id=user_id)

        django_cache.delete(key=self._get_user_auth_cache_key(user_id=user_id))

    def update_access_token_uuid(self, user_id: int) -> None:
        self.update_user_auth_access_uuid(user_id=user_id)


@cache
def get_token_service():
    return TokenService(
        config=TokenConfig(),
    )
