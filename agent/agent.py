import socketio
import mss
import cv2
import numpy as np
import base64
import pyautogui
import time
import threading

# IMPORTANT: Put your Railway URL here!
SERVER_URL = "https://YOUR_RAILWAY_URL_HERE.up.railway.app" 

# Disable failsafe so you can move the mouse to the very edges of the screen
pyautogui.FAILSAFE = False

sio = socketio.Client()

@sio.event
def connect():
    print("✅ Connected to Railway Server!")
    sio.emit('register_host')

@sio.on('mouse_move')
def on_mouse_move(data):
    # Convert percentages back to actual screen pixels
    screen_w, screen_h = pyautogui.size()
    abs_x = int(data['x'] * screen_w)
    abs_y = int(data['y'] * screen_h)
    pyautogui.moveTo(abs_x, abs_y)

@sio.on('mouse_click')
def on_mouse_click(data):
    pyautogui.click(button=data['button'])

@sio.on('key_press')
def on_key_press(data):
    key = data['key']
    try:
        # Standardize some keys
        if key == 'enter': pyautogui.press('enter')
        elif key == 'backspace': pyautogui.press('backspace')
        elif key == ' ': pyautogui.press('space')
        else: pyautogui.press(key)
    except Exception as e:
        pass

def stream_screen():
    with mss.mss() as sct:
        monitor = sct.monitors[1] # Primary monitor
        while True:
            if sio.connected:
                # Capture screen
                img = np.array(sct.grab(monitor))
                # Resize to 720p for faster internet streaming
                img = cv2.resize(img, (1280, 720))
                
                # Compress into JPEG
                _, buffer = cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 40])
                jpg_as_text = base64.b64encode(buffer).decode('utf-8')
                
                # Send to Railway
                sio.emit('screen_frame', jpg_as_text)
            
            # Stream at roughly 20 Frames Per Second
            time.sleep(0.05) 

if __name__ == '__main__':
    print(f"Connecting to {SERVER_URL}...")
    sio.connect(SERVER_URL)
    
    # Run the video stream in the background
    thread = threading.Thread(target=stream_screen)
    thread.daemon = True
    thread.start()
    
    sio.wait()
