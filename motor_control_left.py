#file made 2/21 to test motor (static data)

import joblib
import numpy as np
import time
#from gpiozero import Servo

# Load the trained classifier
clf = joblib.load("motor_classifier.pkl")

# Set up the servo motor
#servo = Servo(12)

# Load the EEG data
X = np.load("eeg_data.npy")
y = np.load("labels.npy")

# Preprocessing: Simple feature extraction (mean per channel)
X = np.mean(X, axis=1)

# Predict movements based on EEG data
predictions = clf.predict(X)

# Function to move the motor for left-hand signals
'''
def move_motor_left():
    servo.value = 0.2  # Move to position for LEFT thought
    time.sleep(3)      # Keep motor in position for 3 seconds
    print(f"Motor moved to position {servo.value}")
    servo.detach()     # Detach to stop the motor from staying in place
    time.sleep(2)
'''
# Iterate through the predictions and control the motor
for i, prediction in enumerate(predictions):
    if prediction == 0:  # Assuming 0 = LEFT
        print(f"Sample {i + 1}: LEFT thought detected - Moving motor")
        #move_motor_left()
    else:
        print(f"Sample {i + 1}: RIGHT thought detected - No motor action")

# Cleanup after execution
#servo.detach()
