from django.db import models


class GFConfig(models.Model):
    """
    Grafana configs
    """

    gf_name = models.CharField(max_length=64)
    gf_host = models.CharField(max_length=128)
    gf_token = models.CharField(max_length=256, blank=True)
    gf_username = models.CharField(max_length=128, blank=True)
    gf_password = models.CharField(max_length=128, blank=True)
    gf_dashboard_uid = models.CharField(max_length=64)
    gf_db_host = models.CharField(max_length=128)
    gf_db_name = models.CharField(max_length=64)
    gf_db_username = models.CharField(max_length=64)
    gf_db_pw = models.CharField(max_length=256)
    gf_current = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.gf_host


class EventCodeAccess(models.Model):
    """This model stores the information about events. When an event is
    ongoing, if a new event_code is added and the enabled property is
    True, then use of the Telemetry app will be restricted to those
    that know the event_code."""

    event_code = models.CharField(max_length=8)
    enabled = models.BooleanField()

    def __str__(self):  # pragma: no cover
        return EventCodeAccess.__name__
