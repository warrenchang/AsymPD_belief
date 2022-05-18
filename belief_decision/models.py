from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from otreeutils.surveys import create_player_model_for_survey, generate_likert_field, generate_likert_table
import random

author = 'Huanren Zhang'

doc = """
Guess participants' decision in another experiment, first need to pass a quiz
"""


class Constants(BaseConstants):
    name_in_url = 'dskljoe'
    players_per_group = None
    num_rounds = 1

    instructions_template = 'belief_decision/instructions_template.html'
    quiz_template = 'belief_decision/quiz_info.html'
    # payoff matrix for each interaction
    payoff_matrix = {
        'EQ-H': [[9,0,10,3],[9,0,10,3]],
        'EQ-L': [[6,0,10,3],[6,0,10,3]],
        'UNEQ': [[9,0,10,3],[6,0,10,3]],
    }
    percentages = {
        'EQ-H': 3,
        'EQ-L': 3,
        'UNEQ': [10,13],
    }
    action_labels = ['C','D']  # labels for the player's actions


class Subsession(BaseSubsession):
    def creating_session(self):
        # starting_time = time.time()
        self.session.vars['num_groups'] = 0
        for p in self.get_players():
            treatment = self.session.config.get('treatment', '')
            if treatment == '':
                p.treatment = ['UNEQ','EQ-H','EQ-L','UNEQ'][p.participant.id_in_session%4]
            else:
                p.treatment = treatment
            p.participant.vars['treatment'] = p.treatment


class Group(BaseGroup):
    pass



class Player(BasePlayer):
    treatment = models.StringField()
    wrong_attempts = models.PositiveIntegerField(initial=0)   # number of wrong attempts on understanding questions page
    percentage1 = models.IntegerField(min=0,max=100)
    percentage2 = models.IntegerField(min=0,max=100)
    p1correct = models.PositiveIntegerField()
    p2correct = models.PositiveIntegerField()
    dropout = models.BooleanField(initial=0)

    # pmat = models.StringField() # payoff matrix used in the quiz
    # qualified = models.BooleanField(initial=False)
    # decision_time = models.IntegerField()  # decision time in seconds

    def live_attempt(self, data):
        if data != 'initialization':
            self.wrong_attempts += 1
        print('received message from page', data)
        print({self.id_in_group: self.wrong_attempts})
        return {self.id_in_group: self.wrong_attempts}
