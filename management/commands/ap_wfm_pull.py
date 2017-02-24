from ap_wfm_settings import AP_USER, AP_PASSWORD
from django.core.management.base import BaseCommand, CommandError

from bs4 import BeautifulSoup
import requests

# http://syndication.ap.org/AP.Distro.Feed/GetFeed.aspx?idList=694439&idListType=savedsearches&fullContent=nitf


class Command(BaseCommand):

    def handle(self, *args, **options):
        r = requests.get(
            'http://syndication.ap.org/AP.Distro.Feed/GetFeed.aspx?idList=694439&idListType=savedsearches&fullContent=nitf',
            auth=(AP_USER, AP_PASSWORD)
        )
        soup = BeautifulSoup(r.text, 'lxml')
        print soup.prettify()
        # print soup.find_all('apnm:managementid')
