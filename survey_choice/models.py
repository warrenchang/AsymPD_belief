from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

from otreeutils.surveys import create_player_model_for_survey, generate_likert_field, generate_likert_table
import random


author = 'Huanren Zhang'

doc = """
survey questions
"""


class Constants(BaseConstants):
    name_in_url = 'asldkja'
    players_per_group = None
    num_rounds = 1

class Subsession(BaseSubsession):
    def creating_session(self):
        for p in self.get_players():
            p.gain_framing = random.choice([0,1])


class Group(BaseGroup):
    pass


# some pre-defined choices

GENDER_CHOICES = (
    ('female', 'Female'),
    ('male', 'Male'),
    ('no_answer', 'Prefer not to answer'),
)

YESNO_CHOICES = (
    ('yes', 'Yes'),
    ('no', 'No'),
)

EBAY_ITEMS_PER_WEEK = (
    ('<5', 'less than 5'),
    ('5-10', 'between 5 and 10'),
    ('>10', 'more than 10'),
)

# define a Likert 5-point scale with its labels

likert_5_labels = (
    'Strongly disagree',
    'Disagree',
    'Neither agree nor disagree',
    'Agree',
    'Strongly agree'
)

likert_7_labels = (
    'Strongly Disagree',
    'Moderately Disagree',
    'Slightly Disagree',
    'Neutral',
    'Slightly Agree',
    'Moderately Agree',
    'Strongly Agree'
)

likert_5point_field = generate_likert_field(likert_5_labels)
likert_7point_field = generate_likert_field(likert_7_labels)


# define survey questions per page
# for each page define a page title and a list of questions
# the questions have a field name, a question text (input label), and a field type (model field class)
SURVEY_DEFINITIONS = (
    {
        'page_title': 'Please answer the following quesitons',
        'survey_fields': [  # you can also split questions into several forms for better CSS styling
            {
                # you need to provide a dict then. you can add more keys to the dict which are then available in the template
                'form_name': 'first_form',  # optional, can be used for CSS styling
                'fields': [
                    ('tp1', {
                        # 'text': 'A notebook and a pencil cost DKK 110 in total. The notebook costs DKK 100 more than the pencil. How much does the pencil cost in DKK?',
                        'text': 'Suppose you are offered an immediate payment of $80 or a delayed payment 30 days from now. How much would you need to be paid in 30 days in order to give up $80 immediately?',
                        'field': models.PositiveIntegerField(),
                    }),
                    ('tp2', {
                        'text': 'Suppose you are offered an immediate payment of $100 in 30 days or an even further delayed payment in 60 days. How much would you require to be paid in 60 days in order to give up $100 in 30 days?',
                        'field': models.PositiveIntegerField(),
                    }),
                ]
            },
        ]
    },

)

# now dynamically create the Player class from the survey definitions
# we can also pass additional (non-survey) fields via `other_fields`
Player = create_player_model_for_survey('survey_choice.models', SURVEY_DEFINITIONS, other_fields={
    'choice': models.IntegerField(choices=[[0, 'A'], [1, 'B']],widget=widgets.RadioSelectHorizontal),
    'gain_framing': models.BooleanField()
})


