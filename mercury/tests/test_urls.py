from django.test import SimpleTestCase
from django.urls import reverse, resolve
from mercury.views import views


class TestUrls(SimpleTestCase):
    def test_index_url_is_resolved(self):
        url = reverse("mercury:index")
        self.assertEquals(resolve(url).func.view_class, views.HomePageView)
