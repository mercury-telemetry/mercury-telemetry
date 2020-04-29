from django.test import TestCase

from ag_data.models import AGActiveEvent
from ag_data.models import AGEvent
from ag_data.models import AGVenue
import datetime


class TestSingleRecord(TestCase):
    test_venue_data = {
        "name": "Venue 1",
        "description": "foo",
        "latitude": 100,
        "longitude": 200,
    }

    test_event_data_1 = {
        "name": "Sunny Day Test Drive",
        "date": datetime.datetime(2020, 2, 2, 20, 21, 22),
        "description": "A very progressive test run at \
                            Sunnyside Daycare's Butterfly Room.",
        "location": "New York, NY",
    }

    test_event_data_2 = {
        "name": "Winter Day Test Drive",
        "date": datetime.datetime(2018, 2, 2, 20, 21, 22),
        "description": "Test run at \
                                Sunnyside Daycare's Butterfly Room.",
        "location": "New York, NY",
    }

    test_active_event_data_1 = {
        "agevent": {
            "name": "Sunny Day Test Drive",
            "date": datetime.datetime(2020, 2, 2, 20, 21, 22),
            "description": "A very progressive test run at \
                                Sunnyside Daycare's Butterfly Room.",
            "location": "New York, NY",
        }
    }

    test_active_event_data_2 = {
        "agevent": {
            "name": "Winter Day Test Drive",
            "date": datetime.datetime(2018, 2, 2, 20, 21, 22),
            "description": "Test run at \
                                    Sunnyside Daycare's Butterfly Room.",
            "location": "New York, NY",
        }
    }

    def test_replace(self):
        venue = AGVenue.objects.create(
            name=self.test_venue_data["name"],
            description=self.test_venue_data["description"],
            latitude=self.test_venue_data["latitude"],
            longitude=self.test_venue_data["longitude"],
        )
        venue.save()

        event = AGEvent.objects.create(
            name=self.test_event_data_1["name"],
            date=self.test_event_data_1["date"],
            description=self.test_event_data_1["description"],
            venue_uuid=venue,
        )
        event.save()

        foo_event = AGEvent.objects.first()

        event2 = AGEvent.objects.create(
            name=self.test_event_data_2["name"],
            date=self.test_event_data_2["date"],
            description=self.test_event_data_2["description"],
            venue_uuid=venue,
        )
        event2.save()

        active_event = AGActiveEvent.objects.create(agevent=event,)
        active_event.save()

        foo_venue = AGVenue.objects.first()

        # Check the basic save functionality
        self.assertEqual(foo_venue.name, self.test_venue_data["name"])
        self.assertEqual(foo_venue.description, self.test_venue_data["description"])
        self.assertEqual(foo_venue.latitude, self.test_venue_data["latitude"])
        self.assertEqual(foo_venue.longitude, self.test_venue_data["longitude"])

        self.assertEqual(foo_event.name, self.test_event_data_1["name"])
        self.assertEqual(foo_event.date, self.test_event_data_1["date"])
        self.assertEqual(foo_event.description, self.test_event_data_1["description"])

        self.assertEqual(AGActiveEvent.objects.first(), active_event)
        objs = AGEvent.objects.all()
        self.assertEqual(2, len(objs))

        test_active_event = AGActiveEvent.objects.create(agevent=event2,)
        test_active_event.save()

        # check later
        self.assertEqual(1, len(AGActiveEvent.objects.all()))
        self.assertEqual(AGActiveEvent.objects.first(), test_active_event)
