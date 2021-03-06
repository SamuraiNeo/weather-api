import unittest
from requests.exceptions import HTTPError
from weather import Weather


class WeatherTests(unittest.TestCase):
    def test_lookup(self):
        w = Weather()
        data = w.lookup(woeid=560743)
        self.assertIsNotNone(data.print_obj())
        self.assertTrue('Dublin' in data.description())

    def test_search(self):
        w = Weather()
        data = w.lookup_by_location('Dublin')
        self.assertIsNotNone(data.print_obj())
        self.assertTrue('Dublin' in data.description())

    def test_forecast(self):
        w = Weather()
        location = w.lookup_by_location('Dublin')
        self.assertIsNotNone(location.print_obj())
        forecasts = location.forecast()
        self.assertTrue(len(forecasts) > 0)
        first = forecasts[0]
        self.assertTrue(hasattr(first, 'text'))
        self.assertTrue(hasattr(first, 'high'))
        self.assertTrue(hasattr(first, 'low'))
        self.assertTrue(hasattr(first, 'date'))

    def test_condition(self):
        w = Weather()
        location = w.lookup_by_location('Dublin')
        self.assertIsNotNone(location.print_obj())
        condition = location.condition()
        self.assertTrue(hasattr(condition, 'text'))
        self.assertTrue(hasattr(condition, 'temp'))
        self.assertTrue(hasattr(condition, 'code'))
        self.assertTrue(hasattr(condition, 'date'))

    def test_invalid_lookup_value(self):
        w = Weather()
        data = w.lookup(woeid=1)
        try:
            print(data.location())
        except AttributeError:
            self.assertTrue(True)
        except Exception as e:
            self.fail("Unexpected exception raised: " + e.message)

    def test_bad_request(self):
        w = Weather()
        try:
            w.lookup(woeid="")
        except HTTPError:
            self.assertTrue(True)
        except Exception as e:
            self.fail("Unexpected exception raised: " + e.message)
