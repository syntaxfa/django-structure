from django.utils.translation import gettext_lazy as _

# authentication codes starts with 100

# 401_00
INVALID_TOKEN = 401_100
INVALID_REFRESH_TOKEN = 401_101
INVALID_ACCESS_TOKEN = 401_102

CODE_TRANSLATION = {
    # 401_00
    INVALID_TOKEN: _("Invalid token"),
    INVALID_REFRESH_TOKEN: _("Invalid refresh token"),
    INVALID_ACCESS_TOKEN: _("Invalid access token"),
}
