
class TypewiseAlert:
    def __init__(self, limits_for_types=None, alert_target_funcs=None):
        # Default values can be moved out of code to DB as required
        self.default_limits_for_cooling_types = {
            "PASSIVE_COOLING": (0, 35),
            "MED_ACTIVE_COOLING": (0, 40),
            "HI_ACTIVE_COOLING": (0, 45),
        }
        self.default_alert_funcs = {
                'TO_CONTROLLER': self.send_controller_message,
                'TO_EMAIL': self.send_email
            }
        self.alert_mail_details = {
            "TOO_LOW": {
                "recipient": "low_temperature_breach_expert@bosch.com",
                "email_message": "The temperature has dropped beyond lower breach limits. "
                                 "Please take corrective action immediately."
            },
            "TOO_HIGH": {
                "recipient": "high_temperature_breach_expert@bosch.com",
                "email_message": "The temperature has dropped beyond upper breach limits. "
                                 "Please take corrective action immediately."
            },
            "NORMAL": {
                "recipient": "monitoring_team@bosch.com",
                "email_message": "The temperature is OK."
            },
        }
        self.default_controller_header = 0xfeed
        self.limits_for_types = [limits_for_types if limits_for_types is not None
                                 else self.default_limits_for_cooling_types][0]
        self.alert_target_funcs = [alert_target_funcs if alert_target_funcs is not None
                                   else self.default_alert_funcs][0]

    def send_controller_message(self, breach_type):
        print(f'{self.default_controller_header}, {breach_type}')
        return f"CONTROLLER_MESSAGE,{breach_type}"

    def send_email(self, breach_type):
        recipients = self.alert_mail_details[breach_type]['recipient']
        email_message = self.alert_mail_details[breach_type]['email_message']
        email_content = f"To,\n{recipients}\n \t{email_message}"
        print(email_content)
        return f"EMAIL,{breach_type}"

    def infer_breach(self, value, lower_limit, upper_limit):
        if value < lower_limit:
            return 'TOO_LOW'
        if value > upper_limit:
            return 'TOO_HIGH'
        return 'NORMAL'

    def classify_temperature_breach(self, cooling_type, temperature_in_c):
        lower_limit, upper_limit = self.limits_for_types[cooling_type]
        return self.infer_breach(temperature_in_c, lower_limit, upper_limit)

    def check_and_alert(self, alert_target, battery_characteristic, temperature_in_c):
        breach_type = \
            self.classify_temperature_breach(battery_characteristic['coolingType'], temperature_in_c)
        return self.alert_target_funcs[alert_target](breach_type)
