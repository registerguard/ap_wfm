from django.conf.urls.defaults import *
from ap_wfm.views import APStoryListView, APStoryDetailView, \
APCategoryCountListView, PortlandStocks, OregonSports, \
OregonNewsNoSportsNoBizNoLott, Lotteries, json_view
from ap_wfm.feeds import LatestEntries

urlpatterns = patterns('',
    url(r'^$', APStoryListView.as_view(), name='ap_story_index'),
    url(r'^lotteries/(?P<count>\d+)/$', Lotteries.as_view(template_name='ap_wfm/apstory_list.html'), name='lotteries'),
    url(r'^ore/(?P<count>\d+)/$', OregonNewsNoSportsNoBizNoLott.as_view(), name='oregon_news_no_sports_no_biz'),
    url(r'^portland-stocks/(?P<count>\d+)/$', PortlandStocks.as_view(), name='portland_stocks'),
    url(r'^oregon-sports/(?P<count>\d+)/$', OregonSports.as_view(template_name = 'ap_wfm/apstory_list.html'), name='oregon_sports'),
    url(r'^(?P<category>[a-z]+)/(?P<count>\d+)/json/$', json_view, name='json_ap_story_list'),
    url(r'^(?P<category>[a-z]+)/(?P<count>\d+)/$', APCategoryCountListView.as_view(template_name = 'ap_wfm/apstory_list.html'), name='ap_story_list'),
    url(r'^(?P<category>[a-z]+)/(?P<slug>[\-\w]+)/$', APStoryDetailView.as_view(), name='ap_story_detail'),
    url(r'^(?P<category>[a-z]+)/(?P<slug>[\-\w]+)/multimedia/$', APStoryDetailView.as_view(template_name = 'ap_wfm/apstory_detail_multimedia.html'), name='ap_story_multimedia'),
    url(r'^lotteries/index/(?P<count>\d+)/$', Lotteries.as_view(template_name='ap_wfm/apstory_category_index.html'), name='lotteries_index'),
    url(r'^nwn/index/(?P<count>\d+)/$', APCategoryCountListView.as_view(template_name = 'ap_wfm/apstory_nwn_index.html'), name='northwest_now'),
    url(r'^oregon-sports/index/(?P<count>\d+)/$', OregonSports.as_view(template_name = 'ap_wfm/apstory_category_index.html'), name='oregon_sports_index'),
    url(r'^(?P<category>[a-z]+)/index/(?P<count>\d+)/$', APCategoryCountListView.as_view(template_name = 'ap_wfm/apstory_category_index.html'), name='ap_topic_index'),
    (r'^/feeds/rss/$', LatestEntries()),
)
