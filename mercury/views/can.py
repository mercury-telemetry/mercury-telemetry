from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
import logging
from mercury.can import (
    CANDecoder,
    InvalidBitException,
    MessageLengthException,
    BadInputException,
    NoMoreBitsException,
)
from mercury.can_map import CANMapper
from ..forms import CANForm
from django.shortcuts import render
import json
import datetime
from ..models import (
    TemperatureSensor,
    AccelerationSensor,
    WheelSpeedSensor,
    SuspensionSensor,
    FuelLevelSensor,
)


logging.basicConfig(level=logging.WARNING)
log = logging.getLogger(__name__)


def create_and_save_sensor(data):
    mapper = CANMapper(data)
    sensor = mapper.get_sensor_from_id()
    if sensor is None:
        return None
    created_at = datetime.datetime.now()
    if sensor is TemperatureSensor:
        return sensor(created_at=created_at, temperature=data["data"])
    if sensor is AccelerationSensor:
        x = int(data["data_word_0"], 2)
        y = int(data["data_word_1"], 2)
        z = int(data["data_word_2"], 2)
        return sensor(
            created_at=created_at, acceleration_x=x, acceleration_y=y, acceleration_z=z
        )
    if sensor is WheelSpeedSensor:
        fr = int(data["data_word_0"], 2)
        fl = int(data["data_word_1"], 2)
        br = int(data["data_word_2"], 2)
        bl = int(data["data_word_3"], 2)
        return sensor(
            created_at=created_at,
            wheel_speed_fr=fr,
            wheel_speed_fl=fl,
            wheel_speed_br=br,
            wheel_speed_bl=bl,
        )
    if sensor is SuspensionSensor:
        fr = int(data["data_word_0"], 2)
        fl = int(data["data_word_1"], 2)
        br = int(data["data_word_2"], 2)
        bl = int(data["data_word_3"], 2)
        return sensor(
            created_at=created_at,
            suspension_fr=fr,
            suspension_fl=fl,
            suspension_br=br,
            suspension_bl=bl,
        )
    if sensor is FuelLevelSensor:
        return sensor(created_at=created_at, current_fuel_level=data["data"])


@csrf_exempt
def post(request, *args, **kwargs):
    if "can_msg" in request.POST:
        # origin is the ui
        can_msg = request.POST.get("can_msg")
    else:
        # origin is the api
        if not request.body:
            return HttpResponse(
                json.dumps({"error": "Request body is empty"}), status=400
            )
        can_msg = request.body
    try:
        decoder = CANDecoder(can_msg)
    except (MessageLengthException, BadInputException) as e:
        return HttpResponse(json.dumps(e.error), status=400)

    try:
        decoded_data = decoder.decode_can_message()
    except (InvalidBitException, NoMoreBitsException) as e:
        return HttpResponse(json.dumps(e.error), status=400)

    try:
        sensor = create_and_save_sensor(decoded_data)
    except (KeyError, TypeError):
        return HttpResponse(
            json.dumps(
                {
                    "error": "Necessary data for the CAN ID type you "
                    "specified was missing. The data was probably too short."
                }
            ),
            status=400,
        )
    log.debug("Saving a new instance of {}".format(sensor))
    sensor.save()
    return HttpResponse(json.dumps(decoded_data), status=201)


class CANUI(TemplateView):
    template_name = "can.html"

    def get(self, request, *args, **kwargs):
        form = CANForm()
        if request.session.get("event_code_active") and request.session.get(
            "event_code_known"
        ):
            return render(request, "can.html", {"form": form})
        else:
            return render(
                request,
                "login.html",
                context={
                    "no_session_message": (
                        "You do not appear to have an "
                        "active session. Please login again."
                    )
                },
            )
