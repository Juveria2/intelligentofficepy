import unittest
from datetime import datetime
from unittest.mock import patch, Mock, PropertyMock, MagicMock
import mock.GPIO as GPIO
from mock.SDL_DS3231 import SDL_DS3231
from mock.adafruit_veml7700 import VEML7700
from src.intelligentoffice import IntelligentOffice, IntelligentOfficeError


class TestIntelligentOffice(unittest.TestCase):
    def setUp(self):
        self.servo_motor = MagicMock()
        self.light_sensor = MagicMock()
        self.light_bulb = MagicMock()
        self.gas_sensor = MagicMock()
        self.buzzer = MagicMock()
        self.intelligent_office = IntelligentOffice(
        )
    @patch.object(GPIO, "input")
     def test_check_quadrant_occupancy_detects_worker(self):
            self.servo_motor.check_quadrant_occupancy(7)
            self.intelligent_office.check_quadrant_occupancy(7)
            self.assertTrue(self.servo_motor.check_quadrant_occupancy(7))

        def test_check_quadrant_occupancy_no_worker(self):
            self.servo_motor.check_quadrant_occupancy(7)
            self.intelligent_office.check_quadrant_occupancy(7)
            self.assertFalse(self.servo_motor.check_quadrant_occupancy(7))

        def test_manage_blinds_based_on_time_day(self):
            with unittest.mock.patch('datetime.datetime') as mock_datetime:
                mock_datetime.now.return_value.hour = 10
                self.intelligent_office.manage_blinds_based_on_time()
                self.servo_motor.open.assert_called_once()

        def test_manage_blinds_based_on_time_night(self):
            with unittest.mock.patch('datetime.datetime') as mock_datetime:
                mock_datetime.now.return_value.hour = 22
                self.intelligent_office.manage_blinds_based_on_time()
                self.servo_motor.close.assert_called_once()

        def test_manage_light_level_turn_on_light(self):
            self.light_sensor.read.return_value = 30
            self.intelligent_office.manage_light_level()
            self.light_bulb.turn_on.assert_called_once()

        def test_manage_light_level_turn_off_light(self):
            self.light_sensor.read.return_value = 70
            self.intelligent_office.manage_light_level()
            self.light_bulb.turn_off.assert_called_once()

        def test_monitor_air_quality_safe(self):
            self.gas_sensor.read.return_value = 100
            self.intelligent_office.monitor_air_quality()
            self.buzzer.trigger.assert_not_called()

        def test_monitor_air_quality_hazardous(self):
            self.gas_sensor.read.return_value = 350
            self.intelligent_office.monitor_air_quality()
            self.buzzer.trigger.assert_called_once()

    if __name__ == '__main__':
        unittest.main()

