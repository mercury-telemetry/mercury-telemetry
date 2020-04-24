from ag_data.models import ErrorLog
from django.utils import timezone
import uuid

ERROR_CODE = {
    "UNKNOWN_FMT": "UNKNOWN_FORMAT",
    "MISSING_COL": "MISSING_COLUMN",
    "MISSING_FIELD_IN_RAW": "MISSING_FIELD_IN_RAW_READING",
    "INVALID_COL_NM": "INVALID_COLUMN_NAME",
    "INVALID_COL_VL": "INVALID_COLUMN_VALUE",
    "INVALID_FIELD_IN_RAW": "INVALID_FIELD_IN_RAW_READING",
    "ERROR_F_PROC_MMT": "FORMULA_PROCESS_MEASUREMENT_ERROR",
    "EXTRA_KEYVAL_IN_MMT": "EXTRANEOUS_KEY_VALUE_PAIR_IN_MEASUREMENT",
    "NO_ACT_EVENT":"NO_ACTIVE_EVENT",
    "OTHER": "OTHER_ERROR",
}


def error_record(raw_data, error_code, error_description):
    """Function take raw_data, error_code, error_description as input and 
    store these information in error_log table
    """
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
