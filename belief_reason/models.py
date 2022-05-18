from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from otreeutils.surveys import create_player_model_for_survey, generate_likert_field, generate_likert_table
import random

author = 'Huanren Zhang'

doc = """
Guess participants' reason for defection after mutual cooperation, also elicit second order belief
"""


class Constants(BaseConstants):
    name_in_url = 'dbaehoe'
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
        'EQ-H': [97,97],
        'EQ-L': [97,97],
        'UNEQ': [90,87],
    }
    action_labels = ['C','D']  # labels for the player's actions


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass

# define a Likert 5-point scale with its labels
likert_6_labels = (
    '1. Not Important At All',
    '2',
    '3',
    '4',
    '5',
    '6. Very Important',
)


likert_6point_field = generate_likert_field(likert_6_labels)
# define survey questions per page
# for each page define a page title and a list of questions
# the questions have a field name, a question text (input label), and a field type (model field class)
SURVEY_DEFINITIONS = (
    {
        'page_title': '',
        'survey_fields': [
            # create a table of Likert scale choices
            # we use the same 5-point scale a before and specify four rows for the table,
            # each with a tuple (field name, label)
            ## Big-five (OCEAN: Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism)
            generate_likert_table(likert_6_labels,
                                  [
                                      ('inequality_aversion', "They disliked the unequal payoff between them and Player 1"),
                                      ('other_defection', "They believed that Player 1 would choose D"),
                                      ('higher_payoff', "They wanted to receive a higher payoff"),

                                  ],
                                  form_help_initial='<p>Now consider <b>Player 2</b> who chose D in a round after both players chose' +
                                                    ' C in the previous round. What do you think are the reasons that led Player 2' +
                                                    ' to choose D? On a scale of 1 to 6 (1 indicates <b>Not Important At All </b> w'
                                                    'hile 6 indicate <b>Very Important</b>), ' +
                                                    'rate the importance of the following reasons.</p>',
                                  # HTML to be placed on top of form
                                  form_help_final='<p></p>',  # HTML to be placed below form
                                  table_row_header_width_pct=50,
                                  # width of row header (first column) in percent. default: 25
                                  table_rows_randomize=True,  # randomize order of displayed rows
                                  ),
        ]
    },
    {
        'page_title': '',
        'survey_fields': [
            # create a table of Likert scale choices
            # we use the same 5-point scale a before and specify four rows for the table,
            # each with a tuple (field name, label)
            ## Big-five (OCEAN: Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism)
            generate_likert_table(likert_6_labels,
                                  [
                                      ('inequality_aversionc',
                                       "They disliked the unequal payoff between them and Player 1"),
                                      ('other_defectionc', "They believed that Player 1 would choose D"),
                                      ('higher_payoffc', "They wanted to receive a higher payoff"),

                                  ],
                                  form_help_initial='<p>In the next task, <b>you will guess the most common ratings provided by ' +
                                                    'all the participants for each of the reasons that Player 2 chose D in the previous question</b>. '+
                                                    'For each reason, if your guess correctly the most common rating, you will receive an additional payment of €2'+
                                                    ' (up to up to €6 in this task). '+
                                                    'In order to receive the payment, it is important to indicate what you think most other participants '+
                                                    'have chosen in the previous question.</p>' +


                                                    '<p>Your earnings for this part will be determined at the end of experiment, after all the participants '+
                                                    'in this experiment have rated the importance of each reason.</p>' +

                                                    '<p>Now choose what you think most participants have rated reach of the reasons '+
                                                    'for which Player 2 decided to choose D in a round after both players chose C in the previous round.</p>',

                                  # HTML to be placed on top of form
                                  form_help_final='<p></p>',  # HTML to be placed below form
                                  table_row_header_width_pct=50,
                                  # width of row header (first column) in percent. default: 25
                                  table_rows_randomize=True,  # randomize order of displayed rows
                                  ),
        ]
    },

)

# now dynamically create the Player class from the survey definitions
# we can also pass additional (non-survey) fields via `other_fields`
Player = create_player_model_for_survey('belief_reason.models', SURVEY_DEFINITIONS, other_fields={
    'correct_guesses': models.IntegerField(),
    'dropout': models.BooleanField(initial=0),
}
                                        )


# class Player(BasePlayer):
#     inequality_aversion = models.PositiveIntegerField()
#     other_defection = models.PositiveIntegerField()
#     higher_payoff = models.PositiveIntegerField()
#     inequality_aversionc = models.PositiveIntegerField()
#     other_defectionc = models.PositiveIntegerField()
#     higher_payoffc = models.PositiveIntegerField()


