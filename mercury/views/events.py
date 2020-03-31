import csv
import logging

from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import TemplateView
from ..event_check import require_event_code
from mercury.forms import EventForm, VenueForm
from ag_data.models import AGMeasurement, AGEvent, AGVenue, AGSensor
from django.contrib import messages
from mercury.grafanaAPI.grafana_api import Grafana
from mercury.models import GFConfig

log = logging.getLogger(__name__)
log.setLevel(logging.ERROR)


def update_venue(request, venue_uuid=None):
    venue_to_update = AGVenue.objects.get(uuid=venue_uuid)
    if venue_to_update:
        venue_to_update.name = request.POST.get("name")
        venue_to_update.description = request.POST.get("description")
        venue_to_update.latitude = request.POST.get("latitude")
        venue_to_update.longitude = request.POST.get("longitude")
        venue_to_update.save()

    return redirect("/events")


def update_event(request, event_uuid=None):
    event_to_update = AGEvent.objects.get(uuid=event_uuid)
    if event_to_update:
        event_to_update.name = request.POST.get("name")
        post_event_location_id = request.POST.get("venue_uuid")
        venue_object = AGVenue.objects.get(uuid=post_event_location_id)
        event_to_update.venue_uuid = venue_object
        event_to_update.description = request.POST.get("description")
        event_to_update.save()

    return redirect("/events")


def delete_event(request, event_uuid=None):
    event_to_delete = AGEvent.objects.get(uuid=event_uuid)
    event_to_delete.delete()
    return redirect("/events")


def export_event(request, event_uuid=None):
    event_to_export = AGEvent.objects.get(uuid=event_uuid)
    if event_to_export:
        response = HttpResponse(content_type="text/csv")
        filename = event_to_export.name.replace(" ", "").lower()
        response["Content-Disposition"] = 'attachment; filename="' + filename + '".csv'
        measurement_data = AGMeasurement.objects.filter(event_uuid=event_uuid)
        if len(measurement_data) == 0:
            return redirect("/events")
        writer = csv.writer(response)
        writer.writerow(
            [
                "S.No",
                "Event Name",
                "Event Date",
                "Event Description",
                "Venue Name",
                "Sensor Name",
                "Sensor Data TimeStamp",
                "Sensor Value",
            ]
        )
        i = 0
        venue = AGVenue.objects.get(uuid=event_to_export.venue_uuid.uuid)
        sensor = AGSensor.objects.get(id=measurement_data[0].sensor_id.id)
        for measurement in measurement_data:
            i += 1
            if sensor.id != measurement.sensor_id:
                sensor = AGSensor.objects.get(id=measurement.sensor_id.id)
            writer.writerow(
                [
                    str(i),
                    event_to_export.name,
                    event_to_export.date,
                    event_to_export.description,
                    venue.name,
                    sensor.name,
                    measurement.timestamp,
                    measurement.value["reading"],
                ]
            )
        return response
    else:
        return redirect("/events")


class CreateEventsView(TemplateView):
    """This is the view for creating a new event."""

    template_name = "events.html"

    @require_event_code
    def get(self, request, *args, **kwargs):
        events = AGEvent.objects.all().order_by("uuid")
        venues = AGVenue.objects.all().order_by("uuid")
        event_form = EventForm()
        venue_form = VenueForm()
        context = {
            "event_form": event_form,
            "venue_form": venue_form,
            "events": events,
            "venues": venues,
        }
        return render(request, self.template_name, context)

    @require_event_code
    def post(self, request, *args, **kwargs):
        if "submit-venue" in request.POST:
            post_venue_name = request.POST.get("name")
            post_venue_description = request.POST.get("description")
            post_venue_longitude = request.POST.get("longitude")
            post_venue_latitude = request.POST.get("latitude")
            venue_data = AGVenue(
                name=post_venue_name,
                description=post_venue_description,
                longitude=post_venue_longitude,
                latitude=post_venue_latitude,
            )
            venue_data.save()
        if "submit-event" in request.POST:
            post_event_name = request.POST.get("name")
            post_event_location_id = request.POST.get("venue_uuid")
            venue_object = AGVenue.objects.get(uuid=post_event_location_id)
            post_event_date = request.POST.get("date")
            post_event_description = request.POST.get("description")
            event_data = AGEvent(
                name=post_event_name,
                venue_uuid=venue_object,
                date=post_event_date,
                description=post_event_description,
            )

            event_data.save()

            gfconfig = GFConfig.objects.filter(gf_current=True)

            # only create an event dashboard if a current gfconfig exists
            if gfconfig.count() > 0:
                dashboard = None
                # create a dashboard with the same name as the event
                config = gfconfig[0]
                try:
                    grafana = Grafana(config)
                    dashboard = grafana.create_dashboard(post_event_name)
                except ValueError as error:
                    # pass any failure message from the API to the UI
                    messages.error(
                        request,
                        f"Grafana dashboard for this event was not "
                        f"created: {error}",
                    )

                # if a dashboard was created successfully, add panels to it
                if dashboard:
                    # create a panel for each sensor
                    sensors = AGSensor.objects.all()
                    for sensor in sensors:
                        try:
                            grafana.add_panel(sensor, event_data)
                        except ValueError as error:
                            # pass any error messages from the API to the UI
                            messages.error(request, error)

        events = AGEvent.objects.all().order_by("uuid")
        venues = AGVenue.objects.all().order_by("uuid")
        event_form = EventForm()
        venue_form = VenueForm()
        context = {
            "event_form": event_form,
            "venue_form": venue_form,
            "events": events,
            "venues": venues,
        }
        return render(request, self.template_name, context)
