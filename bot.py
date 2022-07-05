from pynput import mouse, keyboard
from enum import Enum
from PIL import ImageGrab
import time
import sys

class Color(Enum):
    Grey = 1
    Yellow = 2
    Green = 3

class Bot:
    """

    """

    # Constructor + Member Variables
    def __init__(self, ostream=sys.stdout) -> None:
        self.grid_pixels: list[list[tuple]] = []
        self.output_stream = ostream

        # Variables for internal communication
        self.found_chars = [False for i in range(0, 5)]
        self.attempt_result = [Color.Grey for i in range(0, 5)]

        # Read in from the CSV file
        self.word_bank = []


    # Member Functions
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


    def _solve(self) -> None:
        guess = "salet"
        
        # for attempt_num in range(0, 6):
        #     # do the algorithm
        #     pass

        self._sendKBInput(guess)
        time.sleep(2.5)
        self._recordResults(0)
        print(self.attempt_result)
    

    def _sendKBInput(self, word: str) -> None:
        kb = keyboard.Controller()
        for char in word:
            kb.press(char)
            kb.release(char)
        kb.press(keyboard.Key.enter)
        kb.release(keyboard.Key.enter)


    def _recordResults(self, rowNum: int) -> None:
        GREEN = (83, 141, 78)
        YELLOW = (181, 159, 59)
        GREY = (58, 58, 60)
        CLR_CODES = [GREEN, YELLOW, GREY]

        screenshot = ImageGrab.grab().load()

        for i in range(0, len(self.grid_pixels[rowNum])):
            coord = self.grid_pixels[rowNum][i]
            pix_color = screenshot[coord[0], coord[1]]

            # determine similarity to each color
            distances = []
            for color in CLR_CODES:
                distances.append((color[0] - pix_color[0])**2 + (color[1] 
                                 - pix_color[1])**2 + (color[2] - pix_color[2])**2)

            min_idx = distances.index(min(distances))

            if min_idx == 0:
                # Green
                self.attempt_result[i] = Color.Green
                self.found_chars[i] = True
            elif min_idx == 1:
                # yellow
                self.attempt_result[i] = Color.Yellow
            else:
                # grey
                self.attempt_result[i] = Color.Grey


    def _updateWordBank(self, guessed: str) -> None:
        pass


    # Public Functions
    def run(self) -> None:
        self._calibrate()
        self._solve()


protoBot = Bot()
protoBot.run()