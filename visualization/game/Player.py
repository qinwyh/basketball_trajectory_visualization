class Player():
    def __init__(self, player):
        self.id = int(player['id'])
        self.x = float(player['x'])
        self.y = float(player['y'])
        self.jersey = int(player['jersey'])
        self.color = player['color']