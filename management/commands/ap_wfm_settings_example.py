# -*- coding: utf-8 -*-

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
    'All-TopHeadlines-JH': {
        'skip_title': ('Top-General-Headlines',), 
        'replace': ('',),
    },
    'Arts-Entertainment-JH': {
        'skip_title': ('-NYT', '-MCT-', 'Top-Entertainment-', 'Top-General-', 'BC-', 'World Briefly',), 
        'replace': ('',),
    },
    'Business-TopHeadlines-JH': {
        'skip_title': ('Top-Business-Headlines',), 
        'replace': ('',),
    },
    'Entertainment-TopHeadlines-JH': {
        'skip_title': ('Top-Entertainment-Headlines',), 
        'replace': ('',),
    },
    'HealthChannel-JH': {
        'skip_title': ('TN--Tennessee Today',),
        'replace': ('',),
    },
    'International-TopHeadlines-JH': {
        'skip_title': ('Top-International-Headlines',), 
        'replace': ('',),
    },
    'Oddities-JH': {
        'skip_title': ('',),
        'replace': ('',),
    },
    'Oregon-JH': {
        'skip_title': ('USDA-', 'The Register-Guard',), 
        'replace': ('',),
    },
    'Politics-JH': {
        'skip_title': ('-Cnty', '-Sum', '-elected', '-nominated', '-Uncontested', '-Contested'),
        'replace': ('',),
    },
    'Region-JH': {
        'skip_title': ('',),
        'replace': ('',),
    },
    'ScienceChannels-JH': {
        'skip_title': ('Wind Chill Advisory', ),
        'replace': ('',),
    },
    'Sports-TopHeadlines-JH': {
        'skip_title': ('Top-Sports-Headlines',), 
        'replace': ('',),
    },
    'Technology-JH': {
        'skip_title': ('-NYT', '-MCT-', 'COX', 'HNS', 'Stock News', '-CPT', u':MCT — ', u':WA — ',), 
        'replace': ('',),
    },
    'US-TopHeadlines-JH': {
        'skip_title': ('Top-U.S.-News-Headlines',), 
        'replace': ('',),
    },
    'Washington-DC-JH': {
        'skip_title': ('-NYT', '-HNS', u':TBW — ', u':WA — ',), 
        'replace': ('',),
    },
    'Washington-State-JH': {
        'skip_title': ('HKO-WHL', 'LOT--', 'USDA-Portland', 'Box, BKC',), 
        'replace': ('',),
    },
    'Weather-JH': {
        'skip_title': ('',),
        'replace': ('',),
    },
}
"""

# Items to skip within the above custom searches:
WIRE_PROCESSING = {}
