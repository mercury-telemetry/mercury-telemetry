from ag_data.models import ErrorLog
from django.utils import timezone
import uuid

def error_record(raw_data, error_code, error_description):
    assert error_code is not None
    assert error_description is not None
    assert raw_data is not None

    uuid = uuid.uuid4()
    time = timezone.now()

    return isinstance(ErrorLog.objects.create(
        uuid = uuid,
        timestamp = time,
        error_code = error_code,
        description = error_description,
        raw_data = raw_data
    ), ErrorLog)
