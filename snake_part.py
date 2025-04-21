
class SnakePart:

    def __init__(self, snake_pos_x, snake_pos_y):
        self.snake_pos_x = int(snake_pos_x)
        self.snake_pos_y = int(snake_pos_y)
        self.snake_previous_x = int(0)
        self.snake_previous_y = int(0)