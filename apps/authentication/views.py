from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiRequest
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.api.response import base_response, error_open_api_example, base_response_with_error
from apps.authentication import codes
from apps.authentication.serializers import TokenSerializer, AccessTokenSerializer, \
    TokenVerifyResponseSerializer, TokenRefreshResponseSerializer, TokenBanResponseSerializer, RefreshTokenSerializer
from apps.authentication.services import get_token_service
from pkg.client.client import get_client_info

SCHEMA_TAGS = ("Auth / Token",)
service = get_token_service()


class TokenVerifyView(APIView):
    serializer_class = TokenSerializer

    @extend_schema(
        request=OpenApiRequest(request=serializer_class),
        responses={
            200: OpenApiResponse(response=TokenVerifyResponseSerializer),
            400: OpenApiResponse(response=serializer_class),
            401: OpenApiResponse(response=OpenApiTypes.OBJECT,
                examples=[
                    error_open_api_example(message="Invalid token", error=codes.CODE_TRANSLATION[codes.INVALID_TOKEN]),
                ]),
        },
        tags=SCHEMA_TAGS
    )
    def post(self, request):
        """
        ### Verify Token Validity

        This endpoint allows clients to check the validity of a given token (either an access token or a refresh token).
        It's useful for clients to confirm if their stored tokens are still active before making protected API calls.

        **Request Body:**
        * `token`: The token string to be validated.

        **Possible Responses:**
        * **200 OK**: The token is valid.
        * **400 Bad Request**: The request body is malformed, or the `token` field is missing/invalid.
        * **401 Unauthorized**: The token is invalid or has expired.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            service.validate_token(
                token_str=serializer.validated_data["token"], client_info=get_client_info(request=request))
            return base_response()
        except Exception as err:
            return base_response_with_error(err)


class TokenRefreshView(APIView):
    serializer_class = RefreshTokenSerializer
    serializer_class_output = AccessTokenSerializer

    @extend_schema(
        request=OpenApiRequest(request=serializer_class),
        responses={
            200: OpenApiResponse(response=TokenRefreshResponseSerializer),
            400: OpenApiResponse(response=serializer_class),
            401: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                examples=[
                    error_open_api_example(message="Invalid token", error=codes.CODE_TRANSLATION[codes.INVALID_TOKEN]),
                ]
            )
        },
        tags=SCHEMA_TAGS)
    def post(self, request):
        """
        ### Refresh Access Token

        This endpoint allows clients to obtain a new access token using a valid refresh token.
        This is crucial for maintaining user sessions without requiring them to re-authenticate frequently.
        The refresh token itself is also returned, indicating whether it was regenerated or simply reused.

        **Request Body:**
        * `token`: The refresh token string previously issued to the client.

        **Possible Responses:**
        * **200 OK**: A new access token and potentially a new refresh token are successfully issued. The response
         includes their values and the access token's expiry.
        * **400 Bad Request**: The request body is malformed, or the `token` (refresh token) field is missing, empty,
         or not a valid string.
        * **401 Unauthorized**: The refresh token is invalid, expired, revoked, or does not match server-side
         security checks (e.g., mismatched UUIDs, device name, or IP address). This also applies if the provided
          token is an access token instead of a refresh token.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            resp = service.refresh_access_token(refresh_token_str=serializer.validated_data["refresh_token"],
                                                client_info=get_client_info(request=request))
            return base_response(result=resp.__dict__, message="token refreshed")
        except Exception as err:
            return base_response_with_error(err)


class TokenBanView(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        responses={
            200: OpenApiResponse(response=TokenBanResponseSerializer),
            401: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                examples=[
                    error_open_api_example(message="Invalid token", error=codes.CODE_TRANSLATION[codes.INVALID_TOKEN]),
                ]
            )
        },
        tags=SCHEMA_TAGS)
    def get(self, request):
        """
        ### Ban User Tokens (Logout from All Devices)

        This endpoint allows an authenticated user to invalidate all their active tokens,
        effectively logging them out from all devices where they are currently logged in.
        This action revokes both access and refresh tokens associated with the user.

        **Authentication:**
        * This endpoint requires an **authenticated user**. A valid access token must be provided in the
        `Authorization` header.

        **Request Body:**
        * This endpoint does not require a request body.

        **Possible Responses:**
        * **200 OK**: The user's tokens have been successfully revoked, and they are logged out.
        * **401 Unauthorized**: The request does not contain a valid authentication token, or the
         token has already expired/is invalid.
        """
        try:
            service.ban_token(user_id=request.user.id)
            return base_response()
        except Exception as err:
            return base_response_with_error(err)
