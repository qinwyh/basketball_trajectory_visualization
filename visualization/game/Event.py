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
    def __init__(self, game_id, event):
        self.id = event['eventId']
        self.visitor = event['visitor']['abbreviation']
        self.home = event['home']['abbreviation']
        self.meta_data, self.player_to_jersey = Event.extract_meta_data(event)
        self.moments = [Moment(moment, self.player_to_jersey) for moment in event['moments']]
        self.event_description = self.extract_event_description(game_id)

    def plot_events(self):
        fig = plt.figure(figsize=(4, 4), dpi=250)
        clock, play_ground, player_table = self.initialize(fig)
    
        # clock info and player info
        clock_info, player_circles, ball_circle, jerseys = self.plot_clock_and_ground(clock, play_ground)
        
        # table info
        self.plot_player_table(player_table)

        # animation
        ani = animation.FuncAnimation(
                        fig, self.update_moment,
                        fargs=(clock_info, player_circles, ball_circle, jerseys),
                        frames=len(self.moments), interval=Constant.INTERVAL)

        plt.show()
        

    def initialize(self, fig):
        # clock region
        clock = fig.add_axes([0, 0.95, 1, 0.05])
        clock.axis('off')
        clock.grid(False)

        # playground region
        play_ground = fig.add_axes([0, 0.3, 1, 0.6])
        play_ground.axis('off')
        play_ground.grid(False)
        play_ground.set_xlim([Constant.X_MIN - Constant.BORDER, Constant.X_MAX + Constant.BORDER])
        play_ground.set_ylim([Constant.Y_MIN - Constant.BORDER, Constant.Y_MAX + Constant.BORDER])

        # player table region
        player_table = fig.add_axes([0, 0, 1, 0.25])
        player_table.axis('off')
        player_table.grid(False)

        return clock, play_ground, player_table


    def plot_clock_and_ground(self, clock, play_ground):
        start_moment = self.moments[0]

        # clock info
        clock_info = clock.annotate("", xy=[Constant.X_CENTER, Constant.Y_CENTER], \
                                        color='black', horizontalalignment='center', \
                                        verticalalignment='center')
        
        # player info
        court = plt.imread(os.path.join("visualization", "image", "court.png"))
        play_ground.imshow(court, zorder=0, extent=[Constant.X_MIN, Constant.X_MAX,
                                                    Constant.Y_MIN, Constant.Y_MAX])
        jerseys = [play_ground.annotate("", xy=[0,0], color='white', fontweight='bold', \
                                            horizontalalignment='center', verticalalignment='center') \
                                            for _ in range(10)]
        player_circles = [plt.Circle((0,0), Constant.CIRCLE_SIZE, color=player.color)
                          for player in start_moment.players]
        ball_circle = plt.Circle((0,0), Constant.CIRCLE_SIZE, color=start_moment.ball.color)

        for circle in player_circles:
            play_ground.add_patch(circle)
        play_ground.add_patch(ball_circle)

        return clock_info, player_circles, ball_circle, jerseys
    

    def plot_player_table(self, player_table):
        start_moment = self.moments[0]

        home_players = [self.meta_data['players'][player.id] for player in start_moment.players \
                        if player.id in self.meta_data['home']]
        guest_players = [self.meta_data['players'][player.id] for player in start_moment.players \
                        if player.id in self.meta_data['visitor']]
        players = [home_players[i] + guest_players[i] for i in range(len(home_players))]

        column_labels = ('Pos', 'No.', self.home, 'Pos', 'No.', self.visitor)
        column_colors = tuple([Team.team_dict[self.home]]*3 + [Team.team_dict[self.visitor]]*3)
        column_widths = [Constant.NUMBER_WIDTH, Constant.NUMBER_WIDTH, Constant.NAME_WIDTH] * 2
        cell_colors = [column_colors] * 5

        table = player_table.table(cellText=players, colLabels=column_labels, colColours=column_colors, \
                                   colWidths=column_widths, loc='center', cellColours=cell_colors, \
                                   fontsize=Constant.FONTSIZE, cellLoc='center', )
        for i in range(6):
            for j in range(6):
                table[(i, j)].get_text().set_color('white')
    

    def update_moment(self, index, clock_info, player_circles, ball_circle, jerseys):
        moment = self.moments[index]

        # set clock info
        clock_text = "{}\n Quarter {:d}\n Game: {:02d}:{:02d}\n Shot:{:03.1f}".format(
                      self.event_description,
                      moment.quarter,
                      int(moment.game_clock) // 60,
                      int(moment.game_clock) % 60,
                      moment.shot_clock)   
        clock_info.set_text(clock_text)

        # set player info
        for i, circle in enumerate(player_circles):
            circle.center = moment.players[i].x, moment.players[i].y
            jerseys[i].set_text(moment.players[i].jersey)
            jerseys[i].set_position(circle.center)
        
        ball_circle.center = moment.ball.x, moment.ball.y
        ball_circle.radius = moment.ball.radius / Constant.BALL_COEF


    def extract_event_description(self, game_id):
        home_description = ""
        guest_description = ""
        with open(os.path.join("data", "events", game_id + ".csv"), "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['EVENTNUM'] == self.id:
                    home_description = row['HOMEDESCRIPTION']
                    guest_description = row['VISITORDESCRIPTION']
                    break
        
        if len(home_description) > 0 and len(guest_description) > 0:
            return home_description + " and " + guest_description
        else:
            return home_description + guest_description

    @staticmethod
    def extract_meta_data(event):
        home_players = event['home']['players']
        guest_players = event['visitor']['players']
        home_id = [player['playerid'] for player in home_players]
        guest_id = [player['playerid'] for player in guest_players]

        players = home_players + guest_players
        player_ids = [player['playerid'] for player in players]
        player_names = [" ".join((player['firstname'], player['lastname'])) for player in players]
        jerseys = [player['jersey'] for player in players]
        positions = [player['position'] for player in players]

        meta_data =  {'home': home_id, 'visitor': guest_id, 
                    'players': dict(zip(player_ids, zip(positions, jerseys, player_names)))}
        
        player_to_jersey = {player['playerid']: player['jersey'] for player in players}

        return meta_data, player_to_jersey    

        


if __name__ == '__main__':
    with open(os.path.join("data", "0021500226.json"), "r") as f:
        raw_data = json.load(f)

    event = Event(raw_data['gameid'], raw_data['events'][87])
    print(event.id)
    print(len(raw_data['events'][87]['home']['players']))
    print(event.event_description)
    event.plot_events()
    