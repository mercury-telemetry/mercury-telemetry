from mercury.tests.selenium_tests.selenium_base import SeleniumTestBase
from django.urls import reverse
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options


class CreateEventTest(SeleniumTestBase):
    def setUp(self):
        self.set_test_code()
        options = Options()
        options.add_argument("-headless")
        self.wd = Firefox(firefox_options=options)
        self.wd.implicitly_wait(10)

    def tearDown(self):
        self.wd.quit()

    def test_create_event(self):
        # login with testcode
        self.login_test_code()

        # navigate to events, "Create Venue" tab
        self.open(reverse("mercury:events"))
        self.wd.find_element_by_xpath("//input[@value='Create Venue']").click()

        # fill form
        self.wd.find_element_by_id("post-event-name").send_keys("location1")
        self.wd.find_element_by_id("post-event-description").send_keys("New York")
        self.wd.find_element_by_id("post-event-latitude").send_keys("41")
        self.wd.find_element_by_id("post-event-longitude").send_keys("-74")

        # submit form, redirects events
        self.wd.find_element_by_xpath("//input[@name='submit-venue']").click()

        # navigate to events, "All Venues" tab, check table
        self.wd.find_element_by_xpath("//input[@value='All Venues']").click()
        field = "//div[@id='all-venues']/div/table/tbody/tr/td[{}]"
        loc_name = self.wd.find_element_by_xpath(field.format(2)).text
        loc_description = self.wd.find_element_by_xpath(field.format(3)).text
        loc_latitude = self.wd.find_element_by_xpath(field.format(4)).text
        loc_longitude = self.wd.find_element_by_xpath(field.format(5)).text

        self.assertEqual(loc_name, "location1")
        self.assertEqual(loc_description, "New York")
        self.assertEqual(float(loc_latitude), 41.0)
        self.assertEqual(float(loc_longitude), -74.0)

        # navigate to events, "Create Event" tab
        self.wd.find_element_by_xpath("//input[@value='Create Event']").click()

        # fill form
        self.wd.find_element_by_id("name").send_keys("event1")
        self.wd.find_element_by_id("date").send_keys("2020-03-03 09:00:00")
        self.wd.find_element_by_id("description").send_keys("details1")
        self.wd.find_element_by_id("id_venue_uuid").send_keys("1")

        # submit form, redirects to events, "All Events" tab
        self.wd.find_element_by_xpath("//input[@name='submit-event']").click()

        # check events table
        # field = "//div[@id='all-events']/div/table/tbody/tr/td[{}]"
        # event_name = self.wd.find_element_by_xpath(field.format(2)).text
        # loc_name = self.wd.find_element_by_xpath(field.format(4)).text
        # event_date = self.wd.find_element_by_xpath(field.format(5)).text
        # event_description = self.wd.find_element_by_xpath(field.format(6)).text

        # self.assertEqual(event_name, "event1")
        # self.assertEqual(loc_name, "location1")
        # self.assertEqual(event_date, "March 3, 2020, 9 a.m.")
        # self.assertEqual(event_description, "details1")
