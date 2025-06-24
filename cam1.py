import subprocess

def start_camera():
    """Start live camera stream."""
    print("Starting camera stream... Press Ctrl+C to stop.")
    command = [
        "libcamera-vid",
        "--camera", "0",  # Use camera index 0
        "--width", "640",
        "--height", "480",
        "-t", "0"  # Run indefinitely
    ]
    try:
        subprocess.run(command)
    except KeyboardInterrupt:
        print("\nCamera stream stopped.")

if __name__ == "__main__":
    while True:
        user_input = input("Enter 'start' to begin the livestream or 'exit' to quit: ").strip().lower()
        if user_input == "start":
            start_camera()
        elif user_input == "exit":
            print("Exiting program.")
            break
        else:
            print("Invalid command. Type 'start' or 'exit'.")
