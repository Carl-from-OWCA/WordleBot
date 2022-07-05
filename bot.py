from pynput import mouse, keyboard
import sys

class Bot:
    """

    """

    # Constructor + Member Variables
    def __init__(self, ostream=sys.stdout) -> None:
        self.grid_pixels: list[list[tuple]] = []
        self.output_stream = ostream

    # Private Functions
    def _calibrate(self) -> None:
        """
        After this function is called, self.grid_pixels should be a 6x5
        nested list, where each element contains the coordinates of the pixel
        from the wordle square of the corresponding index. This function can
        use a lot of work to make the process easier.
        """

        # Setup for kb + mouse monitoring
        clickLog: list[tuple] = []
        keepLooping: bool = True

        def on_click(x, y, button, pressed):
            nonlocal clickLog
            if (button == mouse.Button.left) and (not pressed):
                if len(clickLog) < 30:
                    clickLog.append((x, y))
                else:
                    print("Already recorded all 30 points", file=self.output_stream)

        ms_listener = mouse.Listener(on_click=on_click)
        
        def on_press(key):
            nonlocal keepLooping, ms_listener
            if key == keyboard.Key.ctrl_l:
                clickLog.clear()
                if not (ms_listener.is_alive()):
                    ms_listener.start()
            elif (key == keyboard.Key.alt_l):
                if len(clickLog) != 30:
                    print("Please finish calibrating", file=self.output_stream)
                else:
                    ms_listener.stop()
                    keepLooping = False
                
        kb_listener = keyboard.Listener(on_press=on_press)

        # Start the input monitors
        kb_listener.start()
        print("Press 'Ctrl' key to start calibration or reset. " 
            + "Then click on the top left corner of each square "
            + "Press 'Alt' to finish calibration."
            , file=self.output_stream)

        # Stall so the other threads keep running
        while keepLooping:
            pass
        kb_listener.stop()

        # Set the global variable based on recorded data
        self.grid_pixels.clear()
        for i in range(0, 6):
            self.grid_pixels.append([])
            for j in range(0, 5):
                self.grid_pixels[i].append(clickLog.pop(0))

        # Print self.grid_pixels for debugging
        for i in range(0, 6):
            for j in range(0, 5):
                print("[",self.grid_pixels[i][j][0], ",", self.grid_pixels[i][j][1],"]", end=" ", file=self.output_stream)
            print("", file=self.output_stream)


    def _solve(self) -> None:
        pass

    # Public Functions
    def run(self) -> None:
        self._calibrate()
        self._solve()


protoBot = Bot()
protoBot.run()