import configparser
import json


class ConfigServiceTemplate:
    def __init__(self, config_file_path):
        self.Config = configparser.ConfigParser()
        self.Config.read(config_file_path)

    def get_sms_config(self):
        sms_config = {
            "APIKey": self.Config.get("SMS Config", "APIKey"),
            "senderid": self.Config.get("SMS Config", "senderid"),
            "channel": self.Config.get("SMS Config", "channel"),
            "DCS": self.Config.get("SMS Config", "DCS"),
            "flashsms": self.Config.get("SMS Config", "flashsms"),
            "number": self.Config.get("SMS Config", "number"),
            "text": self.Config.get("SMS Config", "text"),
            "route": self.Config.get("SMS Config", "route"),
            "EntityId": self.Config.get("SMS Config", "EntityId"),
            "dlttemplateid": self.Config.get("SMS Config", "dlttemplateid")
        }
        return sms_config

    def get_email_config(self):
        email_config = {
            "subject": self.Config.get("Email Config", "subject"),
            "html_content": self.Config.get("Email Config", "html_content"),
            "sender": json.loads(self.Config.get("Email Config", "sender", fallback='{"name": "", "email": ""}')),
            "to": json.loads(self.Config.get("Email Config", "to", fallback='[{"email": ""}]')),
            "cc": json.loads(self.Config.get("Email Config", "cc", fallback='[{"email": "", "name": ""}]')),
            "bcc": json.loads(self.Config.get("Email Config", "bcc", fallback='[{"email": "", "name": ""}]')),
            "reply_to": json.loads(self.Config.get("Email Config", "reply_to", fallback='{"name": "", "email": ""}')),
            "headers": self.Config.get("Email Config", "headers"),
            "api-key-brevo": self.Config.get("Email Config", "api-key-brevo", fallback="")
        }
        return email_config


