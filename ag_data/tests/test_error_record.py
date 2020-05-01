from django.test import TestCase

from ag_data.error_record import record
from ag_data.models import ErrorLog


class TestErrorRecord(TestCase):
    test_data = {
        "error_code": "UNKNOWN_FORMAT",
        "description": "Data Format Unknown",
        "raw_data": r'{{{{{{{"""date":"2020-04-15 02:25:13.880456","values": {"temperature":"35.56126022338867"}}',
    }

    def setUp(self):
        record.save_error(
            raw_data=self.test_data["raw_data"],
            error_code=self.test_data["error_code"],
            error_description=self.test_data["description"],
        )

    def test_save(self):
        foo = ErrorLog.objects.first()
        self.assertEqual(foo.error_code, self.test_data["error_code"])
        self.assertEqual(foo.description, self.test_data["description"])
        self.assertEqual(foo.raw_data, self.test_data["raw_data"])
