import csv
import json
import logging
import os
from io import BytesIO
from zipfile import ZipFile
from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import TemplateView

from ag_data.models import AGMeasurement, AGEvent, AGVenue, AGSensor, AGActiveEvent
from mercury.forms import EventForm, VenueForm
from mercury.grafanaAPI.grafana_api import Grafana
from mercury.models import GFConfig
from ..event_check import require_event_code, require_event_code_function

log = logging.getLogger(__name__)
log.setLevel(logging.ERROR)

GITHUB_DOCS_ROOT = settings.GITHUB_DOCS_ROOT
CONFIGURE_EVENTS_HELP_DOC = "configure_events.md"

@require_event_code_function
def update_venue(request, venue_uuid=None):
    venue_to_update = AGVenue.objects.get(uuid=venue_uuid)
    if venue_to_update:
        venue_to_update.name = request.POST.get("name")
        venue_to_update.description = request.POST.get("description")
        venue_to_update.latitude = request.POST.get("latitude")
        venue_to_update.longitude = request.POST.get("longitude")
        venue_to_update.save()

    return redirect("/events")


@require_event_code_function
def update_event(request, event_uuid=None):
    event_to_update = AGEvent.objects.get(uuid=event_uuid)
    if event_to_update:
        new_name = request.POST.get("name")
        new_venue_id = request.POST.get("venue_uuid")
        new_venue_object = AGVenue.objects.get(uuid=new_venue_id)
        new_description = request.POST.get("description")

        # if the name was changed, update all Grafana dashboards with new name
        if new_name != event_to_update.name:
            gfconfigs = GFConfig.objects.all()

            for gfconfig in gfconfigs:

                # Grafana instance using current GFConfig
                grafana = Grafana(gfconfig)

                try:
                    dashboard = grafana.update_dashboard_title(
                        event_to_update, new_name
                    )
                    if dashboard:
                        messages.success(
                            request,
                            f"{gfconfig.gf_name}: Grafana " f"dashboard title updated",
                        )
                except ValueError as error:
                    messages.error(
                        request,
                        f"{gfconfig.gf_name}: Grafana dashboard "
                        f"title not updated: {error} ",
                    )

        # update the AGEvent object
        event_to_update.name = new_name
        event_to_update.venue_uuid = new_venue_object
        event_to_update.description = new_description
        event_to_update.save()

        messages.success(request, "Event updated successfully")

    return redirect("/events")


@require_event_code_function
def delete_event(request, event_uuid=None):
    event_to_delete = AGEvent.objects.get(uuid=event_uuid)

    # delete any dashboards that exist for this event
    gfconfigs = GFConfig.objects.all()

    # Add panel to each grafana instance
    for gfconfig in gfconfigs:

        # Grafana instance using current GFConfig
        grafana = Grafana(gfconfig)

        deleted = grafana.delete_dashboard_by_name(event_to_delete.name)

        if not deleted:
            messages.error(
                request,
                f"Failed to delete Event dashboard from Grafana instance: "
                f"{gfconfig.gf_host}",
            )

    event_to_delete.delete()
    return redirect("/events")


@require_event_code_function
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
                    measurement.value,
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
    if len(measurements_object) > 0:
        sensor = AGSensor.objects.get(id=measurements_object[0].sensor_id.id)
        for measurement in measurements_object:
            if sensor.id != measurement.sensor_id:
                sensor = AGSensor.objects.get(id=measurement.sensor_id.id)
            temp = {
                "sensor name": sensor.name,
                "timestamp": str(measurement.timestamp),
                "values": measurement.value,
            }
            measurement_info.append(temp)

    data = {"event_info": event_info, "measurement_info": measurement_info}

    return data


@require_event_code_function
def activate_event(request, event_uuid=None):
    event_to_activate = AGEvent.objects.get(uuid=event_uuid)
    if event_to_activate is not None:
        AGActiveEvent.objects.all().delete()
        active_event = AGActiveEvent(agevent=event_to_activate)
        active_event.save()
    return redirect("/events")


@require_event_code_function
def deactivate_event(request, event_uuid=None):
    event_to_deactivate = AGEvent.objects.get(uuid=event_uuid)
    if event_to_deactivate is not None:
        AGActiveEvent.objects.all().delete()
    return redirect("/events")


@require_event_code_function
def export_event(request, event_uuid=None, file_format="CSV"):
    event_to_export = AGEvent.objects.get(uuid=event_uuid)
    if event_to_export:
        filename = event_to_export.name.replace(" ", "").lower()
        measurement_data = AGMeasurement.objects.filter(event_uuid=event_uuid)
        if len(measurement_data) == 0:
            measurement_data = []

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
                        "reading": measurement.value,
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
            response = create_event_csv(
                writer, response, event_to_export, venue, measurement_data
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
        active_event_object = AGActiveEvent.objects.all()
        active_event = None
        if len(active_event_object) > 0:
            active_event = active_event_object[0].agevent

        configure_events_github_url = os.path.join(GITHUB_DOCS_ROOT,
                                                    CONFIGURE_EVENTS_HELP_DOC)

        context = {
            "event_form": event_form,
            "venue_form": venue_form,
            "events": events,
            "venues": venues,
            "active_event": active_event,
            "configure_events_github_url": configure_events_github_url,
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

        configure_events_github_url = os.path.join(GITHUB_DOCS_ROOT,
                                                   CONFIGURE_EVENTS_HELP_DOC)

        context = {
            "event_form": event_form,
            "venue_form": venue_form,
            "events": events,
            "venues": venues,
            "configure_events_github_url": configure_events_github_url
        }
        return render(request, self.template_name, context)
