from django.conf.urls.defaults import *
from django.views.generic import ListView
from ap_wfm.models import APStory

urlpatterns = patterns('',
    (r'^$', ListView.as_view(
        model = APStory,
    )),
)