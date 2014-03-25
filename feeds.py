from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from ap_wfm.models import APStory

class RssLatestEntries(Feed):
    title = 'Latest from The AP'
    link = '/apf/feeds/rss/'
    description = 'The very latest from The Associated Press'
    
    def items(self):
        return APStory.objects.all().exclude(consumer_ready=False)[:10]
    
    def item_title(self, item):
        return item.headline
    
#     def item_description(self, item):
#         return item.body
    
    def item_pubdate(self, item):
        return item.updated

class AtomLatestEntries(RssLatestEntries):
    feed_type = Atom1Feed
    subtitle = RssLatestEntries.description