from otree.api import *



class Constants(BaseConstants):
    name_in_url = 'survey'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    name = models.StringField(label="What is your name?")

    age = models.StringField(
        label='What is your age?',
        choices=['18-22', '23-30', '30-40', '40 and Above'],
        widget=widgets.RadioSelect,
        )
    gender = models.StringField(
        choices=['Male', 'Female', 'Other', 'Prefer not to answer'],
        label='What is your gender?',
        widget=widgets.RadioSelect,
    )
    race_ethnicity = models.StringField(
        label="What is your race or ethnicity?",
        choices=['White', 'Black or African American', 'Asian', 'Indian or Pacific Inslander', 'Hispanic', 'Other'],
        widget=widgets.RadioSelect,
    )
    field_major = models.StringField(
        label="What is your major or field of study?"
    )
    econ_courses = models.IntegerField(
        label="How many economics courses have you taken (including any in progress)?"
    )



# FUNCTIONS
# PAGES
class Survey(Page):
    form_model = 'player'
    form_fields = ['name', 'age', 'gender', 'race_ethnicity', 'field_major', 'econ_courses']


page_sequence = [Survey, ]
