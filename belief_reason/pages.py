from otree.api import Currency as c, currency_range
from . import models
from otreeutils.pages import AllGroupsWaitPage, ExtendedPage, UnderstandingQuestionsPage, APPS_DEBUG
from otreeutils.surveys import SurveyPage, setup_survey_pages
from ._builtin import Page, WaitPage
from .models import Constants
import random
import settings


# def vars_for_all_templates(self):
#     pmat = Constants.payoff_matrix[self.player.treatment]
#     return {
#         'pmat': pmat,
#     }


class SurveyPage1(SurveyPage):
    # timeout_seconds = 900
    debug_fill_forms_randomly = True   # enable random data input if APPS_DEBUG is True

    def is_displayed(self):
        # print('SurveyPage2',self.participant.vars['treatment'],self.participant.vars['treatment'] == 'UNEQ')
        return self.participant.vars['treatment'] == 'UNEQ'

    def before_next_page(self):
        if self.timeout_happened:
            self.player.dropout = 1




class SurveyPage2(SurveyPage):
    # timeout_seconds = 900
    debug_fill_forms_randomly = True   # enable random data input if APPS_DEBUG is True

    def is_displayed(self):
        # print('SurveyPage2',self.participant.vars['treatment'],self.participant.vars['treatment'] == 'UNEQ')
        return (self.participant.vars['treatment'] == 'UNEQ')and(self.player.dropout==0)


class ResultsWaitPage(WaitPage):
    template_name = 'belief_reason/ResultsWaitPage.html'

    def after_all_players_arrive(self):
        players = [p for p in self.subsession.get_players() if (p.participant.vars['treatment']=='UNEQ')&(p.dropout==0)]
        ltemp = [p.inequality_aversion for p in players]
        inequality_aversion = (max(set(ltemp), key=ltemp.count))
        ltemp = [p.other_defection for p in players]
        other_defection = (max(set(ltemp), key=ltemp.count))
        ltemp = [p.higher_payoff for p in players]
        higher_payoff = (max(set(ltemp), key=ltemp.count))
        print(players)
        print(inequality_aversion,other_defection,higher_payoff)
        for p in players:
            p.correct_guesses = ((p.inequality_aversionc == inequality_aversion)
                                + (p.other_defectionc == other_defection)
                                + (p.higher_payoffc == higher_payoff))
            p.participant.vars['paymentII'] = p.correct_guesses*self.session.config.get('payment_per_reason',1)
            p.payoff += p.participant.vars['paymentII']
            print('ResultsWaitPage',p,p.correct_guesses,p.participant.vars.get('paymentII', 0))

    def is_displayed(self):
        return self.participant.vars['treatment'] == 'UNEQ'

    def vars_for_template(self):
        paymentI = self.participant.vars.get('paymentI',0)
        participation_fee = self.session.config['participation_fee']

        return {
            'participation_fee': participation_fee,
            'paymentI': paymentI,
            'real_currency': getattr(settings, 'REAL_WORLD_CURRENCY_CODE', '$'),
        }



class PaymentInfo(Page):
    def vars_for_template(self):
        paymentI = self.participant.vars.get('paymentI', 0)
        paymentII = self.participant.vars.get('paymentII', 0)
        participation_fee = self.session.config['participation_fee']
        final_payment = paymentI + paymentII + participation_fee
        treatment = self.participant.vars.get('treatment','EQ-H')

        p = self.player
        print('PaymentInfo',p,p.correct_guesses,p.participant.vars.get('paymentII', 0),paymentII)

        return {
            'participation_fee': participation_fee,
            'paymentI': paymentI,
            'paymentII': paymentII,
            'real_currency': getattr(settings, 'REAL_WORLD_CURRENCY_CODE', '$'),
            'final_payment': final_payment,
            'treatment': treatment,
        }


survey_pages = [
    SurveyPage1,
    SurveyPage2,
]

# Common setup for all pages (will set the questions per page)
setup_survey_pages(models.Player, survey_pages)
page_sequence = []
page_sequence.extend(survey_pages)

additional_pages = [ResultsWaitPage,PaymentInfo]
page_sequence.extend(additional_pages)