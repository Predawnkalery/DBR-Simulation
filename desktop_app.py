# desktop_app.py
import threading
import webbrowser
import time
from server import app
from waitress import serve

def open_browser():
    # Wait 1.5 seconds to ensure the server is fully booted before opening the tab
    time.sleep(1.5)
    webbrowser.open_new('http://127.0.0.1:8085/')

if __name__ == '__main__':
    print("Starting DBR Simulation Suite Engine...")
    print("DO NOT CLOSE this window until you are done simulating.")
    
    # Open the user's default web browser in a background thread
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Run the rock-solid Waitress production server on the main thread
    serve(app, host='127.0.0.1', port=8085)