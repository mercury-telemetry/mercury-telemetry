import logging
from django.shortcuts import render
from django.views.generic import TemplateView
from ..event_check import require_event_code

from mercury.forms import EventForm
from mercury.models import Event

log = logging.getLogger(__name__)
log.setLevel(logging.ERROR)


class CreateEventView(TemplateView):
    """This is the view for creating a new event."""

    template_name = "event.html"

    @require_event_code
    def get(self, request, *args, **kwargs):
        event_form = EventForm()
        context = {"event_form": event_form}
        return render(request, self.template_name, context)

    @require_event_code
    def post(self, request, *args, **kwargs):
        post_event_name = request.POST.get("event_name")
        post_event_location = request.POST.get("event_location")
        post_event_date = request.POST.get("date")
        post_event_comments = request.POST.get("comments")
        event_data = Event(
            event_name=post_event_name,
            event_location=post_event_location,
            date=post_event_date,
            comments=post_event_comments,
        )

        event_data.save()
        return render(request, "dashboard.html")
