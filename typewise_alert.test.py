import random
import unittest
import typewise_alert


# Have also performed Handle Comms tests here
class TypewiseTest(unittest.TestCase):
    def test_infers_breach_as_per_lower_limit(self):
        self.assertTrue(typewise_alert.TypewiseAlert().infer_breach(20, 50, 100) == 'TOO_LOW')

    def test_infers_breach_as_per_upper_limit(self):
        self.assertTrue(typewise_alert.TypewiseAlert().infer_breach(60, 0, 50) == 'TOO_HIGH')

    def test_infers_no_breach_within_limits(self):
        self.assertTrue(typewise_alert.TypewiseAlert().infer_breach(40, 0, 100) == 'NORMAL')

    def test_classifies_breach_correctly(self):
        limits_for_cooling_types = {
            "PASSIVE_COOLING": (0, 35),
            "MED_ACTIVE_COOLING": (0, 40),
            "HI_ACTIVE_COOLING": (0, 45),
        }
        count_cooling_types = len(limits_for_cooling_types)
        cooling_type = list(limits_for_cooling_types.keys())[random.randint(0, count_cooling_types - 1)]
        upper_limit = limits_for_cooling_types[cooling_type][1]
        too_high_temp = upper_limit + 10
        self.assertTrue(typewise_alert.TypewiseAlert().classify_temperature_breach(cooling_type, too_high_temp)
                        == 'TOO_HIGH')


if __name__ == '__main__':
    unittest.main()
