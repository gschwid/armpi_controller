import sys
sys.path.append('/home/ubuntu/Ai_FPV/HiwonderSDK')
import Board
import time
from pynput import keyboard, mouse
import threading


def my_function():
    pulse = 500
    for i in range(5):
        Board.setBusServoPulse(id, pulse, 100)
        print("Hello from a thread!")

thread = threading.Thread(target=my_function, daemon=True)
thread.start()

for i in range(5):
    print("other loop")