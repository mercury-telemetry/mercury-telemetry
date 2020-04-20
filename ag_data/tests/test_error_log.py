from django.test import TestCase
import datetime
import uuid
from ag_data.models import ErrorLog


class TestErrorLogModels(TestCase):
    test_error_log_data = {
        "unknown_format": {
            "uuid": "",
            "timestamp": datetime.datetime(2020, 4, 18, 14, 44, 00),
            "error_code": "UNKNOWN_FORMAT",
            "description": "Data Format Unknown",
            "raw_data": r'{{{{{{{"""date":"2020-04-15 02:25:13.880456","values": {"temperature":"35.56126022338867"}}',
        },
        "missing_error": {
            "uuid": "",
            "timestamp": datetime.datetime(2020, 4, 17, 13, 17, 00),
            "error_code": "MISSING_COLUMN",
            "description": "Seneor_id Column Missing",
            "raw_data": r'{"date":"2020-04-15 02:25:13.880456","values": {"temperature":"35.56126022338867"}}',
        },
        "invalid_error": {
            "uuid": "",
            "timestamp": datetime.datetime(2020, 4, 17, 14, 24, 00),
            "error_code": "INVALID_COLUMN_VALUE",
            "description": "Sensor_id 100 Invalid",
            "raw_data": r'{date":"2020-03-01 02:25:13.112234","sensor_id":"100",\
                            "values": {"temperature":"35.56126022338867"}}',
        },
        "formula_process_error": {
            "uuid": "",
            "timestamp": datetime.datetime(2020, 4, 18, 15, 12, 00),
            "error_code": "FORMULA_PROCESS_MEASUREMENT_ERROR",
            "description": "Formula 4 Parameter Error",
            "raw_data": r'{"Formula":"dual_temperature_sensor","Parameter":{"internal":"unknown", external:"2"} }',
        },
        "extra_key_value_in_measurement": {
            "uuid": "",
            "timestamp": datetime.datetime(2020, 4, 18, 16, 21, 00),
            "error_code": "EXTRANEOUS_KEY_VALUE_PAIR_IN_MEASUREMENT",
            "description": "Extraneous Key-Value Pair In Measurement Received By API",
            "raw_data": r'{date":"2020-03-01 02:25:13.112234","sensor_id":"100",\
                            "values": {"temperature":"35.56126022338867"}, "sensor_type": "speed_sensor"}',
        },
        "other": {
            "uuid": "",
            "timestamp": datetime.datetime(2020, 4, 18, 14, 53, 00),
            "error_code": "OTHER_ERROR",
            "description": "Invalid or Missing Event Code",
            "raw_data": r'{"Event Code": "0xffff"}',
        },
    }

    def setUp(self):
        for error in self.test_error_log_data.keys():
            self.test_error_log_data[error]["uuid"] = uuid.uuid4()
            ErrorLog.objects.create(
                uuid=self.test_error_log_data[error]["uuid"],
                timestamp=self.test_error_log_data[error]["timestamp"],
                error_code=self.test_error_log_data[error]["error_code"],
                description=self.test_error_log_data[error]["description"],
                raw_data=self.test_error_log_data[error]["raw_data"],
            )

    def test_error_log_table(self):
        for error in self.test_error_log_data.keys():
            foo = ErrorLog.objects.get(uuid=self.test_error_log_data[error]["uuid"])
            self.assertEqual(foo.uuid, self.test_error_log_data[error]["uuid"])
            self.assertEqual(
                foo.timestamp, self.test_error_log_data[error]["timestamp"]
            )
            self.assertEqual(
                foo.error_code, self.test_error_log_data[error]["error_code"]
            )
            self.assertEqual(
                foo.description, self.test_error_log_data[error]["description"]
            )
            self.assertEqual(foo.raw_data, self.test_error_log_data[error]["raw_data"])
