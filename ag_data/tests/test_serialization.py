from django.test import TestCase
from django.utils.dateparse import parse_datetime
from ag_data.tests import common
from ag_data.serializers import AGEventSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import io


class AGEventAPISerializationTest(TestCase):
    def test_event_serialization(self):
        # prepare an event object
        agEvent = common.create_event(common.test_event_data["event1"])
        # serialize data
        serializer = AGEventSerializer(agEvent)
        self.assertEqual(serializer.instance.event_name, agEvent.event_name)
        self.assertEqual(serializer.instance.event_date, agEvent.event_date)
        self.assertEqual(
            serializer.instance.event_description, agEvent.event_description
        )
        # render to json
        jsonContent = JSONRenderer().render(serializer.data)
        # deserialize: parse the stream to python native
        stream = io.BytesIO(jsonContent)
        parsedData = JSONParser().parse(stream)
        self.assertEqual(parsedData["agEventName"], agEvent.event_name)
        self.assertEqual(parsedData["agEventDate"], agEvent.event_date)
        self.assertEqual(parsedData["agEventDescription"], agEvent.event_description)
        # deserialize: populate object instance
        serializer = AGEventSerializer(data=parsedData)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["event_name"], agEvent.event_name)
        self.assertEqual(
            serializer.validated_data["event_date"], parse_datetime(agEvent.event_date)
        )
        self.assertEqual(
            serializer.validated_data["event_description"], agEvent.event_description
        )
