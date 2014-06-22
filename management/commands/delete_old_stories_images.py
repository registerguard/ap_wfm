from django.core.management.base import BaseCommand

'''
Required settings.py variables:
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''

Optional ap_wfm_settings.py variable:
DAYS_BACK = [integer]

Default is 60 days.

'''

class Command(BaseCommand):
    pass
