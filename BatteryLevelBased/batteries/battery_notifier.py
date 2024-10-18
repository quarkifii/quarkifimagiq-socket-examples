import psutil
import time
import win32api
import win32con
import win32gui
from .magiq_control import device_on_off


def get_battery_info():
    battery = psutil.sensors_battery()
    battery_percent = battery.percent
    power_plugged = battery.power_plugged

    return battery_percent, power_plugged


def check_battery_status(previous_percent):
    percent, status = get_battery_info()
    response = {}

    if percent != previous_percent:
        if status:
            if percent >= 80:
                response = device_on_off('16612385', False)
                if response:
                    print('Device turned off:', response)
                else:
                    print('Error:', response)
        else:
            if percent <= 20:
                response = device_on_off('16612385', True)
                if response:
                    print('Device turned on:', response)
                else:
                    print('Error:', response)

        print(f"Battery Level: {percent}%")
        print(f"Status: {'Plugged in' if status else 'not Plugged in'}")

    return percent


class BatteryStatusNotifier:
    def __init__(self):
        self.hwnd = None
        self.previous_percent = None

    def start(self):
        wc = win32gui.WNDCLASS()
        wc.lpfnWndProc = self.wnd_proc
        wc.lpszClassName = 'BatteryStatusNotifier'
        wc.hInstance = win32api.GetModuleHandle(None)
        class_atom = win32gui.RegisterClass(wc)
        self.hwnd = win32gui.CreateWindow(class_atom, 'BatteryStatusNotifier', 0, 0, 0, 0, 0, 0, 0, wc.hInstance, None)
        win32gui.UpdateWindow(self.hwnd)
        self.previous_percent = get_battery_info()[0]
        self.message_loop()

    def wnd_proc(self, hwnd, msg, wparam, lparam):
        if msg == win32con.WM_POWERBROADCAST and wparam == win32con.PBT_APMPOWERSTATUSCHANGE:
            self.previous_percent = check_battery_status(self.previous_percent)
        return 0

    def message_loop(self):
        while True:
            win32gui.PumpWaitingMessages()
            self.previous_percent = check_battery_status(self.previous_percent)
            time.sleep(60)
