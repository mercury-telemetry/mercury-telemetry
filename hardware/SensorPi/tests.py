import unittest
from .utils import date_str_with_current_timezone
from datetime import datetime
import dateutil.parser


class TestUtil(unittest.TestCase):
    def test_date_str_with_current_timezone(self):
        s = date_str_with_current_timezone()
        date = dateutil.parser.isoparse(s)
        self.assertTrue("T" in s)
        self.assertAlmostEqual(date.timestamp(), datetime.now().timestamp(), places=1)
