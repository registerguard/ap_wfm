import datetime
from django.views.generic import DetailView, ListView
from ap_wfm.models import APStory

class APStoryListView(ListView):
    
    template_name = 'ap_wfm/bulldog.html'
    
    def get_queryset(self):
        return APStory.objects.filter(published__lte=datetime.datetime.now(), consumer_ready=True)[:20]

class APStoryDetailView(DetailView):
    template_name = 'ap_wfm/bulldog_story.html'
    model = APStory
    slug_field = 'pk'
