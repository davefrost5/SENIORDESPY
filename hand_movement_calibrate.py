from pylsl import StreamInfo, StreamOutlet
import time

# Create a new LSL stream for markers
info = StreamInfo('MotorImag-Markers', 'Markers', 1, 0, 'string')
outlet = StreamOutlet(info)

# Number of trials for each class
num_trials = 15

# Add rest period between trials
rest_duration = 2  # seconds

print("Starting calibration for Open vs. Closed Hand Imagery...")

for i in range(num_trials):
    # Rest period before each trial
    print("Resting...")
    time.sleep(rest_duration)

    # Send 'open' marker
    print("Imagine OPEN hand movement (right hand)")
    outlet.push_sample(['open'])
    time.sleep(3)  # 3 seconds for imagining

    # Rest period
    print("Resting...")
    time.sleep(rest_duration)

    # Send 'close' marker
    print("Imagine CLOSE hand movement (right hand)")
    outlet.push_sample(['close'])
    time.sleep(3)  # 3 seconds for imagining

print("Calibration complete. Close Lab Recorder.")