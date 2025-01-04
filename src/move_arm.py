import sys
sys.path.append('/home/ubuntu/Ai_FPV/HiwonderSDK')
import Board
import time
from pynput import keyboard, mouse

# Code to control the armpi arm with mouse and keyboard

keys_held = []
pulse_values = [500,500,500,500,500,500]
mouse_held = [False, False]
mouse_coords = [[0,0],[0,0]] # Left is previous value, right is new one

def keyboard_on_press(key):
	if key.char not in keys_held:
		keys_held.append(key.char)
			
def keyboard_on_release(key):
	keys_held.remove(key.char)
	Board.stopBusServo(6)

def mouse_on_move(x, y):
	if mouse_coords[0] == [0,0]: # default
		mouse_coords[0] = [x,y]
		mouse_coords[1] = [x,y]
	
	mouse_coords[0] = mouse_coords[1]
	mouse_coords[1] = [x,y]

def update_mouse_position():
	mouse_coords[0] = mouse_coords[1]

def mouse_on_click(x, y, button, pressed):
	if str(button) == "Button.left":
		if pressed:
			mouse_held[0] = True
		else:
			mouse_held[0] = False
	elif str(button) == "Button.right":
		if pressed:
			mouse_held[1] = True
		else:
			mouse_held[1] = False

def handle_key(letter): # Set to -1 to counteract 0 based indexing
	if letter == 'a':
		id = 6
		update_pulse_value(id, True)
		pulse = pulse_values[id - 1]
		Board.setBusServoPulse(id, pulse, 100)
	elif letter == 'd':
		id = 6
		update_pulse_value(id, False)
		pulse = pulse_values[id - 1]
		Board.setBusServoPulse(id, pulse, 100)
	time.sleep(0.1)

def handle_mouse_click():
	left = mouse_held[0]
	right = mouse_held[1]
	id = 1
	if left:
		update_pulse_value(id, False)
		pulse = pulse_values[id - 1]
		Board.setBusServoPulse(id, pulse, 100)
	if right:
		update_pulse_value(id, True)
		pulse = pulse_values[id - 1]
		Board.setBusServoPulse(id, pulse, 100)
	time.sleep(0.1)

def handle_mouse_movement():
	previous = mouse_coords[0]
	current = mouse_coords[1]
	id = 2
	if current[0] > previous[0]:
		update_pulse_value(id, False)
		pulse = pulse_values[id - 1]
		Board.setBusServoPulse(id, pulse, 100)
	elif current[0] < previous[0]:
		update_pulse_value(id, True)
		pulse = pulse_values[id - 1]
		Board.setBusServoPulse(id, pulse, 100)
	id = 3
	if current[1] > previous[1]:
		update_pulse_value(id, False)
		pulse = pulse_values[id - 1]
		Board.setBusServoPulse(id, pulse, 100)
	elif current[1] < previous[1]:
		update_pulse_value(id, True)
		pulse = pulse_values[id - 1]
		Board.setBusServoPulse(id, pulse, 100)
	time.sleep(0.1)

			
def update_pulse_value(id, positive):
	id = id - 1
	PULSE_INCREASE = 20
	pulse = pulse_values[id]
	if pulse < 1000 and pulse > 0:
		if positive:
			pulse += PULSE_INCREASE
		else:
			pulse -= PULSE_INCREASE
	pulse_values[id] = pulse

def initialize():
	for i in range(1,7):
		Board.setBusServoPulse(i, 500, 500)
	
if __name__ == '__main__':

	# pynput code to listen for keyboard inputs
	keyboard_listener = keyboard.Listener(
			on_press = keyboard_on_press,
			on_release = keyboard_on_release)
	keyboard_listener.start()

	# pynput code to listen for mouse inputs
	mouse_listener = mouse.Listener(
			on_click = mouse_on_click,
			on_move = mouse_on_move)
	mouse_listener.start()

	initialize()

	while True:

		if mouse_held[0] or mouse_held[1]:
			handle_mouse_click()
		if mouse_coords[0] != mouse_coords[1]:
			handle_mouse_movement()	
		#todo: Turn this into a function
		if len(keys_held) > 0:
			key = keys_held[-1]
			handle_key(key)
		#print(mouse_coords)

		update_mouse_position()

			
	
