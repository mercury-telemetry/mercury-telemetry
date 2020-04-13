from django.views.generic import TemplateView
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib import pyplot as plt
import matplotlib

from django.http import HttpResponse

from ag_data.models import AGMeasurement, AGEvent
from mercury.event_check import require_event_code


class CreateGPSPanelView(TemplateView):
    """This is the view for creating a new event."""

    template_name = "gpspanels.html"

    @require_event_code
    def get(self, request, *args, **kwargs):
        # ruh_m = plt.imread('C:/.. … /Riyadh_map.png')

        gpsMeasurements = AGMeasurement.objects.filter(sensor_id=4)
        if len(gpsMeasurements) > 0:
            event = AGEvent.objects.get(uuid=gpsMeasurements[0].event_uuid_id)
            latitudes, longitutes = [], []
            for measurement in gpsMeasurements:
                value = measurement.value
                latitudes.append(value["latitude"])
                longitutes.append(value["longitude"])

            BBox = (
                min(latitudes) - 2,
                max(latitudes) + 2,
                min(longitutes) - 2,
                max(longitutes) + 2,
            )
            matplotlib.use("agg")
            fig, ax = plt.subplots(figsize=(8, 7))

            ax.scatter(latitudes, longitutes, zorder=1, alpha=0.2, c="b", s=10)
            ax.set_title("Plotting GPS map for " + event.name)
            ax.set_xlim(BBox[0], BBox[1])
            ax.set_ylim(BBox[2], BBox[3])

            # ax.imshow(ruh_m, zorder=0, extent = BBox, aspect= 'equal')

            canvas = FigureCanvas(fig)
            response = HttpResponse(content_type="image/jpg")
            canvas.print_jpg(response)
            return response
