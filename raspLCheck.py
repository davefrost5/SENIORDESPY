from pylsl import StreamInlet, resolve_byprop
import time
import sys
import paramiko

# --- Raspberry Pi SSH Connection Details ---
PI_HOST = "100.65.46.51"      # Pi's IP address
PI_USERNAME = "syncd"            # Replace if different
PI_PASSWORD = "syncd"     # Replace with your Pi's password
PI_SCRIPT_PATH = "/home/syncd/SYNCdWork/circuitwork.py"  # Path to the script on the Pi

# --- SSH Client Setup ---
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# --- Function to Connect to Raspberry Pi via SSH ---
def connect_to_pi():
    try:
        print(f"Connecting to Raspberry Pi at {PI_HOST}...")
        ssh.connect(PI_HOST, username=PI_USERNAME, password=PI_PASSWORD, timeout=10)
        print("Connected to Raspberry Pi via SSH!")
    except Exception as e:
        print(f"Failed to connect to Pi: {e}")
        sys.exit(1)

# --- Function to Run Script on Pi ---
def run_pi_script():
    try:
        print(f"Running {PI_SCRIPT_PATH} on the Raspberry Pi...")
        stdin, stdout, stderr = ssh.exec_command(f"python3 {PI_SCRIPT_PATH}")
        time.sleep(1)  # Give it a moment to start
        error = stderr.read().decode().strip()
        if error:
            print(f"Error running script: {error}")
        else:
            print(f"Successfully triggered {PI_SCRIPT_PATH}!")
    except Exception as e:
        print(f"Error triggering script: {e}")

# --- Function to Connect to LSL Stream ---
def connect_to_stream():
    print("Looking for NeuroPype prediction stream...")
    streams = resolve_byprop('name', 'OutStream')
    if not streams:
        print("Error: Prediction stream 'OutStream-markers' not found! Ensure NeuroPype is running.")
        sys.exit(1)
    inlet = StreamInlet(streams[0])
    print("Connected to NeuroPype prediction stream 'OutStream-markers'!")
    return inlet

# --- Real-Time Detection ---
print("Starting real-time detection for 'close' signal...")
close_threshold = 0.4  # Below 0.4 = 'close'

# Connect to Pi once at startup
connect_to_pi()

try:
    inlet = connect_to_stream()
    print("Waiting for first 'close' signal (probability < 0.4)...")
    while True:
        try:
            prediction, timestamp = inlet.pull_sample(timeout=0.1)
            if prediction is None:
                continue
            prediction = prediction[0]
            
            if prediction < close_threshold:
                print(f"Closed hand detected (probability: {prediction:.3f}) at {timestamp}")
                run_pi_script()  # Trigger the script on the Pi
                while True:  # Keep running after triggering (adjust as needed)
                    time.sleep(1)
            time.sleep(0.1)
        except KeyboardInterrupt:
            print("Interrupted by user.")
            raise

except KeyboardInterrupt:
    print("Stopped by user.")
    ssh.close()
    sys.exit(0)