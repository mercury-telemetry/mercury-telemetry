from django.views.generic import TemplateView


class StopwatchView(TemplateView):
    template_name = "stopwatch.html"
