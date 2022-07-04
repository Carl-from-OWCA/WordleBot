from pynput import mouse, keyboard

# Global variables for the module
clickLog: list[tuple] = []
stayLooping: bool = True

def on_click(x, y, button, pressed):
    global clickLog
    if (button == mouse.Button.left) and (not pressed):
        if len(clickLog) < 2:
            clickLog.append({x, y})
        else:
            print("Already recorded 2 points")

ms_listener = mouse.Listener(on_click=on_click)
    
def on_press(key):
    global stayLooping, ms_listener
    if key == keyboard.Key.ctrl_l:
        clickLog.clear()
        if not (ms_listener.is_alive()):
            ms_listener.start()
    elif (key == keyboard.Key.alt_l):
        if len(clickLog) != 2:
            print("Please finish calibrating")
        else:
            ms_listener.stop()
            stayLooping = False
        
kb_listener = keyboard.Listener(on_press=on_press)



# Basically a do-while loop to kick things off:
kb_listener.start()
print("Press 'Ctrl' key to start calibration or reset. " 
      + "First click on the top left corner of the grid. "
      + "Then click on the bottom right corner of the grid. "
      + "Press 'Alt' to finish calibration.")
while stayLooping:
    # Stall so the other threads keep running
    pass
kb_listener.stop()

print(clickLog)

