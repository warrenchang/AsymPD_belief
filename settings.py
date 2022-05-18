from os import environ

# the environment variable OTREE_PRODUCTION controls whether Django runs in
# DEBUG mode. If OTREE_PRODUCTION==1, then DEBUG=False
if environ.get('OTREE_PRODUCTION') not in {None, '', '0'}:
    APPS_DEBUG = False
else:
    APPS_DEBUG = True

# setting for integration with AWS Mturk
AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')

Qid_qual = '3RM888DJP83NA9MT64121KG66XX2F1' # Qualification of being able to participate an experiment at a specific time
Qid_preferences = '3KVW4MB3P584GRBMDJDG682UC8SXJD' # Qualification ID of Preferences
Qid_games = '3T04ZEB6XS3KDFO8D7H8LQ8RTR95AQ' # Qualification ID of Preferences
Qid_coopetition = '355NDHMUE4408REV3XQ8DXPSH6SCF1'  # Qualification ID of Coopetition
Qid_games = '355NDHMUE4408REV3XQ8DXPSH6SCF1'  # Qualification ID of Coopetition
Qid_qual_sandbox = '39GW9SGGAEVYK6G7KXZV3IVP28GROX' # Qualification of being able to participate an experiment at a specific time
Qid_coopetition_sandbox = '3KPASCSMA0FIAKFOHBY5SS3J0R98H3'
Qid_preferences_sandbox = '3F97VQZTZ52G8HM1KEZAOKL8XI1HUS'
Qid_games_sandbox = '38CFB6RWNQR7NMC9VPCCXY3J39IVK9'
Test_workerids = ['A2J47PTIYO03TZ','A38IOZBVC9FXFJ']


SESSION_CONFIGS = [
    {
        'name': "EQ_UNEQ",
        'display_name': 'Guess Decisions',
        'num_demo_participants': 4,
        'debug': APPS_DEBUG,
        'participation_fee': 5,
        'guess_tolerance': 2, # difference allowed from the correct guess
        'payment_per_decision': 2,
        'payment_per_reason': 1,
        'payment_currency': '€',
        'app_sequence': [
            'belief_decision',
            'belief_reason'
        ],
    },
    # {
    #     'name': 'EQ_H',
    #     'display_name': "EQ_H",
    #     'num_demo_participants': 2,
    #     'treatment': 'EQ-H',  # points for each correct answer
    #     'app_sequence': [
    #        'coordination'
    #     ],
    # },
    # {
    #     'name': 'EQ_L',
    #     'display_name': "EQ-L",
    #     'num_demo_participants': 2,
    #     'treatment': 'EQ-L',  # points for each correct answer
    #     'app_sequence': [
    #         'coordination'
    #     ],
    # },
    # {
    #     'name': 'UNEQ',
    #     'display_name': "UNEQ",
    #     'num_demo_participants': 2,
    #     'treatment': 'UNEQ',  # points for each correct answer
    #     'app_sequence': [
    #         'coordination'
    #     ],
    # },
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=5.00, doc=""
)

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, CAD, GBP, CHF, CNY, JPY
# REAL_WORLD_CURRENCY_CODE = 'RMB '
REAL_WORLD_CURRENCY_CODE = '$'
REAL_WORLD_CURRENCY_CODE = '€'
USE_POINTS = False
POINTS_CUSTOM_NAME = 'Francs'
REAL_WORLD_CURRENCY_DECIMAL_PLACES = 2
POINTS_DECIMAL_PLACES = 0

ROOMS = [
    {
        'name': 'sdc',
        'display_name': 'SDC',
        'participant_label_file': '_rooms/sdc.txt',
    },
    {
        'name': '1',
        'display_name': 'Room 1',
        'participant_label_file': '_rooms/1.txt',
    },
    {
        'name': '2',
        'display_name': 'Room 2',
    },
    {
        'name': '3',
        'display_name': 'Room 3',
    },
]





# AUTH_LEVEL:
# this setting controls which parts of your site are freely accessible, and which are password protected:
# - If it's not set (the default), then the whole site is freely accessible.
# - If you are launching a study and want visitors to only be able to
#   play your app if you provided them with a start link, set it to STUDY.
# - If you would like to put your site online in public demo mode where
#   anybody can play a demo version of your game, but not access the rest
#   of the admin interface, set it to DEMO.
# for flexibility, you can set it in the environment variable OTREE_AUTH_LEVEL
AUTH_LEVEL = 'STUDY'
AUTH_LEVEL = environ.get('OTREE_AUTH_LEVEL')
ADMIN_USERNAME = environ.get('OTREE_ADMIN_USERNAME')
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')


DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""


SECRET_KEY = '^pj7p=ng+g+ay66-!=54r4gxbct=b%hwbnzx61h7196*kbzs5o'


# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = [
    'otree',
    'otreeutils',
]
