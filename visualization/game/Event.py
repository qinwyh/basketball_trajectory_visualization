import os
import json
import csv
import sys

import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.patches import Circle, Rectangle, Arc

sys.path.append('visualization')

from game.Constant import Constant
from game.Team import Team
from game.Moment import Moment


class Event():
    def __init__(self, event):
        self.id = event['eventId']
        self.visitor = event['visitor']['abbreviation']
        self.home = event['home']['abbreviation']
        self.meta_data, self.player_jersey = extract_meta_data(event)
        self.moments = [Moment(moment, self.player_jersey) for moment in event['moments']]


    def plot_moment(self):
        ax = plt.axes(xlim=(Constant.X_MIN, Constant.X_MAX),
                      ylim=(Constant.Y_MIN, Constant.Y_MAX))
        ax.axis('off')
        ax.grid(False)
        fig = ax.gcf()

        start_moment = self.moments[0]





def extract_meta_data(event):
    home_players = event['home']['players']
    guest_players = event['visitor']['players']
    home_player_names = [" ".join((player['firstname'], player['lastname'])) for player in home_players]
    guest_player_names = [" ".join((player['firstname'], player['lastname'])) for player in guest_players]
    home_id = [player['playerid'] for player in home_players]
    guest_id = [player['playerid'] for player in guest_players]
    home_jersey = [player['jersey'] for player in home_players]
    guest_jersey = [player['jersey'] for player in guest_players]
    home_position = [player['position'] for player in home_players]
    guest_position = [player['position'] for player in guest_players]

    meta_data =  {'home': zip(home_id, home_player_names, home_jersey, home_position),
                    'visitor': zip(guest_id, guest_player_names, guest_jersey, guest_position)}
    
    players = event['home']['players'] + event['visitor']['players']
    player_jersey = {player['playerid']: player['jersey'] for player in players}

    return meta_data, player_jersey    


if __name__ == '__main__':
    with open(os.path.join("data", "0021500226.json"), "r") as f:
        raw_data = json.load(f)
    