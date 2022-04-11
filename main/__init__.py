
from otree.api import *

import numpy as np
import random

import config

doc = """
One player decides how to divide a certain amount between himself and the other
player.
See: Kahneman, Daniel, Jack L. Knetsch, and Richard H. Thaler. "Fairness
and the assumptions of economics." Journal of business (1986):
S285-S300.
"""


class Constants(BaseConstants):
    name_in_url = 'main'
    players_per_group = 2
    num_rounds = 30

    # charge variable interval
    c_lower = 0
    c_upper = 100

    # treatment variables
    phi = 1 # 1.5
    # alpha = [.2, .7]
    alpha = [.7, .2]

    # instructions_template = 'main/instructions.html'
    # Initial amount allocated to the dictator

    i = 'I'
    l = 'L'

    offer_initpos_ceiling = 100

    currency_unit = ''
    conversion_rate = 1/5

    trial_cost = 10


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    initial_position = models.FloatField(min=Constants.c_lower, max=Constants.c_upper)
    offer = models.FloatField(label="What charge/sentence will you offer as a plea bargain?", min=Constants.c_lower, max=Constants.c_upper)
    offer_accepted = models.BooleanField()
    final_position = models.FloatField()
    guilty_at_trial = models.BooleanField(doc="True: OUTCOME P, False: OUTCOME R")
    phi = models.FloatField(initial=Constants.phi)


class Player(BasePlayer):
    alpha = models.FloatField()
    payoff_points = models.FloatField(initial=0)

##################################################################################################

# FUNCTIONS
def is_responder(player: Player):
    return player.id_in_group == 1

def creating_session(subsession):
    subsession.group_randomly()

    payment_round = random.randint(0, Constants.num_rounds)
    # generate I box money 
    for player in subsession.get_players():
        player.participant.payment_round = payment_round

        if player.round_number <= Constants.num_rounds / 2:
            player.alpha = Constants.alpha[0]
        else:
            player.alpha = Constants.alpha[1]

def p(c):
    """probability defendent found guilty at trial"""
    return 1 - c/100

def simulate_trial(p):
    """return true if innocent, false for guilty"""
    return bool(np.random.binomial(1, p))

def record_payoff(player: Player):
    """record payment if current round is selected for payment"""
    if player.participant.payment_round == player.round_number:
        player.participant.final_payment = player.payoff_points * Constants.conversion_rate

##################################################################################################            

# PAGES
class InitialPosition(Page):
    form_model = 'group'
    form_fields = ['initial_position']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(alpha=player.alpha)

    @staticmethod
    def is_displayed(player: Player):
        return not is_responder(player)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        group = player.group
        

class ChargeWait(WaitPage):
    pass

class Offer(Page):
    form_model = 'group'
    form_fields = ['offer']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            lower=round(player.alpha * player.group.initial_position, 2),
            upper=player.group.initial_position,
            )

    @staticmethod
    def is_displayed(player: Player):
        return not is_responder(player)

class OfferWait(WaitPage):
    pass

class OfferDecision(Page):
    form_model = 'group'
    form_fields = ['offer_accepted']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            alpha=player.alpha,
            lower=round(player.alpha * player.group.initial_position, 2),
            upper=player.group.initial_position,
            )

    @staticmethod
    def is_displayed(player: Player):
        return is_responder(player)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        group = player.group

        if not is_responder(player):
            return

        responder = player
        proposer = player.get_others_in_group()[0]

        if group.offer_accepted:
            # round is over

            # calculate PLEA ACCEPTED payoffs
            responder.payoff_points = -group.offer
            proposer.payoff_points = group.offer


class OfferDecisionWait(WaitPage):
    pass

# if plea deal is rejected
class OfferRejected(Page):
    form_model = 'group'
    form_fields = ['final_position']

    @staticmethod
    def is_displayed(player: Player):
        return not is_responder(player) and not player.group.offer_accepted

    # simulate_trial
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        group = player.group

        # probability defendant found guilty at trial
        prob = p(group.final_position)
        group.guilty_at_trial = simulate_trial(prob)

        proposer = player
        responder = player.get_others_in_group()[0]

        # trial fee
        proposer.payoff_points -= Constants.trial_cost
        responder.payoff_points -= Constants.trial_cost

        if not group.guilty_at_trial:
            #innocent
            responder.payoff_points -= 0

            proposer.payoff_points -= group.final_position
        else:
            #guilty
            responder.payoff_points -= group.final_position
            
            proposer.payoff_points += group.phi * group.final_position

        # round payoffs
        responder.payoff_points = round(responder.payoff_points, 2)
        proposer.payoff_points = round(proposer.payoff_points, 2)

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
                alpha=player.alpha,
                lower=round(player.alpha * player.group.initial_position, 2),
                upper=player.group.initial_position,
            )


class OfferRejectedWait(WaitPage):
    pass


class FeedbackProposerAccepted(Page):

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
                responder_payoff=player.get_others_in_group()[0].payoff_points,
                alpha=player.alpha,
                lower=round(player.alpha * player.group.initial_position, 2),
                upper=player.group.initial_position,
            )
    
    @staticmethod
    def is_displayed(player: Player):
        return not is_responder(player) and player.group.offer_accepted
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        record_payoff(player)

class FeedbackProposerRejected(Page):

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
                responder_payoff=player.get_others_in_group()[0].payoff_points,
                alpha=player.alpha,
                lower=round(player.alpha * player.group.initial_position, 2),
                upper=player.group.initial_position,
            )
    
    @staticmethod
    def is_displayed(player: Player):
        return not is_responder(player) and not player.group.offer_accepted

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        record_payoff(player)


class FeedbackResponderAccepted(Page):

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
                proposers_payoff=player.get_others_in_group()[0].payoff_points,
                alpha=player.alpha,
                lower=round(player.alpha * player.group.initial_position, 2),
                upper=player.group.initial_position,
            )
    
    @staticmethod
    def is_displayed(player: Player):
        return is_responder(player) and player.group.offer_accepted

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        record_payoff(player)


class FeedbackResponderRejected(Page):

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
                proposers_payoff=player.get_others_in_group()[0].payoff_points,
                alpha=player.alpha,
                lower=round(player.alpha * player.group.initial_position, 2),
                upper=player.group.initial_position,
            )
    
    @staticmethod
    def is_displayed(player: Player):
        return is_responder(player) and not player.group.offer_accepted

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        record_payoff(player)


class AlphaWait(Page):
    
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == Constants.num_rounds / 2



page_sequence = [InitialPosition, ChargeWait, Offer, OfferWait, OfferDecision, OfferDecisionWait, OfferRejected, OfferRejectedWait, FeedbackProposerAccepted, FeedbackProposerRejected, FeedbackResponderAccepted, FeedbackResponderRejected, AlphaWait]
