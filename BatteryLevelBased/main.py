from batteries.battery_notifier import BatteryStatusNotifier

if __name__ == "__main__":
    notifier = BatteryStatusNotifier()
    notifier.start()
