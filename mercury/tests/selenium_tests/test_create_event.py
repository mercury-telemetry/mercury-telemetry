from mercury.tests.selenium_tests.selenium_base import SeleniumTestBase
from django.urls import reverse

# from selenium import webdriver

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options


class CreateEventTest(SeleniumTestBase):
    def setUp(self):
        self.set_test_code()
        # self.wd = webdriver.Firefox()
        options = Options()
        options.add_argument("-headless")
        self.wd = Firefox(firefox_options=options)
        self.wd.implicitly_wait(10)

    def tearDown(self):
        self.wd.quit()

    def test_create_event(self):
        # login with testcode
        self.login_test_code()

        # create a new event
        self.open(reverse("mercury:event"))
        self.wd.find_element_by_id("id_event_name").send_keys("event1")
        self.wd.find_element_by_id("id_event_location").send_keys("New York")
        self.wd.find_element_by_id("post-event-date").send_keys("2020-03-03")
        self.wd.find_element_by_id("post-event-comments").send_keys("event1 comment")

        # submit form, redirects to dashboard
        self.wd.find_element_by_xpath("//input[@value='Submit']").click()
        self.assertEqual(self.wd.title, "Mercury Raw Telemetry")

        # open simulator, locate new event
        self.open(reverse("mercury:simulator"))
        field = "//div[@id='accordion-event-form']/div/table/tbody/tr/td[{}]"
        event_name = self.wd.find_element_by_xpath(field.format(1)).text
        event_loc = self.wd.find_element_by_xpath(field.format(2)).text
        event_date = self.wd.find_element_by_xpath(field.format(3)).text
        event_comments = self.wd.find_element_by_xpath(field.format(4)).text

        # check new event
        self.assertEqual(event_name, "event1")
        self.assertEqual(event_loc, "New York")
        self.assertEqual(event_date, "March 3, 2020, midnight")
        self.assertEqual(event_comments, "event1 comment")
