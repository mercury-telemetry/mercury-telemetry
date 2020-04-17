import datetime
import uuid
import json

from django.test import TestCase

from rest_framework import serializers
from ag_data.models import AGSensor, AGVenue, AGMeasurement, AGEvent, AGSensorType
from ag_data.serializers import AGMeasurementSerializer


class TestSerializers(TestCase):
    test_event_data = {
        "name": "Sunny Day Test Drive",
        "date": "2020-04-17T12:12:16.102657",
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

    test_sensor_type_data = {
        "name": "temperature",
        "processing_formula": 1,
        "format": {1: 1},
    }

    test_sensor_data = {"name": "temperature", "type_id": 1}

    test_measurement_data = {
        "value": {"power": 2, "speed": 1},
        "timestamp": "2020-04-17T12:12:16.102657"
    }

    def setUp(self):
        AGVenue.objects.create(
            name=self.test_venue_data["name"],
            description=self.test_venue_data["description"],
            latitude=self.test_venue_data["latitude"],
            longitude=self.test_venue_data["longitude"],
        )
        AGEvent.objects.create(
            name=self.test_event_data["name"],
            date=self.test_event_data["date"],
            description=self.test_event_data["description"],
            venue_uuid=AGVenue.objects.all().first(),
        )
        AGSensorType.objects.create(
            name=self.test_sensor_type_data["name"],
            processing_formula=self.test_sensor_type_data["processing_formula"],
            format=self.test_sensor_type_data["format"],
        )
        AGSensor.objects.create(
            name=self.test_sensor_data["name"],
            type_id=AGSensorType.objects.all().first(),
        )

        self.uuid = AGEvent.objects.all().first().uuid
        self.sensor_id = AGSensor.objects.all().first().id
        self.data = self.test_measurement_data.copy()

    def test_wrong_event_uuid(self):
        self.data["event_uuid"] = uuid.uuid4()
        self.data["sensor_id"] = self.sensor_id
        serializer = AGMeasurementSerializer(data=self.data)

        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError:
            self.assertEqual(len(serializer.errors), 1)
            self.assertTrue("event_uuid" in serializer.errors)

    def test_wrong_sensor_id(self):
        self.data = self.test_measurement_data
        self.data["event_uuid"] = self.uuid
        self.data["sensor_id"] = 0
        serializer = AGMeasurementSerializer(data=self.data)

        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError:
            self.assertEqual(len(serializer.errors), 1)
            self.assertTrue("sensor_id", serializer.errors)

    def test_create_measurement_successfully_JSON_String(self):
        self.data["event_uuid"] = str(self.uuid)
        self.data["sensor_id"] = self.sensor_id
        self.data["value"] = '{"power": 2, "speed": 1}'
        serializer = AGMeasurementSerializer(data=self.data)

        try:
            # self.assertTrue(serializer.is_valid())
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except serializers.ValidationError:
            pass

        measurements = AGMeasurement.objects.all()
        self.assertTrue(measurements.count() > 0)

        measurement = measurements.first()
        self.assertEqual(measurement.value, self.test_measurement_data["value"])
        self.assertEqual(measurement.event_uuid.uuid, self.uuid)
        self.assertEqual(measurement.sensor_id.id, self.sensor_id)
        self.assertEqual(measurement.timestamp.isoformat(), self.test_measurement_data["timestamp"])

    def test_create_measurement_successfully_JSON_dict(self):
        self.data["sensor_id"] = self.sensor_id
        self.data["event_uuid"] = self.uuid
        serializer = AGMeasurementSerializer(data=self.data)

        try:
            # self.assertTrue(serializer.is_valid())
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except serializers.ValidationError:
            pass

        measurements = AGMeasurement.objects.all()
        self.assertTrue(measurements.count() > 0)

        measurement = measurements.first()
        self.assertEqual(measurement.value, self.test_measurement_data["value"])
        self.assertEqual(measurement.event_uuid.uuid, self.uuid)
        self.assertEqual(measurement.sensor_id.id, self.sensor_id)
        self.assertEqual(measurement.timestamp.isoformat(), self.test_measurement_data["timestamp"])

    def test_create_measurement_JSON_binary(self):
        self.data["sensor_id"] = self.sensor_id
        self.data["event_uuid"] = str(self.uuid)
        self.data["value"] = json.dumps(self.data["value"]).encode("utf-8")

        serializer = AGMeasurementSerializer(data=self.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        measurements = AGMeasurement.objects.all()
        self.assertTrue(measurements.count() > 0)

        measurement = measurements.first()
        self.assertEqual(measurement.value, self.test_measurement_data["value"])
        self.assertEqual(measurement.event_uuid.uuid, self.uuid)
        self.assertEqual(measurement.sensor_id.id, self.sensor_id)
        self.assertEqual(measurement.timestamp.isoformat(), self.test_measurement_data["timestamp"])
