from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
import logging
from mercury.can import CANDecoder, InvalidBitException, MessageLengthException
from ..forms import CANForm
from django.shortcuts import render
import json


logging.basicConfig(level=logging.WARNING)
log = logging.getLogger(__name__)


@csrf_exempt
def post(request, *args, **kwargs):
    if "can_msg" in request.POST:
        # origin is the ui
        can_msg = request.POST.get("can_msg")
    else:
        # origin is the api
        if not request.body:
            """Return 400 Bad Request if no CAN message is received"""
            return HttpResponse(status=400)
        can_msg = request.body
    try:
        decoder = CANDecoder(can_msg)
    except MessageLengthException as e:
        return HttpResponse(e.error, status=400)

    try:
        sensor_type, decoded_data = decoder.decode_can_message_full_dict()
        return HttpResponse(json.dumps(decoded_data), status=201)
    except InvalidBitException as e:
        return HttpResponse(e.error, status=400)
    except NotImplementedError as e:
        return HttpResponse(e.args, status=400)


class CANUI(TemplateView):
    template_name = "can.html"

    def get(self, request, *args, **kwargs):
        form = CANForm()
        return render(request, "can.html", {"form": form})
