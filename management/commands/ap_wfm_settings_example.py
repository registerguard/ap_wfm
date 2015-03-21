# -*- coding: utf-8 -*-

# How many days of AP stories do you want to keep active?
# If None, defaults to 60 (set with integer, not string).
DAYS_BACK = None

# Error email “from”/sender:
FROM_EMAIL = 'baz@foo.com'

# Who gets error emails?
RECIPIENT_LIST = [
    'foo@baz.com',
    # Add more here …
]

"""
WIRE_CATEGORY_DICT = {
    'All-TopHeadlines-JH':               'top', 
    'Arts-Entertainment-JH':             'arts', 
    'Business-TopHeadlines-JH':          'biz', 
    'Entertainment-TopHeadlines-JH':     'enter', 
    'HealthChannel-JH':                  'health', 
    'International-TopHeadlines-JH':     'intl', 
    'Oddities-JH':                       'odd', 
    'Oregon-JH':                         'ore', 
    'Politics-JH':                       'politics', 
    'Region-JH':                         'region', 
    'ScienceChannels-JH':                'sci', 
    'Sports-TopHeadlines-JH':            'sports', 
    'Technology-JH':                     'tech', 
    'US-TopHeadlines-JH':                'us', 
    'Washington-DC-JH':                  'dc', 
    'Washington-State-JH':               'wash', 
    'Weather-JH':                        'wx', 
}
"""

# Named AP WFM custom searches mapped to shorter names for convenience:
WIRE_CATEGORY_DICT = {}

"""
WIRE_PROCESSING = {
    'All-TopHeadlines': {
        'skip_title': ('Top-General-Headlines',), 
        'replace': ('',),
        'delay': 0,
    },
    'Arts-Entertainment': {
        'skip_title': ('-NYT', '-MCT-', 'Top-Entertainment-', 'Top-General-', 'BC-', 'World Briefly',), 
        'replace': ('',),
        'delay': 0.5,
    },
    'Business-TopHeadlines': {
        'skip_title': ('Top-Business-Headlines',), 
        'replace': ('',),
        'delay': 1.5,
    },
    'Entertainment-TopHeadlines': {
        'skip_title': ('Top-Entertainment-Headlines',), 
        'replace': ('',),
        'delay': 2,
    },
    'HealthChannel': {
        'skip_title': ('TN--Tennessee Today',),
        'replace': ('',),
        'delay': 2.5,
    },
    'International-TopHeadlines': {
        'skip_title': ('Top-International-Headlines',), 
        'replace': ('',),
        'delay': 3,
    },
    'Oddities': {
        'skip_title': ('',),
        'replace': ('',),
        'delay': 3.5,
    },
    'Oregon': {
        'skip_title': ('USDA-', 'The Register-Guard',), 
        'replace': ('',),
        'delay': 4,
    },
    'Politics': {
        'skip_title': ('-Cnty', '-Sum', '-elected', '-nominated', '-Uncontested', '-Contested'),
        'replace': ('',),
        'delay': 4.5,
    },
    'Region': {
        'skip_title': ('',),
        'replace': ('',),
        'delay': 5,
    },
    'ScienceChannels': {
        'skip_title': ('Wind Chill Advisory', ),
        'replace': ('',),
        'delay': 5.5,
    },
    'Sports-TopHeadlines': {
        'skip_title': ('Top-Sports-Headlines',), 
        'replace': ('',),
        'delay': 6,
    },
    'Technology': {
        'skip_title': ('-NYT', '-MCT-', 'COX', 'HNS', 'Stock News', '-CPT', u':MCT — ', u':WA — ',), 
        'replace': ('',),
        'delay': 6.5,
    },
    'US-TopHeadlines': {
        'skip_title': ('Top-U.S.-News-Headlines',), 
        'replace': ('',),
        'delay': 7,
    },
    'Washington-DC': {
        'skip_title': ('-NYT', '-HNS', u':TBW — ', u':WA — ',), 
        'replace': ('',),
        'delay': 7.5,
    },
    'Washington-State': {
        'skip_title': ('HKO-WHL', 'LOT--', 'USDA-Portland', 'Box, BKC',), 
        'replace': ('',),
        'delay': 8,
    },
    'Weather': {
        'skip_title': ('',),
        'replace': ('',),
        'delay': 8.5,
    },
}
"""

# Items to skip within the above custom searches:
WIRE_PROCESSING = {}
