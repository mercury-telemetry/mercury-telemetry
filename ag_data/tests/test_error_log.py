from django.test import TestCase
import datetime

from ag_data.models import ErrorLog

class TestErrorLogModels(TestCase):
    test_error_log_data = {
        "missing_error":{
            "error_timestamp": datetime.datetime(2020, 4, 17, 13, 17, 00),
            "error_code": "MISSING_COLUMN",
            "error_description": "Seneor_id Column Missing",
            "error_raw_data": r'{"date":"2020-04-15 02:25:13.880456","values": {"temperature":"35.56126022338867"}}',
        },

        "invalid_error":{
            "error_timestamp": datetime.datetime(2020, 4, 17, 14, 24, 00),
            "error_code": "INVALID_COLUMN_VALUE",
            "error_description": "Sensor_id 100 Invalid",
            "error_raw_data": r'{date":"2020-03-01 02:25:13.112234","sensor_id":"100","values": {"temperature":"35.56126022338867"}}',
        },
    }

    def setUp(self):
        for error in self.test_error_log_data.keys():
            ErrorLog.objects.create(
                error_timestamp = self.test_error_log_data[error]["error_timestamp"],
                error_code = self.test_error_log_data[error]["error_code"],
                error_description = self.test_error_log_data[error]["error_description"],
                error_raw_data = self.test_error_log_data[error]["error_raw_data"]
            )
    
    def test_error_log_table(self):
        for error in self.test_error_log_data.keys():
            foo = ErrorLog.objects.get(error_timestamp=self.test_error_log_data[error]["error_timestamp"])
            self.assertEqual(foo.error_timestamp, self.test_error_log_data[error]["error_timestamp"])
            self.assertEqual(foo.error_code, self.test_error_log_data[error]["error_code"])
            self.assertEqual(foo.error_description, self.test_error_log_data[error]["error_description"])
            self.assertEqual(foo.error_raw_data, self.test_error_log_data[error]["error_raw_data"])