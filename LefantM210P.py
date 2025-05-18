# LefantM210P.py

import tinytuya
from config import DEVICE_ID, DEVICE_IP, LOCAL_KEY, TUYA_VERSION

class LefantM210P:
    def __init__(self):
        self.device = tinytuya.OutletDevice(DEVICE_ID, DEVICE_IP, LOCAL_KEY)
        self.device.set_version(TUYA_VERSION)
        self.device.socketPersistent = True

    def send_direction(self, direction):
        try:
            self.device.set_value('4', direction)
        except Exception as e:
            print("[Erreur TinyTuya]", e)

    def get_battery_level(self):
        try:
            return self.device.status().get("dps", {}).get("6")
        except:
            return None

    def keep_alive(self):
        import time
        while True:
            try:
                self.device.status()
            except:
                pass
            time.sleep(30)

    def update_battery_loop(self, update_callback):
        import time
        while True:
            bat = self.get_battery_level()
            if bat is not None:
                update_callback(bat)
            time.sleep(5)

    def start_clean(self):
        self.device.set_value('3', 'smart')
        self.device.set_value('2', True)

    def stop_clean(self):
        self.device.set_value('2', False)

    def return_to_base(self):
        self.device.set_value('3', 'chargego')
        self.device.set_value('2', True)

    def cancel_return(self):
        self.device.set_value('2', False)
