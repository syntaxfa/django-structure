from django.utils.translation import gettext_lazy as _

from apps.api.response import base_response_with_error

# 404_00
POST_NOT_FOUND = 404_00

CODE_TRANSLATION = {
    # 404_00
    POST_NOT_FOUND: _("This post does not exists"),
}


def response_with_error(err: Exception):
    return base_response_with_error(error=err, code_translation=CODE_TRANSLATION)
