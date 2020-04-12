from django.views.generic import TemplateView
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.dates import DateFormatter
from matplotlib.figure import Figure
import random
import datetime

from django.http import HttpResponse

from mercury.event_check import require_event_code


class CreateGPSPanelView(TemplateView):
    """This is the view for creating a new event."""

    template_name = "gpspanels.html"

    @require_event_code
    def get(self, request, *args, **kwargs):
        fig = Figure()
        ax = fig.add_subplot(111)
        x = []
        y = []
        now = datetime.datetime.now()
        delta = datetime.timedelta(days=1)
        for i in range(10):
            x.append(now)
            now += delta
            y.append(random.randint(0, 1000))
        ax.plot_date(x, y, "-")
        ax.xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))
        fig.autofmt_xdate()
        canvas = FigureCanvas(fig)
        response = HttpResponse(content_type="image/jpg")
        canvas.print_jpg(response)
        return response
