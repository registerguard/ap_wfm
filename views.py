from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = 'ap_fm/index.html'