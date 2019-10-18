from django.http import HttpResponse


def home(request):
    return HttpResponse("<h1>This is the page for the dashboard</h1>")