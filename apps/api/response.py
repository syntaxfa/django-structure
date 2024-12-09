from typing import Dict, Optional

from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from pkg.rich_error.error import RichError, error_code
from .codes import INTERNAL_SERVER_ERROR


def _get_code(error: Exception):
    if isinstance(error, RichError):
        return error_code(error=error)

    return INTERNAL_SERVER_ERROR


def base_response(*, status_code: int = HTTP_200_OK, result: Optional[Dict] = None) -> Response:
    return Response(data={"result": result}, status=status_code)


def base_response_with_error(*, error: Exception, code_translation: Dict) -> Response:
    code_translation[INTERNAL_SERVER_ERROR] = _("Internal server error")
    code = _get_code(error=error)
    return Response(data={"error": code_translation[code]}, status=code // 100)
