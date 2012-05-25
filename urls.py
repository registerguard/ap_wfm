from django.conf.urls.defaults import *
from django.views.generic import ListView
from ap_wfm.models import APStory
from ap_wfm.views import APStoryDetailView

urlpatterns = patterns('',
    (r'^$', ListView.as_view(
        model = APStory,
    )),
    (r'^(?P<pk>\d+)$', APStoryDetailView.as_view()),
)