import sys
import time

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication
from main_window import MainWindow

is_game_over = False
timer = QTimer()

def game_loop():
    window.move_snake()
    window.update()

def initialize_app():
    global window # Declare the window global, so the game_loop can access it
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