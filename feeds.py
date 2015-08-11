from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from ap_wfm.models import APStory

class RssLatestEntries(Feed):
    '''
    Latest AP, excluding 'region' Category
    '''
    title = 'Latest from The AP'
    link = '/apf/feeds/rss/'
    description = 'The very latest from The Associated Press'

    def items(self):
        return APStory.objects.filter(consumer_ready=True).exclude(category__name='region')[:10]

    def item_title(self, item):
        return item.headline

#     def item_description(self, item):
#         return item.body

    def item_pubdate(self, item):
        return item.updated

class AtomLatestEntries(RssLatestEntries):
    feed_type = Atom1Feed
    subtitle = RssLatestEntries.description

class RssLatestRegion(Feed):
    '''
    Latest AP 'region' Category
    '''
    title = 'Latest regional from The AP'
    link = '/apf/feeds/rss/region/'
    description = 'The very latest region items via The Associated Press'

    def items(self):
        # 14 is Id of 'region' Category.
        return APStory.objects.filter(consumer_ready=True, category__name='region').exclude(contributor='The Register-Guard')[:10]

    def item_title(self, item):
        return '%s: %s' % (item.contributor, item.headline)

    def item_pubdate(self, item):
        return item.updated

