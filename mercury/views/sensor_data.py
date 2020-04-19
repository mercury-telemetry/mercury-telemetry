import logging
import json
from django.http import HttpResponse
from ag_data.models import AGMeasurement

log = logging.getLogger(__name__)
log.setLevel(logging.ERROR)


def get(request, sensor_id=None):
    """
    Checks whether measurements exist for this sensor_id
    Returns either { "status": False } or { "status" : True }
    answers the question, "Does measurement data exist for this sensor?"
    """

    response = dict()

    if not sensor_id:
        response["status"] = False

    response["status"] = True if AGMeasurement.objects.filter(
        sensor_id=sensor_id).count() > 0 else False

    return HttpResponse(json.dumps(response))