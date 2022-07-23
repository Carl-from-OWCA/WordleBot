## Wordle Bot
#### By: Raghav Varshney

This is a bot that can play wordle for you on your computer. It will be able to simulate keyboard input to send guesses to the game window, and then it will be able to scan the screen to see the results of each guess. Based on the results, it will update the list of words that could be potential solutions. The first time you use the bot you will have to calibrate it (for which it will give you instructions). On subsequent runs, you can choose to use the saved calibration data. Do note that if the layout or colors of the game window changes, the bot will need to be recalibrated. 

If you plan on running this bot on multiple different interfaces, I recommend saving a copy of the "calibration_data.csv" file in a separate folder with some indication of what specific interface it's for. Then when you want to switch interfaces (ie, go from NYT to wordlegame.org), simply take the "calibration_data.csv" file corresponding to that interface and move it back into the folder with the Python scripts.

Requirements:
* Python 3
* pynput (library)
* PIL (library)
