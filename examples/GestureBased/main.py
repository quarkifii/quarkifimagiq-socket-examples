import cv2
import mediapipe as mp
import time
import util
import magiq_control

mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_hands=1
)

GESTURE_DURATION = 1
PAUSE_DURATION = 5
MESSAGE_DURATION = 3
MONITORING_DELAY = 3

gesture_start_time = None
last_gesture = None
pause_until_time = None
message_display_time = None
message = "Monitoring"

# Device IDs
devices = {
    'ac': '16612385',
    'light': '11715506'
}


def gesture_one(landmarks_list, thumb_middle_dist):
    return (util.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list[8]) > 90 and
            util.get_angle(landmarks_list[9], landmarks_list[10], landmarks_list[12]) < 50 and
            util.get_angle(landmarks_list[13], landmarks_list[14], landmarks_list[16]) < 50 and
            util.get_angle(landmarks_list[17], landmarks_list[18], landmarks_list[20]) < 50 >
            thumb_middle_dist
            )


def gesture_two(landmarks_list, thumb_middle_dist):
    return (util.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list[8]) > 90 and
            util.get_angle(landmarks_list[9], landmarks_list[10], landmarks_list[12]) > 90 and
            util.get_angle(landmarks_list[13], landmarks_list[14], landmarks_list[16]) < 50 and
            util.get_angle(landmarks_list[17], landmarks_list[18], landmarks_list[20]) < 50 >
            thumb_middle_dist
            )


def detect_gestures(landmarks_list):
    global gesture_start_time, last_gesture, pause_until_time, message
    if time.time() < pause_until_time:
        return None

    if len(landmarks_list) >= 21:
        thumb_middle_dist = util.get_distance([landmarks_list[4], landmarks_list[9]])

        if gesture_one(landmarks_list, thumb_middle_dist):
            current_gesture = 'ac'
        elif gesture_two(landmarks_list, thumb_middle_dist):
            current_gesture = 'light'
        else:
            current_gesture = None

        if current_gesture:
            if last_gesture == current_gesture:
                if time.time() - gesture_start_time >= GESTURE_DURATION:
                    pause_until_time = time.time() + PAUSE_DURATION
                    message = current_gesture
                    return current_gesture
            else:
                gesture_start_time = time.time()
            last_gesture = current_gesture
        else:
            last_gesture = None
            gesture_start_time = None

    return None


def main():
    cap = cv2.VideoCapture(0)
    draw = mp.solutions.drawing_utils
    global pause_until_time, result, message, message_display_time
    pause_until_time = time.time()

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            processed = hands.process(frame_rgb)

            landmarks_list = []
            if processed.multi_hand_landmarks:
                for hand_landmarks in processed.multi_hand_landmarks:
                    draw.draw_landmarks(frame, hand_landmarks, mpHands.HAND_CONNECTIONS)
                    for lm in hand_landmarks.landmark:
                        landmarks_list.append((lm.x, lm.y))

            gesture = detect_gestures(landmarks_list)
            if gesture:
                message_display_time = time.time()
                device_state = magiq_control.get_device_state(devices[gesture])
                message = f'Switch {"on" if device_state == "1" else "off"} the {gesture}'

                if device_state == '0':
                    operate = magiq_control.device_on_off(devices[gesture], True)
                    if operate['code'] == '200':
                        result = f'{gesture} is turned On'
                    else:
                        result = 'Device operation failed'
                elif device_state == '1':
                    operate = magiq_control.device_on_off(devices[gesture], False)
                    if operate['code'] == '200':
                        result = f'{gesture} is turned Off'
                    else:
                        result = 'Device operation failed'

                message = result
                message_display_time = time.time()
                pause_until_time = time.time() + PAUSE_DURATION

            if message_display_time and time.time() - message_display_time < MESSAGE_DURATION:
                cv2.putText(frame, message, (50, frame.shape[0] - 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 255, 0), 2, cv2.LINE_AA)

            elif time.time() - pause_until_time < MONITORING_DELAY:
                # Show "Monitoring" after result for MONITORING_DELAY seconds
                cv2.putText(frame, "Monitoring", (50, frame.shape[0] - 50), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 255, 0), 2, cv2.LINE_AA)

            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
