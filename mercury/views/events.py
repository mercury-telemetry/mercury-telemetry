import csv
import json
import logging
from io import BytesIO
from zipfile import ZipFile
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import TemplateView

from ag_data.models import AGMeasurement, AGEvent, AGVenue, AGSensor
from mercury.forms import EventForm, VenueForm
from mercury.grafanaAPI.grafana_api import Grafana
from mercury.models import GFConfig
from ..event_check import require_event_code

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


def export_all_event(request):
    if request.path.__contains__("json"):
        events = AGEvent.objects.all().order_by("uuid")
        filenames = []
        for event in events:
            measurement_data = AGMeasurement.objects.filter(event_uuid=event.uuid)
            venue = AGVenue.objects.get(uuid=event.venue_uuid.uuid)
            temp = create_event_json(event, venue, measurement_data)
            json_object = json.dumps(temp)
            filename = event.name.replace(" ", "").lower()
            filenames.append(filename + ".json")
            with open(filename + ".json", "w") as outfile:
                outfile.write(json_object)
        byte_data = BytesIO()
        try:
            event_zip = ZipFile(byte_data, "w")
            for fn in filenames:
                event_zip.write(fn)
        finally:
            event_zip.close()

        response = HttpResponse(byte_data.getvalue(), content_type="application/zip")
        response["Content-Disposition"] = "attachment; filename=events.zip"
        return response
    else:
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=all_events.csv"
        events = AGEvent.objects.all().order_by("uuid")
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
        for event in events:
            measurement_data = AGMeasurement.objects.filter(event_uuid=event.uuid)
            if len(measurement_data) == 0:
                measurement_data = []
            venue = AGVenue.objects.get(uuid=event.venue_uuid.uuid)
            response = create_event_csv(
                writer, response, event, venue, measurement_data
            )
        return response


def create_event_csv(writer, response, event_object, venue_object, measurements_object):
    i = 0
    if len(measurements_object) > 0:
        sensor = AGSensor.objects.get(id=measurements_object[0].sensor_id.id)
        for measurement in measurements_object:
            i += 1
            if sensor.id != measurement.sensor_id:
                sensor = AGSensor.objects.get(id=measurement.sensor_id.id)
            writer.writerow(
                [
                    str(i),
                    event_object.name,
                    event_object.date,
                    event_object.description,
                    venue_object.name,
                    sensor.name,
                    measurement.timestamp,
                    measurement.value["reading"],
                ]
            )
    else:
        i += 1
        writer.writerow(
            [
                str(i),
                event_object.name,
                event_object.date,
                event_object.description,
                venue_object.name,
                "no data for event",
                "no data for event",
                "no data for event",
            ]
        )

    return response


def create_event_json(event_object, venue_object, measurements_object):
    event_info = {
        "name": event_object.name,
        "event date": str(event_object.date),
        "event description": event_object.description,
    }
    if venue_object:
        event_info["venue name"] = venue_object.name
        event_info["venue description"] = venue_object.description

    measurement_info = []
    if measurements_object:
        sensor = AGSensor.objects.get(id=measurements_object[0].sensor_id.id)
        for measurement in measurements_object:
            if sensor.id != measurement.sensor_id:
                sensor = AGSensor.objects.get(id=measurement.sensor_id.id)
            temp = {
                "sensor name": sensor.name,
                "timestamp": str(measurement.timestamp),
                "reading": measurement.value["reading"],
            }
            measurement_info.append(temp)

    data = {"event_info": event_info, "measurement_info": measurement_info}

    return data


def export_event(request, event_uuid=None, file_format="CSV"):
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
        venue = AGVenue.objects.get(uuid=event_to_export.venue_uuid.uuid)
        if request.path.__contains__("json"):
            data = create_event_json(event_to_export, venue, measurement_data)
            event_info = {
                "name": event_to_export.name,
                "event date": str(event_to_export.date),
                "event description": event_to_export.description,
            }
            if venue:
                event_info["venue name"] = venue.name
                event_info["venue description"] = venue.description

            measurement_info = []
            if measurement_data:
                sensor = AGSensor.objects.get(id=measurement_data[0].sensor_id.id)
                for measurement in measurement_data:
                    if sensor.id != measurement.sensor_id:
                        sensor = AGSensor.objects.get(id=measurement.sensor_id.id)
                    temp = {
                        "sensor name": sensor.name,
                        "timestamp": str(measurement.timestamp),
                        "reading": measurement.value["reading"],
                    }
                    measurement_info.append(temp)

            data = {"event_info": event_info, "measurement_info": measurement_info}

            response = HttpResponse(str(data), content_type="application/json")
            response["Content-Disposition"] = (
                'attachment; filename="' + filename + '".json'
            )
            return response
        else:
            response = HttpResponse(content_type="text/csv")
            response["Content-Disposition"] = (
                'attachment; filename="' + filename + '".csv'
            )
            if len(measurement_data) == 0:
                return redirect("/events")

            response = create_event_csv(
                response, event_to_export, venue, measurement_data
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
        active_event = {}
        if len(events) > 0:
            active_event = events[0]
        context = {
            "event_form": event_form,
            "venue_form": venue_form,
            "events": events,
            "venues": venues,
            "active_event": active_event,
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
