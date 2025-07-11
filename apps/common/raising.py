from typing import Dict

from pkg.logger.logger import get_logger


logger = get_logger()


def err_log(app: str, err: Exception, category: str, sub_category: str, meta: Dict) -> None:
    logger.error(app=app, msg=str(err), category=category, sub_category=sub_category, meta=meta)
