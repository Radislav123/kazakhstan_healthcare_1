import datetime
import json

import cryptography.x509.name
from cryptography.hazmat.primitives.serialization import Encoding, pkcs12

from pages import DigitalLogInPage, LogInPage
from parser import models
from parser.management.commands import parser_browser_command


class Command(parser_browser_command.ParserBrowserCommand):
    @staticmethod
    def get_subject_data(obj: cryptography.x509.name.Name) -> dict[str, str]:
        not_prepared_data = dict(x.rfc4514_string().split('=') for x in obj.rdns)
        data = {}

        for key, value in not_prepared_data.items():
            if "iin" in value.lower():
                data["iin"] = str(int(value[3:]))
                break
            else:
                data["iin"] = "-1"
        data["email"] = ""
        data["fio"] = f"{not_prepared_data['CN']} {not_prepared_data['2.5.4.42']}"

        return data

    @staticmethod
    def prepare_date(date: datetime.datetime) -> str:
        return ".".join(date.date().isoformat().split('-')[::-1])

    @classmethod
    def read_certificate(cls) -> dict[str, str]:
        data = {}
        log_in_settings = models.LogInSettings.get()
        with open(log_in_settings.digital_signature_path, "rb") as file:
            _, certificate, _ = pkcs12.load_key_and_certificates(
                file.read(),
                log_in_settings.digital_signature_password.encode()
            )
            data["not_before"] = cls.prepare_date(certificate.not_valid_before)
            data["not_after"] = cls.prepare_date(certificate.not_valid_after)
            data["certificate"] = "".join(certificate.public_bytes(Encoding.PEM).decode().split('\n')[1:-2])
            data.update(cls.get_subject_data(certificate.subject))
        return data

    def get_js_script(self) -> str:
        data = self.read_certificate()
        with open(self.settings.JS_REPLACE_CERTIFICATE_PATH, 'r') as file:
            script = file.read()
        for key, value in data.items():
            script = script.replace(f"{key}_placeholder", value)
        return script

    def run(self) -> None:
        log_in_page = LogInPage(self.driver)
        log_in_page.log_in(self.settings.secrets.log_in_settings.iin, self.settings.secrets.log_in_settings.password)

        self.driver.execute_script(self.get_js_script())

        digital_log_in_page = DigitalLogInPage(self.driver)
        digital_log_in_page.log_in()

        with open(self.settings.AUTH_COOKIES_PATH, 'w') as file:
            json.dump(self.driver.get_cookies(), file, indent = 4)
