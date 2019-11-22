from django.apps import AppConfig


class MercuryConfig(AppConfig):
    name = "mercury"

    def ready(self):
        from .models import EventCodeAccess

        for code in EventCodeAccess.objects.all():
            if code.event_code == "testcode":
                code.delete()
        test_code = EventCodeAccess(event_code="testcode", enabled=True)
        test_code.save()
