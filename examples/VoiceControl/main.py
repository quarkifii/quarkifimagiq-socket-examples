import time
import speech_recognition as sr
from magiq_control import device_on_off

# Device IDs
devices = {
    'ac': '16612385',
    'light': '11715506'
}

device_list = list(devices.keys())

# Creating the message
message = "You have these registered devices:\n" + "\n".join(device_list)


def recognize_voice_command():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    try:
        with mic as source:
            print("Listening for voice command...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        command = recognizer.recognize_google(audio)
        print(f"Voice Command: {command}")
        return command.lower()
    except sr.UnknownValueError:
        print("Could not understand the audio")
        return None
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return None


if __name__ == '__main__':
    while True:
        command = recognize_voice_command()
        if command:
            if 'list' in command:
                print(message)
            else:
                action = "turn on" if "on" in command else "turn off" if "off" in command else None
                device = next((device for device in devices if device in command), None)

                if action and device:
                    operation = action == "turn on"
                    response = device_on_off(devices[device], operation)
                    print(f"The {device} has been turned {'ON' if operation else 'OFF'}.")
                else:
                    print("Command not recognized. Available commands are:\n"
                          "'list' to list devices\n"
                          "'turn on <device name>' to turn on a device\n"
                          "'turn off <device name>' to turn off a device")
        time.sleep(2)
