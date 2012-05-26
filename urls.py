from django.conf.urls.defaults import *
from ap_wfm.views import APStoryListView, APStoryDetailView

urlpatterns = patterns('',
    (r'^$', APStoryListView.as_view()),
    (r'^(?P<pk>\d+)$', APStoryDetailView.as_view()),
)