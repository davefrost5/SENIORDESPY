#initial file made to move the motor (OUTDATED)

import joblib
import numpy as np
from pylsl import StreamInlet, resolve_stream
import RPi.GPIO as GPIO
import time

# Load trained classifier
clf = joblib.load("motor_classifier.pkl")

# Raspberry Pi GPIO setup
MOTOR_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTOR_PIN, GPIO.OUT)

pwm = GPIO.PWM(MOTOR_PIN, 50)
pwm.start(0)

# Resolve EEG stream
streams = resolve_stream('name', 'obci_eeg1')  # Connect to the correct OpenBCI LSL stream
inlet = StreamInlet(streams[0])

print("Listening for EEG signals...")

def move_motor(hand_open):
    duty_cycle = 7.5 if hand_open else 2.5
    pwm.ChangeDutyCycle(duty_cycle)
    print(f"Moving motor: {'Open' if hand_open else 'Closed'}")
    time.sleep(1)

try:
    while True:
        sample, _ = inlet.pull_sample()
        features = np.mean(sample)
        prediction = clf.predict([[features]])[0]

        move_motor(prediction == 1)

except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
