from typing import Dict, Optional

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from drf_spectacular.utils import OpenApiExample

from pkg.rich_error.error import RichError, error_code
from apps.api.codes import INTERNAL_SERVER_ERROR, CODE_TRANSLATION


def _get_code(error: Exception):
    if isinstance(error, RichError):
        return error_code(error=error)

    return INTERNAL_SERVER_ERROR


def base_response(*, status_code: int = HTTP_200_OK, result: Optional[Dict] = None,
                  message: Optional[str] = None) -> Response:
    return Response(
        data={
            "result": result,
            "message": message},
        status=status_code)


def base_response_with_error(error: Exception) -> Response:
    code = _get_code(error=error)
    return Response(data={"error": CODE_TRANSLATION[code]}, status=code // 1000)


def error_open_api_example(message: str, error: str) -> OpenApiExample:
    return OpenApiExample(
        name=message,
        value={"error": error}
    )
