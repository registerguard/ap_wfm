from django.core.management.base import BaseCommand, CommandError


# S3 bucket deleting:
# http://stackoverflow.com/questions/3140779/how-to-delete-files-from-amazon-s3-bucket/3264960#3264960
# Some code to look at:
# https://github.com/pcraciunoiu/django-s3sync/blob/master/s3sync/management/commands/s3sync_media.py

'''
Required settings.py variables:
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''

Optional ap_wfm_settings.py variable:
DAYS_BACK = [integer]

Default is 60 days.

'''

try:
    from boto.s3.connection import S3Connection, Bucket, Key
except ImportError, err:
    raise

class Command(BaseCommand):
    DAYS_BACK = None
    
    def handle(self, *args, **kwargs):
        # Get XX days back of APStories
        
        # Delete images attached to above APStories stories
        # ... and make sure it logs! ... 
        
        self.DAYS_BACK = ap_wfm_settings.DAYS_BACK
        
        conn = S3Connection(AWS_ACCESS_KEY, AWS_SECERET_KEY)
        b = Bucket(conn, S3_BUCKET_NAME)
        k = Key(b)
        k.key = 'images/my-images/'+filename
        b.delete_key(k)
