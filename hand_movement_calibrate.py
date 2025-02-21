#lab recording file to connect to np

from pylsl import StreamInfo, StreamOutlet
import time

# Create a new LSL stream for markers
info = StreamInfo('MotorImag-Markers', 'Markers', 1, 0, 'string')  # Updated stream name
outlet = StreamOutlet(info)

# Number of trials for each class
num_trials = 15

print("Starting calibration...")

for i in range(num_trials):
    # Send 'left' marker
    print("Imagine LEFT hand movement")
    outlet.push_sample(['left'])
    time.sleep(3)  # 5 seconds for imagining

    # Send 'right' marker
    print("Imagine RIGHT hand movement")
    outlet.push_sample(['right'])
    time.sleep(3)  # 5 seconds for imagining

print("Calibration complete. Close Lab Recorder.")
