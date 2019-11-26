from django.apps import AppConfig


class MercuryConfig(AppConfig):
    name = "mercury"

    def ready(self):
        """This block is a Django hook that runs when the app is ready. It is
        designed to be used during the "testing sprint" since there was a
        requirement that the acccount (event code in our case) could
        survive a system restart and database reset. This entire method
        should be removed when it is no longer needed. The bare except block
        protects the app from failing when running manage.py commands to
        make and use DB migration files."""
        try:
            from .models import EventCodeAccess

            for code in EventCodeAccess.objects.all():
                if code.event_code == "testcode":
                    code.delete()
            test_code = EventCodeAccess(event_code="testcode", enabled=True)
            test_code.save()
        except:  # noqa E722 # pragma: no cover
            pass
