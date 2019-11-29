import functools
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse


def require_event_code(func):
    @functools.wraps(func)
    def wrapper(self, request, *args, **kwargs):
        if request.session.get("event_code_active") and not request.session.get(
            "event_code_known"
        ):
            messages.error(
                request,
                (
                    "You do not have an active session. "
                    "Please submit the active event code."
                ),
            )
            return HttpResponseRedirect(reverse("mercury:EventAccess"))
        return func(self, request, *args, **kwargs)

    return wrapper
