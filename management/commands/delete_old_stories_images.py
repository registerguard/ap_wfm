import datetime
import logging
import os
import settings
import ap_wfm_settings
from ap_wfm.models import APStory
from django.core.management.base import BaseCommand, CommandError


# S3 bucket deleting:
# http://stackoverflow.com/questions/3140779/how-to-delete-files-from-amazon-s3-bucket/3264960#3264960
# Some code to look at:
# https://github.com/pcraciunoiu/django-s3sync/blob/master/s3sync/management/commands/s3sync_media.py

'''
Required settings.py variables:
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
AWS_STORAGE_BUCKET_NAME = ''

Optional ap_wfm_settings.py variable:
DAYS_BACK = [integer]

Default is 60 days.

'''

try:
    from boto.s3.connection import S3Connection, Bucket, Key
except ImportError, err:
    raise

class Command(BaseCommand):
    args = None
    help = 'Deletes APStories and associated images after DAYS_BACK number of days.'
    DAYS_BACK = 60
    
    def handle(self, *args, **kwargs):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)-6s: %(name)s - %(levelname)s - %(message)s')
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        # get file path bits here.
        fileLogger = logging.handlers.RotatingFileHandler(filename=('delete_old_stories_images.log'), maxBytes=512*1024, backupCount=4) # 512 * 1024 = 512K
        fileLogger.setFormatter(formatter)
        logger.addHandler(fileLogger)
        
        try:
            if ap_wfm_settings.DAYS_BACK:
                self.DAYS_BACK = ap_wfm_settings.DAYS_BACK
        except AttributeError, err:
            raise
        
        try:
            self.AWS_ACCESS_KEY_ID, self.AWS_SECRET_ACCESS_KEY, self.AWS_STORAGE_BUCKET_NAME = settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY, settings.AWS_STORAGE_BUCKET_NAME
        except AttributeError, err:
            raise
        
        expire_date = datetime.datetime.now() - datetime.timedelta(days=self.DAYS_BACK)
        logger.debug('No. of DAYS_BACK: %s' % self.DAYS_BACK)
        print self.DAYS_BACK
        print expire_date
        print APStory.objects.filter(created__lte=expire_date).count()
        
        conn = S3Connection(self.AWS_ACCESS_KEY_ID, self.AWS_SECRET_ACCESS_KEY)
        b = Bucket(conn, self.AWS_STORAGE_BUCKET_NAME)
        k = Key(b)
#         k.key = 'images/my-images/' + filename
#         b.delete_key(k)
