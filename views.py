from django.views.generic import DetailView
from ap_wfm.models import APStory

class APStoryDetailView(DetailView):
    model = APStory
    slug_field = 'pk'
