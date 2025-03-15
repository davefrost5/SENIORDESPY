from pylsl import StreamInlet, resolve_byprop
import time
import sys
# from gpiozero import Motor  # Commented out for no Raspberry Pi control

# --- Raspberry Pi Actuator Setup with gpiozero (Commented Out) ---
# actuator = Motor(forward=17, backward=18)  # GPIO pins 17 (open) and 18 (close)
# actuator.stop()  # Ensure actuator is stopped initially

# --- Function to Connect to Stream ---
def connect_to_stream():
    print("Looking for NeuroPype prediction stream...")
    streams = resolve_byprop('name', 'OutStream')
    if not streams:
        print("Error: Prediction stream 'OutStream-markers' not found! Ensure NeuroPype is running.")
        sys.exit(1)  # Exit with error code
    inlet = StreamInlet(streams[0])
    print("Connected to NeuroPype prediction stream 'OutStream-markers'!")
    return inlet

# --- Real-Time Detection with Alternating Logic ---
print("Starting real-time detection with alternating close/open signals...")
open_threshold = 0.6  # Above 0.6 = 'open'
close_threshold = 0.4  # Below 0.4 = 'close'
pause_duration = 10  # 10-second pause after each detection
# actuator_duration = 0.5  # Duration to activate actuator (adjust as needed)  # Commented out

try:
    while True:
        # Connect to stream anew each cycle
        inlet = connect_to_stream()
        
        # Phase 1: Wait for 'close' first
        print("Waiting for first 'close' signal (probability < 0.4)...")
        while True:
            try:
                prediction, timestamp = inlet.pull_sample(timeout=0.1)  # Short timeout to allow interrupt
                if prediction is None:  # No data received within timeout
                    continue
                prediction = prediction[0]
                
                if prediction < close_threshold:
                    print(f"Closed hand detected (probability: {prediction:.3f}) at {timestamp}")
                    # actuator.backward()  # Move actuator to 'close'  # Commented out
                    # time.sleep(actuator_duration)  # Brief activation  # Commented out
                    # actuator.stop()  # Stop actuator  # Commented out
                    break
                # Ignore values >= 0.4 (no action)
                time.sleep(0.1)  # Small delay to avoid flooding
            except KeyboardInterrupt:
                print("Interrupted during 'close' phase.")
                raise  # Re-raise to outer try block

        print(f"Pausing for {pause_duration} seconds (not reading signals)...")
        time.sleep(pause_duration)  # Complete pause, no signal reading
        
        # Reconnect to stream for 'open' phase
        inlet = connect_to_stream()
        
        # Phase 2: Wait for 'open'
        print("Waiting for first 'open' signal (probability > 0.6)...")
        while True:
            try:
                prediction, timestamp = inlet.pull_sample(timeout=0.1)  # Short timeout to allow interrupt
                if prediction is None:  # No data received within timeout
                    continue
                prediction = prediction[0]
                
                if prediction > open_threshold:
                    print(f"Open hand detected (probability: {prediction:.3f}) at {timestamp}")
                    # actuator.forward()  # Move actuator to 'open'  # Commented out
                    # time.sleep(actuator_duration)  # Brief activation  # Commented out
                    # actuator.stop()  # Stop actuator  # Commented out
                    break
                # Ignore values <= 0.6 (no action)
                time.sleep(0.1)  # Small delay to avoid flooding
            except KeyboardInterrupt:
                print("Interrupted during 'open' phase.")
                raise  # Re-raise to outer try block

        print(f"Pausing for {pause_duration} seconds (not reading signals)...")
        time.sleep(pause_duration)  # Complete pause, no signal reading

except KeyboardInterrupt:
    print("Stopped by user.")
    # actuator.stop()  # Ensure actuator stops on exit  # Commented out
    # print("Actuator stopped and cleaned up.")  # Commented out
    sys.exit(0)  # Clean exit