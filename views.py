import datetime
from django.views.generic import DetailView, ListView
from ap_wfm.models import APStory

class APStoryListView(ListView):
    def get_queryset(self):
        return APStory.objects.filter(published__lte=datetime.datetime.now(), consumer_ready=True)

class APStoryDetailView(DetailView):
    model = APStory
    slug_field = 'pk'
