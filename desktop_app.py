import threading
import webbrowser
import time
import sys
import os
import traceback
from waitress import serve

# Setup a crash log file right next to the executable
if getattr(sys, 'frozen', False):
    log_dir = os.path.dirname(sys.executable)
else:
    log_dir = os.path.dirname(os.path.abspath(__file__))

crash_log_path = os.path.join(log_dir, 'dbr_crash_log.txt')

def open_browser():
    time.sleep(1.5)
    webbrowser.open_new('http://127.0.0.1:8085/')

if __name__ == '__main__':
    try:
        from server import app
        
        print("Starting DBR Simulation Suite Engine...")
        print("DO NOT CLOSE this window until you are done simulating.")
        
        threading.Thread(target=open_browser, daemon=True).start()
        serve(app, host='127.0.0.1', port=8085)
        
    except Exception as e:
        # If the app completely fails to boot, write it to a text file!
        error_msg = traceback.format_exc()
        with open(crash_log_path, 'w') as f:
            f.write("=== DBR SIMULATOR CRASH LOG ===\n")
            f.write(error_msg)
            
        print(f"\n[FATAL STARTUP ERROR] App could not start.")
        print(f"Please send the '{crash_log_path}' file to the developer.")
        
        # Keep the terminal window open for 10 seconds so the user can read the error
        time.sleep(10)