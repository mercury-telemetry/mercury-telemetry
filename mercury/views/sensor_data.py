import logging
from django.http import JsonResponse
from ag_data.models import AGMeasurement

log = logging.getLogger(__name__)
log.setLevel(logging.ERROR)


def event_data_exists(request, event_uuid=None):
    """
    Checks whether measurements exist for this event_id
    Returns either { "status": False } or { "status" : True }
    """

    response = dict()

    response["status"] = (
        True
        if AGMeasurement.objects.filter(event_uuid=event_uuid).count() > 0
        else False
    )

    return JsonResponse(response)


def sensor_data_exists(request, sensor_id=None):
    """
    Checks whether measurements exist for this sensor_id
    Returns either { "status": False } or { "status" : True }
    """

    response = dict()

    response["status"] = (
        True if AGMeasurement.objects.filter(sensor_id=sensor_id).count() > 0 else False
    )

    return JsonResponse(response)
