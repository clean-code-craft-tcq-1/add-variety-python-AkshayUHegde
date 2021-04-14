import random
import unittest
import typewise_alert


# Have also performed Handle Comms tests here
class TypewiseTest(unittest.TestCase):
    def test_check_and_alert_too_low_controller(self):
        expected_alert_type = "TOO_LOW"
        expected_test_alert_mechanism = "TO_CONTROLLER"
        expected_test_alert_response = "CONTROLLER_MESSAGE"
        expected_cooling_type = "PASSIVE_COOLING"
        test_alert_obj = typewise_alert.TypewiseAlert()
        limit = test_alert_obj.limits_for_types[expected_cooling_type][0]
        temp = limit - 10
        alert_status = test_alert_obj.check_and_alert(expected_test_alert_mechanism,
                                                      {'coolingType': expected_cooling_type}, temp)
        expected_alert_status = ','.join([expected_test_alert_response, expected_alert_type])
        self.assertEqual(alert_status, expected_alert_status)

    def test_check_and_alert_too_high_custom_cooling_email(self):
        expected_alert_type = "TOO_HIGH"
        expected_test_alert_mechanism = "TO_EMAIL"
        expected_test_alert_response = "EMAIL"
        custom_cooling_type = "CUSTOM_ACTIVE_COOLING"
        custom_cooling_type_limits = {
            custom_cooling_type: (-40, 80)
        }
        test_alert_obj = typewise_alert.TypewiseAlert(limits_for_types=custom_cooling_type_limits)
        limit = custom_cooling_type_limits[custom_cooling_type][1]
        temp = limit + 10
        alert_status = test_alert_obj.check_and_alert(expected_test_alert_mechanism,
                                                      {'coolingType': custom_cooling_type}, temp)
        expected_alert_status = ','.join([expected_test_alert_response, expected_alert_type])
        self.assertEqual(alert_status, expected_alert_status)

    def test_check_and_alert_normal_custom_console(self):
        expected_alert_type = "NORMAL"
        custom_test_alert_mechanism = "TO_CONSOLE"
        custom_test_alert_response = "CONSOLE_MESSAGE"

        def alert_to_console(breach_type):
            print(breach_type)
            return f"{custom_test_alert_response},{breach_type}"

        custom_test_alert_map = {
            custom_test_alert_mechanism: alert_to_console
        }
        expected_cooling_type = "MED_ACTIVE_COOLING"
        test_alert_obj = typewise_alert.TypewiseAlert(alert_target_funcs=custom_test_alert_map)
        limit = test_alert_obj.limits_for_types[expected_cooling_type][0]
        temp = limit + 10
        alert_status = test_alert_obj.check_and_alert(custom_test_alert_mechanism,
                                                      {'coolingType': expected_cooling_type}, temp)
        expected_alert_status = ','.join([custom_test_alert_response, expected_alert_type])
        self.assertEqual(alert_status, expected_alert_status)


unittest.main()
