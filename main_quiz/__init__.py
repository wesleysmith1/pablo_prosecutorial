from otree.api import *




doc = """
This bargaining game involves 2 players. Each demands for a portion of some
available amount. If the sum of demands is no larger than the available
amount, both players get demanded portions. Otherwise, both get nothing.
"""

from main import Constants as MainConstants


class Constants(BaseConstants):
    name_in_url = 'main_quiz'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass

class Player(BasePlayer):
    q1 = models.IntegerField(
        label="Suppose the PROPOSER chooses an INITIAL POSITION of 20, and an OFFER of 15. If the RESPONDER accepts this OFFER the round earnings are:",
        choices=[
            [1, 'PROPOSER earns 20, and the RESPONDER loses 20'],
            [2, 'PROPOSER earns 15, and the RESPONDER loses 15'],
            [3, 'PROPOSER earns 15, and the RESPONDER loses 20'],
            [4, 'PROPOSER earns 20, and the RESPONDER loses 15'],
        ],
        widget=widgets.RadioSelect,
    )
    q2 = models.IntegerField(
        label="Suppose the PROPOSER chooses an INITIAL POSITION of 40, and an OFFER of 30. The RESPONDER rejects this OFFER. The PROPOSER then chooses a FINAL POSITION of 35. The probability that the outcome is OUTCOME P is (BLANK) and the probability that the outcome is OUTCOME R is (BLANK).",
        choices=[
            [1, '35%, 45%'],
            [2, '35%, 60%'],
            [3, '15%, 65%'],
            [4, '65%, 35%'],

        ],
        widget=widgets.RadioSelect,
    )
    # phi = 1.5
    q3a = models.IntegerField(
        label="Suppose the PROPOSER chooses an INITIAL POSITION of 40, and an OFFER of 29. The RESPONDER rejects this OFFER. The PROPOSER then chooses a FINAL POSITION of 34. The probability that the outcome is OUTCOME P is 66% and the probability that the outcome is OUTCOME R is 34%. If the outcome that is chosen is OUTCOME P, the round earnings are:",
        choices=[
            [1, 'PROPOSER earns 24, and the RESPONDER loses 10'],
            [2, 'PROPOSER earns 41, and the RESPONDER loses 44'],
            [3, 'PROPOSER loses 41, and the RESPONDER earns 44'],
            [4, 'PROPOSER loses 41, and the RESPONDER loses 44'],
        ],
        widget=widgets.RadioSelect,
    )
    # phi = 1
    q3b = models.IntegerField(
        label="Suppose the PROPOSER chooses an INITIAL POSITION of 40, and an OFFER of 29. The RESPONDER rejects this OFFER. The PROPOSER then chooses a FINAL POSITION of 34. The probability that the outcome is OUTCOME P is 66% and the probability that the outcome is OUTCOME R is 34%. If the outcome that is chosen is OUTCOME P, the round earnings are:",
        choices=[
            [1, 'PROPOSER earns 24, and the RESPONDER loses 10'],
            [2, 'PROPOSER earns 24, and the RESPONDER loses 44'],
            [3, 'PROPOSER loses 24, and the RESPONDER earns 44'],
            [4, 'PROPOSER loses 24, and the RESPONDER loses 44']
        ],
        widget=widgets.RadioSelect,
    )
    q4a = models.IntegerField(
        label="Suppose the PROPOSER chooses an INITIAL POSITION of 40, what is the lowest number the FINAL POSITION could be? What is the highest?",
        choices=[
            [1, "8, 40"],
            [2, "40, 8"],
            [3, "35, 40"],
            [4, "40, 35"]
        ],
        widget=widgets.RadioSelect,
    )

    q4b = models.IntegerField(
        label="Suppose the PROPOSER chooses an INITIAL POSITION of 40, what is the lowest number the FINAL POSITION could be? What is the highest?",
        choices=[
            [1, "28, 40"],
            [2, "40, 28"],
            [3, "35, 40"],
            [4, "40, 35"]
        ],
        widget=widgets.RadioSelect,
    )

def q1_error_message(player, value):
    if value != 2:
        return 'Your answer was incorrect. Please try again.'

def q2_error_message(player, value):
    if value != 4:
        return 'Your answer was incorrect. Please try again.'

def q3a_error_message(player, value):
    if value != 2:
        return 'Your answer was incorrect. Please try again.'

def q3b_error_message(player, value):
    if value != 2:
        return 'Your answer was incorrect. Please try again.'

def q4a_error_message(player, value):
    if value != 1:
        return 'Your answer was incorrect. Please try again.'

def q4b_error_message(player, value):
    if value != 1:
        return 'Your answer was incorrect. Please try again.'



# PAGES
class ManualWait(Page):
    pass

class Quiz1(Page):
    form_model = 'player'
    form_fields = ['q1']

class Quiz2(Page):
    form_model = 'player'
    form_fields = ['q2']

class Quiz3(Page):
    form_model = 'player'
    if MainConstants.phi == 1.5:
        form_fields = ['q3a']
    elif MainConstants.phi == 1:
        form_fields = ['q3b']
    else:
        # error
        pass

class Quiz4(Page):
    form_model = 'player'
    if MainConstants.alpha[0] == .2:
        form_fields = ['q4a']
    elif MainConstants.alpha[0] == .7:
        form_fields = ['q4b']
    else:
        # error
        pass

class ManualWait2(Page):
    pass


page_sequence = [ManualWait, Quiz1, Quiz2, Quiz3, Quiz4, ManualWait2]
