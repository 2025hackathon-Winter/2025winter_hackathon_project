import logging
from django.utils.deprecation import MiddlewareMixin
from app.log import log_messages

logger = logging.getLogger("remind")


# すべてのビューの前後でログを記録するミドルウェア
class LoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        #リクエストが来たときにログを記録
        logger.info(f"リクエスト受信: {request.method} {request.path}")
        log_messages()  # ここでログ関数を適用
    
    def process_response(self, request, response):
       #レスポンスを返すときにログを記録
        logger.info(f"レスポンス送信: {response.status_code}")
        return response

