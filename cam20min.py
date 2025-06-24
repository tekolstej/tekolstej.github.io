import subprocess
import time
import datetime
import os

# Set the directory to save images
SAVE_DIR = "/home/jtk/captured_images"

# Ensure the directory exists
os.makedirs(SAVE_DIR, exist_ok=True)

# Capture image function
def capture_image():
    """Capture an image using libcamera-jpeg and save it with a timestamp."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    image_path = os.path.join(SAVE_DIR, f"image_{timestamp}.jpg")
    
    command = [
        "libcamera-jpeg",
        "-o", image_path,
        "--width", "1920",
        "--height", "1080"
    ]
    
    subprocess.run(command)
    print(f"Captured: {image_path}")

# Main loop to run from 9:00 AM to 3:00 PM, Monday to Friday
def main():
    print("Timelapse script started... Press Ctrl+C to stop.")
    
    while True:
        now = datetime.datetime.now()
        # Check if the current time is within the scheduled window (Monday-Friday, 9:00 AM - 3:00 PM)
        if now.weekday() < 5 and 9 <= now.hour < 15:  # Monday (0) to Friday (4)
            capture_image()
        
        # Wait 20 minutes (1200 seconds) before capturing again
        time.sleep(1200)

if __name__ == "__main__":
    main()
