from django.utils.translation import gettext_lazy as _

from apps.authentication.codes import CODE_TRANSLATION as AUTHENTICATION_CODE_TRANSLATION

# 200_000
OK = 200_000
CREATED = 201_000
# 500_000
INTERNAL_SERVER_ERROR = 500_000

CODE_TRANSLATION = {
    OK: _("OK"),
    CREATED: _("Created"),
    INTERNAL_SERVER_ERROR: _("Internal Server Error"),
    **AUTHENTICATION_CODE_TRANSLATION, # authentication code starts with 100
}
