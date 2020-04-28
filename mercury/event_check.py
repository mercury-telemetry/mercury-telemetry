import functools
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse


def require_event_code(func):
    """This decorator can be used on any method which is a view, such as
    get or post for a Class view, in order to verify that the user
    has "logged-in" if necessary, meaning that if an event is active, that
    the user has supplied the necessary credentials. """

    @functools.wraps(func)
    def wrapper(self, request, *args, **kwargs):
        if request.session.get("event_code_active") and not request.session.get(
            "event_code_known"
        ):
            # event is active but user doesn't know the event code
            valid_session = False
        else:
            # event is active and user does know the event code
            valid_session = True

        if request.session.get("event_code_active") is None:
            # server hasn't determined if an event is active yet
            valid_session = False

        if not valid_session:
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


def require_event_code_function(func):
    """This decorator can be used on any function in order to verify that the user
    has "logged-in" if necessary, meaning that if an event is active, that
    the user has supplied the necessary credentials. """

    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.session.get("event_code_active") and not request.session.get(
            "event_code_known"
        ):
            # event is active but user doesn't know the event code
            valid_session = False
        else:
            # event is active and user does know the event code
            valid_session = True

        if request.session.get("event_code_active") is None:
            # server hasn't determined if an event is active yet
            valid_session = False

        if not valid_session:
            messages.error(
                request,
                (
                    "You do not have an active session. "
                    "Please submit the active event code."
                ),
            )
            return HttpResponseRedirect(reverse("mercury:EventAccess"))
        return func(request, *args, **kwargs)

    return wrapper
