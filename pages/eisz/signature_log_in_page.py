import datetime
import subprocess
import time

import cryptography.x509.name
import pyautogui
import pyperclip
import pywinauto
from cryptography.hazmat.primitives.serialization import Encoding, pkcs12
from parsing_helper.web_elements import ExtendedWebElement
from pywinauto.controls.hwndwrapper import DialogWrapper

from eisz import models
from pages.eisz import base_page


# https://www.eisz.kz/edslogin
class SignatureLogInPage(base_page.BasePage):
    path = "edslogin"

    def __init__(self, driver) -> None:
        super().__init__(driver)

        self.enter_button = ExtendedWebElement(self, '//button[@id = "edsLoginBtn"]')
        self.choose_certificate_button = ExtendedWebElement(self, '//button[@onclick]')

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
    def read_certificate(cls, log_in_settings: models.LogInSettings) -> dict[str, str]:
        data = {}
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

    def get_js_script(self, log_in_settings: models.LogInSettings) -> str:
        data = self.read_certificate(log_in_settings)
        with open(self.settings.JS_REPLACE_CERTIFICATE_PATH, 'r') as file:
            script = file.read()
        for key, value in data.items():
            script = script.replace(f"{key}_placeholder", value)
        return script

    @classmethod
    def get_process_ids_by_name(cls, name: str) -> list[int]:
        return [key for key, value in cls.get_all_processes().items() if value.lower().startswith(name.lower())]

    @staticmethod
    def get_all_processes() -> dict[int, str]:
        start = 1

        output = str(subprocess.check_output(["tasklist", "/FO", "csv"]))
        processes = output.split('\\r\\n')[start:-1]
        processes = [[y.strip('\"') for y in x.split(',')] for x in processes]

        processes = {int(x[1]): x[0] for x in processes}
        return processes

    @classmethod
    def enable_popup_window(cls) -> None:
        process_name = "java"
        process_ids = cls.get_process_ids_by_name(process_name)
        if len(process_ids) > 1:
            raise ValueError(f"There are more then 1 {process_name} processes.")
        process_id = process_ids[0]
        app = pywinauto.Application(backend = "uia").connect(process = process_id)

        window_class_name = "SunAwtDialog"
        dialog_window: pywinauto.WindowSpecification | DialogWrapper = app.window(class_name = window_class_name)

        dialog_window.set_focus()

    def open_new_certificate(self, log_in_settings: models.LogInSettings) -> None:
        timeout = 1

        time.sleep(timeout)
        pyperclip.copy(log_in_settings.digital_signature_path)
        pyautogui.hotkey("ctrl", "v")
        pyautogui.press("enter")

        time.sleep(timeout)
        pyperclip.copy(log_in_settings.digital_signature_password)
        pyautogui.hotkey("ctrl", "v")
        pyautogui.press("enter")

        time.sleep(timeout)
        pyautogui.press("enter")

    def log_in(self, log_in_settings: models.LogInSettings) -> None:
        # не надо открывать страницу, так как это сбрасывает ввод ЭЦП
        # self.open()
        time.sleep(1)

        try:
            js_script = self.get_js_script(log_in_settings)
            self.driver.execute_script(js_script)
        except ValueError:
            self.choose_certificate_button.click()
            self.enable_popup_window()
            self.open_new_certificate(log_in_settings)

        self.enter_button.click()
