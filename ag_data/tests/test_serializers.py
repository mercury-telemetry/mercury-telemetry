from datetime import datetime
from unittest import TestCase

from ag_data import serializers
from ag_data.models import AGSensor, AGVenue


class TestSerializers(TestCase):
    wrong_uuid = "d81cac8d-26e1-4983-a942-1922e54a943a"

    test_event_data = {
        "name": "Sunny Day Test Drive",
        "date": datetime.datetime(2020, 2, 2, 20, 21, 22),
        "description": "A very progressive test run at \
                Sunnyside Daycare's Butterfly Room.",
        "location": "New York, NY",
    }

    test_venue_data = {
        "name": "Venue 1",
        "description": "foo",
        "latitude": 100,
        "longitude": 200,
    }

    test_measurement_data = {
        "sensor_id": 1,
        "values": '{"power": 2, "speed": 1}',
        "date": "2020-03-11T19:20:00",
    }

    def setUp(self):
        AGVenue.objects.create(name=self.test_venue_data["name"],
                               description=self.test_venue_data["description"],
                               latitude=self.test_venue_data["latitude"],
                               longitude=self.test_venue_data["longitude"])
        AGSensor.objects.create(name=self.test_event_data["name"],
                                date=self.test_event_data["date"],
                                description=self.test_event_data["description"],
                                location=self.test_event_data["location"])
        event = AGSensor.objects.all().first()
        self.uuid = event.uuid

    def test_wrong_event_uuid(self):

        serializer = serializers.AGMeasurementSerializer()
