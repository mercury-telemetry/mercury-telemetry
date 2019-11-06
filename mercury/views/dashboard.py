from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect  # noqa
from ..models import SimulatedData

# adding the Rest API
from rest_framework.response import Response
from rest_framework.views import APIView


class DashboardView(TemplateView):
    template_name = "dashboard.html"

    def get(self, request, *args, **kwargs):
        all_data = SimulatedData.objects.all().order_by("-created_at")
        return render(request, self.template_name, {"all_data": all_data})


class DashboardLiveView(TemplateView):
    template_name = "dashboard-live.html"

    def get(self, request, *args, **kwargs):
        all_data = SimulatedData.objects.all()
        return render(request, self.template_name, {"all_data": all_data})


class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        dictionary = dict()
        for item in SimulatedData.objects.all().order_by("-created_at"):
            dictionary[item.created_at] = item.temperature



        # dictionary = sorted(dictionary.items(), key=lambda x: x[0])
        # dictionary = dict(dictionary)

        data = {
            "article_labels": dictionary.keys(),
            "article_data": dictionary.values(),
        }
        return Response(data)
