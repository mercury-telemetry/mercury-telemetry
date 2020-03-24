import csv
import logging

from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import TemplateView
from ..event_check import require_event_code
from mercury.forms import EventForm, VenueForm
from ag_data.models import AGMeasurement, AGEvent, AGVenue, AGSensor
from mercury.resources import MeasurementResource

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
        event_to_update.date = request.POST.get("date")
        event_to_update.description = request.POST.get("description")
        event_to_update.save()

    return redirect("/events")


def delete_event(request, event_uuid=None):
    event_to_delete = AGEvent.objects.get(uuid=event_uuid)
    event_to_delete.delete()
    return redirect("/events")


def export_event_two(request, event_uuid=None):
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


def export_event(request, event_uuid=None):
    event_to_export = MeasurementResource()
    file_format = "CSV"
    dataset = event_to_export.export()
    if file_format == "CSV":
        response = HttpResponse(dataset.csv, content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="events.csv"'
        return response
    elif file_format == "JSON":
        response = HttpResponse(dataset.json, content_type="application/json")
        response["Content-Disposition"] = 'attachment; filename="exported_data.json"'
        return response
    elif file_format == "XLS (Excel)":
        response = HttpResponse(dataset.xls, content_type="application/vnd.ms-excel")
        response["Content-Disposition"] = 'attachment; filename="exported_data.xls"'
        return response

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
