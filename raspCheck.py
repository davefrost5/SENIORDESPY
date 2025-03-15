import paramiko
import time

# --- Raspberry Pi Connection Details ---
PI_HOST = "100.65.46.51"  # Replace with your Pi's IP address (e.g., "192.168.1.100")
PI_USERNAME = "syncd"        # Replace with your Pi's username if different
PI_PASSWORD = "syncd" # Replace with your Pi's password
PI_FOLDER_PATH = "/home/syncd/test_folder"  # Path for the new folder on the Pi

# --- Function to Connect to Raspberry Pi via SSH ---
def connect_to_pi(host, username, password):
    try:
        print(f"Connecting to Raspberry Pi at {host}...")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Auto-accept host key
        ssh.connect(host, username=username, password=password)
        print("Successfully connected to Raspberry Pi!")
        return ssh
    except Exception as e:
        print(f"Failed to connect to Raspberry Pi: {e}")
        return None

# --- Function to Create a Folder on the Pi ---
def create_folder(ssh, folder_path):
    if ssh is None:
        print("No SSH connection available.")
        return
    
    try:
        command = f"mkdir {folder_path}"
        print(f"Creating folder at {folder_path}...")
        stdin, stdout, stderr = ssh.exec_command(command)
        
        # Wait for the command to complete
        time.sleep(1)  # Brief delay to ensure execution
        
        # Check for errors
        error = stderr.read().decode().strip()
        if error:
            print(f"Error creating folder: {error}")
        else:
            print(f"Folder created successfully at {folder_path}!")
        
        # Verify folder creation
        stdin, stdout, stderr = ssh.exec_command(f"ls -d {folder_path}")
        output = stdout.read().decode().strip()
        if output:
            print(f"Verified: {output} exists.")
        else:
            print("Folder verification failed.")
            
    except Exception as e:
        print(f"Error during folder creation: {e}")

# --- Main Execution ---
if __name__ == "__main__":
    # Update this with your Pi's IP address
    PI_HOST = input("Enter your Raspberry Pi's IP address (e.g., 192.168.1.100): ").strip()
    
    # Connect to the Pi
    ssh_client = connect_to_pi(PI_HOST, PI_USERNAME, PI_PASSWORD)
    
    # Create the folder
    if ssh_client:
        create_folder(ssh_client, PI_FOLDER_PATH)
        
        # Clean up
        ssh_client.close()
        print("SSH connection closed.")