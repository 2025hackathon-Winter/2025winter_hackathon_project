# myapp/log.py
import logging

logger = logging.getLogger(__name__)

def log_messages():
    logger.debug("デバッグ情報")
    logger.info("情報メッセージ")
    logger.warning("警告メッセージ")
    logger.error("エラーメッセージ")
    logger.critical("致命的エラー")
