import logging
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import TemplateView
from ..event_check import require_event_code
from mercury.forms import EventForm
from ag_data.models import AGEvent

log = logging.getLogger(__name__)
log.setLevel(logging.ERROR)


def update_event(request, event_uuid=None):
    event_to_update = AGEvent.objects.get(event_uuid=event_uuid)
    if event_to_update:
        event_to_update.event_name = request.POST.get("event_name")
        event_to_update.event_location = request.POST.get("event_location")
        event_to_update.event_date = request.POST.get("event_date")
        event_to_update.event_description = request.POST.get("event_description")
        event_to_update.save()

    return redirect("/events")


def delete_event(request, event_uuid=None):
    event_to_delete = AGEvent.objects.get(event_uuid=event_uuid)
    event_to_delete.delete()
    return redirect("/events")


class CreateEventsView(TemplateView):
    """This is the view for creating a new event."""

    template_name = "events.html"

    @require_event_code
    def get(self, request, *args, **kwargs):
        events = AGEvent.objects.all().order_by("event_uuid")
        event_form = EventForm()
        context = {"event_form": event_form, "events": events}
        return render(request, self.template_name, context)

    @require_event_code
    def post(self, request, *args, **kwargs):
        if "submit" in request.POST:
            post_event_name = request.POST.get("event_name")
            post_event_location = request.POST.get("event_location")
            post_event_date = request.POST.get("event_date")
            post_event_description = request.POST.get("event_description")
            event_data = AGEvent(
                event_name=post_event_name,
                event_location=post_event_location,
                event_date=post_event_date,
                event_description=post_event_description,
            )
            event_data.save()
            events = AGEvent.objects.all().order_by("event_uuid")
            event_form = EventForm()
            context = {"event_form": event_form, "events": events}
            return render(request, self.template_name, context)
