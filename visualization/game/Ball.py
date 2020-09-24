class Ball():
    def __init__(self, ball):
        self.x = float(ball['x'])
        self.y = float(ball['y'])
        self.radius = float(ball['radius'])
        self.color = '#ff8c00'  