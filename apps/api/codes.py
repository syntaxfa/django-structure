from django.utils.translation import gettext_lazy as _

from apps.example.codes import CODE_TRANSLATION as EXAMPLE_CODE_TRANSLATION

# 200_000
OK = 200_000
CREATED = 201_000
# 500_000
INTERNAL_SERVER_ERROR = 500_000

CODE_TRANSLATION = {
    OK: _("OK"),
    CREATED: _("Created"),
    INTERNAL_SERVER_ERROR: _("Internal Server Error"),
    **EXAMPLE_CODE_TRANSLATION, # example codes starts with 000
}
