import datetime
import logging
from collections import OrderedDict

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from mercury.can import (
    CANDecoder,
    InvalidBitException,
    MessageLengthException,
    BadInputException,
    NoMoreBitsException,
)
from mercury.can_map import CANMapper
from ..event_check import require_event_code
from ..forms import CANForm
from ..models import (
    TemperatureSensor,
    AccelerationSensor,
    WheelSpeedSensor,
    SuspensionSensor,
    FuelLevelSensor,
)

log = logging.getLogger(__name__)


class DataTooShortException(Exception):
    def __init__(self, expected, found):
        error = (
            f"The CAN Processor attempts to split the maximum 8-byte data field into four "
            f"16-bit words. For the type of sensor identified in the data, {expected} "
            f"word were expected, but only {found} were provided. Please verify the data "
            f"field being sent in the request that the length matches the requirement."
        )
        log.error(error)
        self.error = {"error": error, "words_expected": expected, "words_found": found}


def _bad_request(decoded_data, error_message, *args, **kwargs):
    """This is a helper function to return a specific error message
    including all of the data that was decoded."""
    decoded_data["data_word_0"] = decoded_data.get("data_word_0")
    decoded_data["data_word_1"] = decoded_data.get("data_word_1")
    decoded_data["data_word_2"] = decoded_data.get("data_word_2")
    decoded_data["data_word_3"] = decoded_data.get("data_word_3")

    return JsonResponse(
        OrderedDict(error=error_message, can_msg=decoded_data, **kwargs), status=400
    )


def _determine_sensor(data):
    """This helper method attempts to return the "type" of the Sensor that
    is determined by the can_id within data. If it cannot be identified, None
    is returned."""
    mapper = CANMapper(data)
    sensor = mapper.get_sensor_from_id()
    return sensor


def _create_populated_sensor(sensor, data):
    """This method returns a Sensor object of a particular type with the data in the
    proper fields based on the type of sensor. If required data is missing (because
    the CAN message data was not properly constructed, we raise a DataTooShortException
    which can be caught when this method is invoked."""
    counter = 0
    created_at = datetime.datetime.now()
    if sensor is TemperatureSensor:
        return sensor(created_at=created_at, temperature=data["data"])
    if sensor is AccelerationSensor:
        try:
            x = int(data["data_word_0"], 2)
            counter += 1
            y = int(data["data_word_1"], 2)
            counter += 1
            z = int(data["data_word_2"], 2)
        except KeyError:
            raise DataTooShortException(3, counter)
        return sensor(
            created_at=created_at, acceleration_x=x, acceleration_y=y, acceleration_z=z
        )

    if sensor is WheelSpeedSensor:
        try:
            fr = int(data["data_word_0"], 2)
            counter += 1
            fl = int(data["data_word_1"], 2)
            counter += 1
            br = int(data["data_word_2"], 2)
            counter += 1
            bl = int(data["data_word_3"], 2)
        except KeyError:
            raise DataTooShortException(4, counter)
        return sensor(
            created_at=created_at,
            wheel_speed_fr=fr,
            wheel_speed_fl=fl,
            wheel_speed_br=br,
            wheel_speed_bl=bl,
        )

    if sensor is SuspensionSensor:
        try:
            fr = int(data["data_word_0"], 2)
            counter += 1
            fl = int(data["data_word_1"], 2)
            counter += 1
            br = int(data["data_word_2"], 2)
            counter += 1
            bl = int(data["data_word_3"], 2)
        except KeyError:
            raise DataTooShortException(4, counter)

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
        log.debug("Request came from the UI")
        can_msg = request.POST.get("can_msg")
    else:
        # origin is the api
        log.debug("Request came from the API")
        if not request.body:
            msg = "Request body is empty. Please re-POST with a non-empty body."
            return _bad_request({}, msg)
        else:
            can_msg = request.body

    try:
        decoder = CANDecoder(can_msg)
    except (MessageLengthException, BadInputException) as e:
        return JsonResponse(e.error, status=400)

    try:
        decoded_data = decoder.decode_can_message()
    except (InvalidBitException, NoMoreBitsException) as e:
        return JsonResponse(e.error, status=400)

    sensor_type = _determine_sensor(decoded_data)
    if sensor_type is None:
        msg = "Unable to determine sensor based on can_id. Please check can_id value."
        return _bad_request(decoded_data, msg)

    try:
        sensor = _create_populated_sensor(sensor_type, decoded_data)
    except DataTooShortException as e:
        return _bad_request(
            decoded_data,
            e.error["error"],
            words_expected=e.error["words_expected"],
            words_found=e.error["words_found"],
        )

    log.debug("Saving a new instance of {}".format(sensor))
    sensor.save()
    return JsonResponse(dict(can_msg=decoded_data), status=201)


class CANUI(TemplateView):
    template_name = "can.html"

    @require_event_code
    def get(self, request, *args, **kwargs):
        form = CANForm()
        return render(request, "can.html", {"form": form})
