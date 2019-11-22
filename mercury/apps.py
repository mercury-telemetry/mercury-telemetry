from django.apps import AppConfig
from django.db.utils import OperationalError


class MercuryConfig(AppConfig):
    name = "mercury"

    def ready(self):
        try:
            from .models import EventCodeAccess

            for code in EventCodeAccess.objects.all():
                if code.event_code == "testcode":
                    code.delete()
            test_code = EventCodeAccess(event_code="testcode", enabled=True)
            test_code.save()
        except OperationalError:
            pass
