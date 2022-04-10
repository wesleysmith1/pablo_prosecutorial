from otree.api import *



doc = """
This application provides a webpage instructing participants how to get paid.
Examples are given for the lab and Amazon Mechanical Turk (AMT).
"""


class Constants(BaseConstants):
    name_in_url = 'payment_info'
    players_per_group = None
    num_rounds = 1

    showup = cu(25)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    payment_round = models.IntegerField()
    final_payment = models.CurrencyField()


# FUNCTIONS
# PAGES
class PaymentInfo(Page):
    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        
        try:
            player.payment_round = participant.payment_round
            player.final_payment = participant.final_payment + Constants.showup
        except:
            player.payment_round = -1
            player.final_payment = -1 + Constants.showup

        return dict(redemption_code=participant.label or participant.code)

class FinalPage(Page):
    pass


page_sequence = [PaymentInfo, FinalPage]
