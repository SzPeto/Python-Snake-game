import random
from typing import List

from PyQt5.QtGui import QGuiApplication, QPainter, QColor, QKeyEvent
from PyQt5.QtWidgets import QWidget, QLabel
from snake_part import SnakePart

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        # Variable declarations
        self.is_game_over = False
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
        self.game_over_label = QLabel("Game over!", self)

        # Method calls
        self.center_window()
        self.initUI()
        self.set_initial_snake_position()
        self.snake.append(SnakePart(self.initial_snake_x, self.initial_snake_y))

    # Master methods *******************************************************************************************
    def initUI(self):
        self.setStyleSheet("background-color: rgb(225, 225, 255);")
        self.game_over_label.setFixedSize(300, 200)
        self.game_over_label.setGeometry( int((self.width() - self.game_over_label.width()) / 2),
                                          int((self.height() - self.game_over_label.height()) / 2),
                                          self.game_over_label.width(), self.game_over_label.height())
        self.game_over_label.setStyleSheet("font-family: Bahnschrift; font-size: 50px; color: rgb(255, 100, 100);"
                                           "font-weight: bold;")
        self.game_over_label.hide()

    def center_window(self):
        extra_width = self.frameSize().width() - self.width() # Frame width
        extra_height = self.frameSize().height() - self.height() # Title bar plus frame height
        self.screen_width = self.screen.width()
        self.screen_height = self.screen.height()
        window_x = int((self.screen_width - self.window_width + extra_width) / 2)
        window_y = int((self.screen_height - self.window_height + extra_height) / 2)
        # You have to add here the extra width for the playboard size to have the defined dimensions
        self.setFixedSize(self.window_width + extra_width, self.window_height + extra_height)
        self.setGeometry(window_x, window_y, self.window_width + extra_width, self.window_height + extra_height)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QColor("green"))
        painter.setPen(QColor(225, 225, 255))

        for i in range(0, len(self.snake)):
            painter.drawRect(self.snake[i].snake_pos_x, self.snake[i].snake_pos_y,
                             self.snake_size, self.snake_size)

        painter.setBrush(QColor("red"))
        painter.drawRect(self.food_x, self.food_y, self.food_size, self.food_size)

    # Overriding the keyPressEvent, the : QKeyEvent sets the type of event variable
    def keyPressEvent(self, event: QKeyEvent):
        if event.nativeVirtualKey() == 38:
            if self.direction != 2:
                self.direction = 1
        elif event.nativeVirtualKey() == 40:
            if self.direction != 1:
                self.direction = 2
        elif event.nativeVirtualKey() == 37:
            if self.direction != 4:
                self.direction = 3
        elif event.nativeVirtualKey() == 39:
            if self.direction != 3:
                self.direction = 4

    # Other methods ********************************************************************************************
    def move_snake(self):
        if self.direction == 1:
            for i in range(0, len(self.snake)):
                if i == 0:
                    self.save_previous(i)
                    if self.snake[i].snake_pos_y == 0:
                        self.snake[i].snake_pos_y = self.height() - self.snake_size
                    else:
                        self.snake[i].snake_pos_y = self.snake[i].snake_pos_y - self.snake_size
                else:
                    self.save_previous(i)
                    self.move_tail(i)
        elif self.direction == 2:
            for i in range(0, len(self.snake)):
                if i == 0:
                    self.save_previous(i)
                    if self.snake[i].snake_pos_y == self.height() - self.snake_size:
                        self.snake[i].snake_pos_y = 0
                    else:
                        self.snake[i].snake_pos_y = self.snake[i].snake_pos_y + self.snake_size
                else:
                    self.save_previous(i)
                    self.move_tail(i)
        elif self.direction == 3:
            for i in range(0, len(self.snake)):
                if i == 0:
                    self.save_previous(i)
                    if self.snake[i].snake_pos_x == 0:
                        self.snake[i].snake_pos_x = self.width() - self.snake_size
                    else:
                        self.snake[i].snake_pos_x = self.snake[i].snake_pos_x - self.snake_size
                else:
                    self.save_previous(i)
                    self.move_tail(i)
        elif self.direction == 4:
            for i in range(0, len(self.snake)):
                if i == 0:
                    self.save_previous(i)
                    if self.snake[i].snake_pos_x == self.width() - self.snake_size:
                        self.snake[i].snake_pos_x = 0
                    else:
                        self.snake[i].snake_pos_x = self.snake[i].snake_pos_x + self.snake_size
                else:
                    self.save_previous(i)
                    self.move_tail(i)

        # Condition for creating food
        if self.snake[0].snake_pos_x == self.food_x and self.snake[0].snake_pos_y == self.food_y:
            self.add_snake_part()
            self.create_food()

        # Collision detection of snake
        for i in range(1, len(self.snake)):
            if (self.snake[0].snake_pos_x == self.snake[i].snake_pos_x and
                self.snake[0].snake_pos_y == self.snake[i].snake_pos_y):
                self.is_game_over = True

    def add_snake_part(self):
        last_part_index = len(self.snake) - 1
        current_x = int(self.snake[last_part_index].snake_previous_x)
        current_y = int(self.snake[last_part_index].snake_previous_y)
        self.snake.append(SnakePart(current_x, current_y))

    def create_food(self):
        valid_food_position = False
        while not valid_food_position:
            checker = True
            temp_x = random.randint(0, self.window_width - self.snake_size)
            temp_y = random.randint(0, self.window_height - self.snake_size)
            self.food_x = int(temp_x - temp_x % self.food_size)
            self.food_y = int(temp_y - temp_y % self.food_size)

            # Checking if the food isn't placed into snake
            for i in range(0, len(self.snake)):
                if (self.food_x == self.snake[i].snake_pos_x and
                    self.food_y == self.snake[i].snake_pos_y):
                    checker = False
            if checker: valid_food_position = True


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