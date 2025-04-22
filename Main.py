import sys
import time

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication
from main_window import MainWindow

timer = QTimer()
counter = 0
speed = int(500)

def game_loop():
    global counter
    global speed

    if not window.is_game_over:
        window.move_snake()
        window.update()
    else:
        timer.stop()
        window.game_over_label.show()

    counter += 1
    if counter % 5 == 0 and speed > 100:
        speed = int(speed * 0.97)
        timer.setInterval(speed)


def initialize_app():
    global window # Declare the window global, so the initialize_app can modify it
    app = QApplication(sys.argv)
    window = MainWindow() # The main window should be initialized after QApplication initialization
    window.show()
    timer.timeout.connect(game_loop) # Reference only the game_loop() method without parentheses, so it is not called
                                     # immediately, only after the connect method calls it after timer timeout
    timer.start(500)
    sys.exit(app.exec_())


def main():
    initialize_app()

if __name__ == "__main__":
    main()