import random
import unittest
import typewise_alert


# Have also performed Handle Comms tests here
class TypewiseTest(unittest.TestCase):
    def test_check_and_alert(self):
        new_limits_for_cooling_types = {
            "PASSIVE_COOLING": (-20, 20),
            "MED_ACTIVE_COOLING": (0, 100),
            "HI_ACTIVE_COOLING": (-1000, 2000),
        }

        def test_send_func(breach_type):
            print(breach_type)
            return f"TEST_FUNC,{breach_type}"

        test_alerts = [
            "TOO_LOW",
            "TOO_HIGH",
            "NORMAL",
            "TOO_HIGH"
        ]
        test_alert_mechanisms = {
            "TO_CONTROLLER": "CONTROLLER_MESSAGE",
            "TO_EMAIL": "EMAIL",
            "TO_CONSOLE": "CONSOLE_MESSAGE",
            "TO_TEST_FUNC": "TEST_FUNC"
        }
        typewise_alert_objects = [
            typewise_alert.TypewiseAlert(
                limits_for_types=new_limits_for_cooling_types),
            typewise_alert.TypewiseAlert(
                alert_mail_details={"TOO_HIGH": {
                    "recipient": "test_high_temp_expert@bosch.com",
                    "email_message": "Temperature too high."
                }}),
            typewise_alert.TypewiseAlert(),
            typewise_alert.TypewiseAlert(
                alert_target_funcs={"TO_TEST_FUNC": test_send_func})
        ]
        test_limits_for_cooling_types = [
            new_limits_for_cooling_types,
            typewise_alert_objects[1].default_limits_for_cooling_types,
            typewise_alert_objects[2].default_limits_for_cooling_types,
            typewise_alert_objects[3].default_limits_for_cooling_types
        ]
        index = 0
        for test_alert_mechanism in test_alert_mechanisms:
            count_cooling_types = len(test_limits_for_cooling_types[index])
            cooling_type = list(test_limits_for_cooling_types[index].keys())[random.randint(0, count_cooling_types - 1)]
            limit = test_limits_for_cooling_types[index][cooling_type][index % 2]
            temp = [limit - 10 if index == 0 else limit + 10][0]
            expected_alert_dest = test_alert_mechanisms[test_alert_mechanism]
            expected_alert_type = test_alerts[index]
            alert_status = typewise_alert_objects[index].check_and_alert(test_alert_mechanism,
                                                                         {'coolingType': cooling_type},
                                                                         temp
                                                                         )
            alert_status = alert_status.split(',')
            self.assertEqual(alert_status, [expected_alert_dest, expected_alert_type], f"{alert_status} is incorrect. "
                                                                                       f"Reported temp was {temp} for "
                                                                                       f"{cooling_type}")
            index += 1

    # def test_infers_breach_as_per_lower_limit(self):
    #     self.assertTrue(typewise_alert.TypewiseAlert().infer_breach(20, 50, 100) == 'TOO_LOW')
    #
    # def test_infers_breach_as_per_upper_limit(self):
    #     self.assertTrue(typewise_alert.TypewiseAlert().infer_breach(60, 0, 50) == 'TOO_HIGH')
    #
    # def test_infers_no_breach_within_limits(self):
    #     self.assertTrue(typewise_alert.TypewiseAlert().infer_breach(40, 0, 100) == 'NORMAL')
    #
    # def test_classifies_breach_correctly(self):
    #     limits_for_cooling_types = {
    #         "PASSIVE_COOLING": (0, 35),
    #         "MED_ACTIVE_COOLING": (0, 40),
    #         "HI_ACTIVE_COOLING": (0, 45),
    #     }
    #     count_cooling_types = len(limits_for_cooling_types)
    #     cooling_type = list(limits_for_cooling_types.keys())[random.randint(0, count_cooling_types - 1)]
    #     upper_limit = limits_for_cooling_types[cooling_type][1]
    #     too_high_temp = upper_limit + 10
    #     self.assertTrue(typewise_alert.TypewiseAlert().classify_temperature_breach(cooling_type, too_high_temp)
    #                     == 'TOO_HIGH')


unittest.main()
