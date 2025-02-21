#displayus real time predictions
# display_predictions.py
from pylsl import StreamInlet, resolve_byprop

# Step 1: Resolve EEG prediction stream
print("Looking for EEG stream output from Neuropype...")
streams = resolve_byprop('name', 'obci_eeg1')

# Step 2: Connect to the first stream found
inlet = StreamInlet(streams[0])
print("Connected to EEG stream. Listening for predictions...")

# Step 3: Continuously listen for data and print it
try:
    while True:
        # Receive predictions (assuming integer output: 0 for left, 1 for right)
        sample, timestamp = inlet.pull_sample()
        
        # Interpret and display the result
        if sample:
            command = int(sample[0])
            if command == 0:
                print(f"[{timestamp}] Detected Thought: LEFT")
            elif command == 1:
                print(f"[{timestamp}] Detected Thought: RIGHT")
            else:
                print(f"[{timestamp}] Unknown Signal: {command}")
except KeyboardInterrupt:
    print("Stopped listening.")
