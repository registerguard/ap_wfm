from django.contrib.syndication.feeds import Feed
from ap_wfm.models import APStory

class LatestEntries(Feed):
    title = 'Latest from The AP'
    link = '/apf/'
    description = 'The very latest from The Associated Press'
    
    def items(self):
        return APStory.objects.all()[:10]
