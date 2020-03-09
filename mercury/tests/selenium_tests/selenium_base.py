from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse

from mercury.models import EventCodeAccess


class SeleniumTestBase(StaticLiveServerTestCase):
    """
    Base class for selenium tests
    """

    def open(self, url):
        self.wd.get("{}{}".format(self.live_server_url, url))

    def print_current_url(self):
        url = self.wd.current_url
        print("\n" + "-" * len(url))
        print(url)
        print("-" * len(url))

    def set_test_code(self):
        self.test_code = "testcode"
        EventCodeAccess.objects.create(event_code=self.test_code, enabled=True)

    def login_test_code(self):
        # open index, redirects to login
        self.open(reverse("mercury:EventAccess"))
        self.assertEqual(self.wd.title, "Mercury Event Access")

        # input event code, submit, redirects to index
        self.wd.find_element_by_name("eventcode").send_keys(self.test_code)
        self.wd.find_element_by_xpath("//input[@type='submit']").click()
