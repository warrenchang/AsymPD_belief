from otree.api import Currency as c, currency_range
from . import models
from otreeutils.pages import AllGroupsWaitPage, ExtendedPage, UnderstandingQuestionsPage, APPS_DEBUG
from otreeutils.surveys import SurveyPage, setup_survey_pages
from ._builtin import Page, WaitPage
from .models import Constants
import settings


def vars_for_all_templates(self):
    pmat = Constants.payoff_matrix[self.player.treatment]
    return {
        'pmat': pmat,
    }



class StartPage(Page):
    def vars_for_template(self):
        return {
            'payment_currency': self.session.config.get('payment_currency','$'),
            'showup_fee': self.session.config.get('showup_fee',5),
        }


class Instructions(Page):
    pass



class SomeUnderstandingQuestions(UnderstandingQuestionsPage):
    page_title = ''
    extra_info = Constants.instructions_template
    quiz_info = Constants.quiz_template
    set_correct_answers = True    # this is the default setting
    # set_correct_answers = False  # do not fill out the correct answers in advance (this is for fast skipping through pages)
    form_model = 'player'
    form_field_n_wrong_attempts = 'wrong_attempts'
    live_method = 'live_attempt'

    # def get_timeout_seconds(self):
    #     return self.session.config.get('quiz_minutes', 5)*60

    def get_questions(self):
        pmat = Constants.payoff_matrix[self.player.treatment]
        possible_payoffs = list(set(sum(pmat,[])))
        options = [
            'Player 1 chooses C, Player 2 chooses C',
            'Player 1 chooses C, Player 2 chooses D',
            'Player 1 chooses D, Player 2 chooses C',
            'Player 1 chooses D, Player 2 chooses D',
        ]
        questions = [
            {
                'question': "What is Player 2's payoff if Player 1 chooses D and Player 2 chooses C?",
                'options': possible_payoffs,
                'correct': 0,
            },
            {
                'question': "What is the highest possible payoff that Player 2 can get?",
                'options': possible_payoffs,
                'correct': 10,
            },
            {
                'question': "What does the two players receive the highest joint payoff?",
                'options': options,
                'correct': 'Player 1 chooses C, Player 2 chooses C',
            },
            {
                'question': "What does the two players receive the lowest joint payoff?",
                'options': options,
                'correct': 'Player 1 chooses D, Player 2 chooses D',
            },
            {
                'question': "After the players play a round, what is the chance that the game will continue for another round?",
                'options': ['0%','16%','20%','50%','80%','100%'],
                'correct': '80%',
            },
        ]
        return questions

    def extra_vars_for_template(self):
        pmat = Constants.payoff_matrix[self.player.treatment]
        # print('Payoff matrix:  ',pmat)
        return {
            'pmat': pmat,
        }


class QuizResults(Page):
    pass


class BeliefDecisionEQ(Page):
    form_model = 'player'
    form_fields = ['percentage1']

    def vars_for_template(self):
        return {
            'payment_per_decision': self.session.config.get('payment_per_decision',2),
            'payment_currency': getattr(settings, 'REAL_WORLD_CURRENCY_CODE', '$'),
        }

    def is_displayed(self):
        print(self.player,self.player.treatment)
        return (self.player.treatment == 'EQ-H') or (self.player.treatment == 'EQ-L')

    def before_next_page(self):
        self.player.dropout = self.timeout_happened
        if not self.player.dropout:
            tolerance = self.session.config.get('guess_tolerence',2)
            self.player.p1correct = abs(self.player.percentage1-Constants.percentages[self.player.treatment])<=tolerance
            self.participant.vars['paymentI'] = self.player.p1correct*self.session.config.get('payment_per_decision',2)
            self.player.payoff += self.participant.vars['paymentI']


class BeliefDecisionUNEQ(Page):
    form_model = 'player'
    form_fields = ['percentage1','percentage2']

    def vars_for_template(self):
        return {
            'payment_per_decision': self.session.config.get('payment_per_decision',2),
            'payment_currency': getattr(settings, 'REAL_WORLD_CURRENCY_CODE', '$'),
        }

    def is_displayed(self):
        return (self.player.treatment == 'UNEQ')

    def before_next_page(self):
        self.player.dropout = self.timeout_happened
        if not self.player.dropout:
            tolerance = self.session.config.get('guess_tolerence',2)
            self.player.p1correct = abs(self.player.percentage1-Constants.percentages['UNEQ'][0])<=tolerance
            self.player.p2correct = abs(self.player.percentage2-Constants.percentages['UNEQ'][1])<=tolerance
            self.participant.vars['paymentI'] = (self.player.p1correct*self.session.config.get('payment_per_decision',2)
                                   + self.player.p2correct*self.session.config.get('payment_per_decision',2))
            self.player.payoff += self.participant.vars['paymentI']


page_sequence = [
    StartPage,
    Instructions,
    SomeUnderstandingQuestions,
    QuizResults,
    BeliefDecisionEQ,
    BeliefDecisionUNEQ,
]

