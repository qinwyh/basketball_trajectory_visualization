from game.Constant import Constant
from game.Ball import Ball
from game.Player import Player
from game.Team import Team

class Moment():
    def __init__(self, moment, player_jersey):
        self.quarter = moment[0]
        self.game_clock = moment[2]
        self.shot_clock = moment[3]

        # Ball info
        ball_info = {'x': moment[5][0][2], 
                     'y': moment[5][0][3], 
                     'radius': moment[5][0][4]
                     }
        self.ball = Ball(ball_info)

        # Player info
        self.players = []
        team_id_set = set()
        for item in moment[5][1:]:
            team_id_set.add(item[0])
            color = Team.color_dict[item[0]][0]
            player = {'id':item[1], 
                      'x': item[2], 
                      'y':item[3], 
                      'jersey':player_jersey[item[1]], 
                      'color': color
                      }
            self.players.append(Player(player))
        
        # Team info
        self.teams = (Team(team_id_set.pop()), Team(team_id_set.pop()))


