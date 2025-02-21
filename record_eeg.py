# Records 1000 samples and organizes them to dta and labels for the classifier to read

from pylsl import StreamInlet, resolve_byprop
import numpy as np
import time

print("Looking for an EEG stream...")

# Find the OpenBCI EEG stream by name
streams = resolve_byprop('name', 'obci_eeg1')

if not streams:
    print("Error: EEG stream 'obci_eeg1' not found!")
    exit()

inlet = StreamInlet(streams[0])  # Connect to the first matching stream
print("Connected to EEG stream!")

data = []
labels = []

print("Recording EEG data for calibration...")

try:
    for i in range(1000):  
        sample, timestamp = inlet.pull_sample()
        data.append(sample)

        # Alternate labels (adjust timing in practice)
        labels.append(1 if i % 10 < 5 else 0)

        print(f"Sample {i}: {sample}, Label: {labels[-1]}")
        time.sleep(0.01)

except KeyboardInterrupt:
    print("Recording stopped.")

np.save("eeg_data.npy", np.array(data))
np.save("labels.npy", np.array(labels))

print("Data saved as eeg_data.npy and labels.npy")
