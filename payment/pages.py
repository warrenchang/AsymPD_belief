from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants
import math


class EndInfo(Page):
    def vars_for_template(self):
        return {
            'total_payoff': self.participant.payoff,
        }

page_sequence = [
    EndInfo,
]
