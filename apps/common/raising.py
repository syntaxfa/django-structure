from typing import Dict

from pkg.logger.logger import get_logger
from pkg.rich_error.error import get_error_info, RichError


logger = get_logger()


def raise_and_log(app: str, op: str, err: Exception, category: str, sub_category: str, meta: Dict):
    meta["error"] = get_error_info(error=err)
    rich_error = RichError(op).set_error(err)
    logger.error(app=app, msg=str(rich_error), category=category, sub_category=sub_category, meta=meta)
    raise rich_error
