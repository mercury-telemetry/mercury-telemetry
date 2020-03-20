import logging
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import TemplateView
from mercury.forms import GFConfigForm
from mercury.models import GFConfig

log = logging.getLogger(__name__)
log.setLevel(logging.ERROR)


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
            config_data = GFConfig(
                gf_name = request.POST.get("gf_name"),
                gf_host = request.POST.get("gf_host"),
                gf_token = request.POST.get("gf_token"),
            )
            config_data.save()
            
            configs = GFConfig.objects.all().order_by("id")
            config_form = GFConfigForm()
            context = {"config_form": config_form, "configs": configs}
            return render(request, self.template_name, context)
