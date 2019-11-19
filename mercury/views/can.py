from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import logging
from mercury.can import CANDecoder, InvalidBitException

# logging.basicConfig(level=logging.WARNING)
log = logging.getLogger(__name__)


@csrf_exempt
def post(request, *args, **kwargs):
    if not request.body:
        """Return 400 Bad Request if no CAN message is received"""
        return HttpResponse(status=400)
    decoder = CANDecoder(request.body)
    try:
        decoded_message = decoder.decode_can_message()
        status = 201
    except InvalidBitException as e:
        decoded_message = e.error
        status = 400
    return HttpResponse(decoded_message, status=status)
