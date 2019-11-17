from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import logging
from ..can_decoder import decode_can_message

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


@csrf_exempt
def post(request, *args, **kwargs):
    if not request.body:
        """Return 400 Bad Request if no CAN message is received"""
        return HttpResponse(status=400)
    log.debug(request.body)
    log.debug(dir(request.body))
    decoded_message = decode_can_message(request.body)
    return HttpResponse(decoded_message, status=201)
