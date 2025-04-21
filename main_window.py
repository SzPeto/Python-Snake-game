import random
from typing import List

from PyQt5.QtGui import QGuiApplication, QPainter, QColor, QKeyEvent
from PyQt5.QtWidgets import QWidget
from snake_part import SnakePart

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        from Main import is_game_over

        # Variable declarations
        self.window_width = int(810)
        self.window_height = int(810)
        self.setWindowTitle("Snake game")
        self.snake_size = 30
        self.food_size = 30
        self.initial_snake_x = 0
        self.initial_snake_y = 0
        self.screen = QGuiApplication.primaryScreen().geometry()
        self.direction = 1  # 1: UP, 2: DOWN, 3: LEFT, 4: RIGHT
        self.snake: List[SnakePart] = [] # This is how to define the type of empty list
        self.food_x = 0
        self.food_y = 0
        self.create_food()

        # Method calls
        self.center_window()
        self.initUI()
        self.set_initial_snake_position()
        self.snake.append(SnakePart(self.initial_snake_x, self.initial_snake_y))

    # Master methods *******************************************************************************************
    def initUI(self):
        self.setStyleSheet("background-color: rgb(225, 225, 255);")

    def center_window(self):
        extra_width = self.frameSize().width() - self.width() # Frame width
        extra_height = self.frameSize().height() - self.height() # Title bar plus frame height
        self.screen_width = self.screen.width()
        self.screen_height = self.screen.height()
        window_x = int((self.screen_width - self.window_width + extra_width) / 2)
        window_y = int((self.screen_height - self.window_height + extra_height) / 2)
        # You have to add here the extra widthfor the playboard size to have the defined dimensions
        self.setFixedSize(self.window_width + extra_width, self.window_height + extra_height)
        self.setGeometry(window_x, window_y, self.window_width + extra_width, self.window_height + extra_height)

    def paintEvent(self, a0):
        painter = QPainter(self)
        painter.setBrush(QColor("green"))
        painter.setPen(QColor(225, 225, 255))

        for i in range(0, len(self.snake)):
            painter.drawRect(self.snake[i].snake_pos_x, self.snake[i].snake_pos_y,
                             self.snake_size, self.snake_size)

        painter.setBrush(QColor("red"))
        painter.drawRect(self.food_x, self.food_y, self.food_size, self.food_size)

    # Overriding the keyPressEvent
    def keyPressEvent(self, event: QKeyEvent):
        if event.nativeVirtualKey() == 38:
            self.direction = 1
        elif event.nativeVirtualKey() == 40:
            self.direction = 2
        elif event.nativeVirtualKey() == 37:
            self.direction = 3
        elif event.nativeVirtualKey() == 39:
            self.direction = 4

    # Other methods ********************************************************************************************
    def move_snake(self):
        if self.direction == 1:
            for i in range(0, len(self.snake)):
                if i == 0:
                    self.save_previous(i)
                    self.snake[i].snake_pos_y = self.snake[i].snake_pos_y - self.snake_size
                else:
                    self.save_previous(i)
                    self.move_tail(i)
        elif self.direction == 2:
            for i in range(0, len(self.snake)):
                if i == 0:
                    self.save_previous(i)
                    self.snake[i].snake_pos_y = self.snake[i].snake_pos_y + self.snake_size
                else:
                    self.save_previous(i)
                    self.move_tail(i)
        elif self.direction == 3:
            for i in range(0, len(self.snake)):
                if i == 0:
                    self.save_previous(i)
                    self.snake[i].snake_pos_x = self.snake[i].snake_pos_x - self.snake_size
                else:
                    self.save_previous(i)
                    self.move_tail(i)
        elif self.direction == 4:
            for i in range(0, len(self.snake)):
                if i == 0:
                    self.save_previous(i)
                    self.snake[i].snake_pos_x = self.snake[i].snake_pos_x + self.snake_size
                else:
                    self.save_previous(i)
                    self.move_tail(i)
        if self.snake[0].snake_pos_x == self.food_x and self.snake[0].snake_pos_y == self.food_y:
            self.add_snake_part()
            self.create_food()

    def add_snake_part(self):
        last_part_index = len(self.snake) - 1
        current_x = int(self.snake[last_part_index].snake_previous_x)
        current_y = int(self.snake[last_part_index].snake_previous_y)
        self.snake.append(SnakePart(current_x, current_y))

    def create_food(self):
        temp_x = random.randint(0, self.window_width - self.snake_size)
        temp_y = random.randint(0, self.window_height - self.snake_size)
        self.food_x = int(temp_x - temp_x % self.food_size)
        self.food_y = int(temp_y - temp_y % self.food_size)

    def set_initial_snake_position(self):
        temp_x = (self.width() - self.snake_size) / 2
        temp_y = (self.height() - self.snake_size) / 2
        self.initial_snake_x = int( temp_x - (temp_x % self.snake_size) )
        self.initial_snake_y = int(temp_y - (temp_y % self.snake_size))

    def save_previous(self, i):
        self.snake[i].snake_previous_x = self.snake[i].snake_pos_x
        self.snake[i].snake_previous_y = self.snake[i].snake_pos_y

    def move_tail(self, i):
        self.snake[i].snake_pos_x = self.snake[i - 1].snake_previous_x
        self.snake[i].snake_pos_y = self.snake[i - 1].snake_previous_y