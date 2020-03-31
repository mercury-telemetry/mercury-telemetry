import logging
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import TemplateView
from mercury.forms import GFConfigForm
from mercury.models import GFConfig
from mercury.grafanaAPI.grafana_api import Grafana
from django.contrib import messages
from django.conf import settings

log = logging.getLogger(__name__)
log.setLevel(logging.ERROR)


# Sets the GFConfig's current status to True
def update_config(request, gf_id=None):
    GFConfig.objects.all().update(gf_current=False)
    GFConfig.objects.filter(id=gf_id).update(gf_current=True)
    return redirect("/gfconfig")


def delete_config(request, gf_id=None):
    GFConfig.objects.get(id=gf_id).delete()
    return redirect("/gfconfig")


class GFConfigView(TemplateView):

    template_name = "gf_configs.html"

    def get(self, request, *args, **kwargs):
        configs = GFConfig.objects.all().order_by("id")
        config_form = GFConfigForm()
        context = {"config_form": config_form, "configs": configs}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if "submit" in request.POST:
            DB = settings.DATABASES
            config_data = GFConfig(
                gf_name=request.POST.get("gf_name"),
                gf_host=request.POST.get("gf_host"),
                gf_token=request.POST.get("gf_token"),
                gf_db_host=DB["default"]["HOST"] + ":" + str(DB["default"]["PORT"]),
                gf_db_name=DB["default"]["NAME"],
                gf_db_username=DB["default"]["USER"],
                gf_db_pw=DB["default"]["PASSWORD"],
            )

            # Create Grafana instance with host and token
            grafana = Grafana(config_data)
            try:
                grafana.validate_credentials()
                config_data.gf_current = True
                # Only save the config if credentials were validated
                config_data.save()
            except ValueError as error:
                messages.error(request, f"Grafana initial set up failed: {error}")

            try:
                grafana.create_postgres_datasource()
            except ValueError as error:
                messages.error(request, f"Datasource couldn't be created. {error}")

            configs = GFConfig.objects.all().order_by("id")
            config_form = GFConfigForm(request.POST)
            context = {"config_form": config_form, "configs": configs}
            return render(request, self.template_name, context)
