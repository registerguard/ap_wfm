import datetime
from django.contrib.sites.models import Site
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView
from ap_wfm.models import APStory, Category, json_response

PRETTY_NAME = {
    'biz': 'business',
    'dc': 'federal',
    'enter': 'entertainment',
    'health': 'health',
    'intl': 'international',
    'odd': 'oddities',
    'ore': 'oregon',
    'politics': 'politics',
    'sci': 'science',
    'sports': 'sports',
    'tech': 'technology',
    'top': 'top news',
    'us': 'national',
    'wash': 'washington state',
    'wx': 'weather',
}

@json_response
def json_view(request, *args, **kwargs):
    # It would be nice if we could plug in URL args ...
    callback_name = request.GET.get('callback', '')
#     index_category = Category.objects.get(name=kwargs['category'])
    index_category = get_object_or_404(Category, name=kwargs['category'])
    count = kwargs['count']
    return [mm.to_json_dict() for mm in APStory.objects.filter(category=index_category, published__lte=datetime.datetime.now()).exclude(consumer_ready=False).exclude(subject_code='j')[:count]]

class APStoryListView(ListView):

    template_name = 'ap_wfm/apstory_index_all.html'

    def get_queryset(self):
        return APStory.objects.filter(published__lte=datetime.datetime.now()).exclude(consumer_ready=False)[:20]

    def get_context_data(self, **kwargs):
        context = super(APStoryListView, self).get_context_data(**kwargs)
        context.update({
            'current_site': Site.objects.get_current(),
            'page': {'title': 'The very latest from across The Associated Press'},
        })
        return context

class APStoryDetailView(DetailView):
    '''
    http://robots.thoughtbot.com/post/43154885203/class-based-generic-views-in-django
    '''
    template_name = 'ap_wfm/apstory_detail.html'

    model = APStory
    slug_field = 'slug'

    def get_queryset(self):
        detail_category = Category.objects.get(name=self.kwargs['category'])

        qs = super(APStoryDetailView, self).get_queryset()
        return qs.filter(slug=self.kwargs['slug'], category=detail_category, consumer_ready=True)

    def get_context_data(self, **kwargs):
        context = super(APStoryDetailView, self).get_context_data(**kwargs)
        context.update({
            'page': {'title': 'The Wire', 'cat': self.kwargs['category'], 'description_short': PRETTY_NAME.get(self.kwargs['category'], self.kwargs['category'])}
        })
        return context

class APCategoryCountListView(ListView):
    def get_queryset(self):
        if self.template_name == 'ap_wfm/apstory_nwn_index.html':
            '''
            If we come in this way, there's no self.kwargs['category'], so we
            have to contrive one for further down. Ick.
            '''
            self.kwargs['category'] = 'ore'
            the_category = Category.objects.get(name='ore')
            self.wash_category = Category.objects.get(name='wash')
        else:
            the_category = Category.objects.get(name=self.kwargs['category'])
            self.wash_category = None

        # The standalone Oregon page ...
        if self.kwargs['category'] == 'ore' and not self.wash_category:
            return APStory.objects.filter(category=the_category, published__lte=datetime.datetime.now()).exclude(consumer_ready=False).exclude(subject_code='j').exclude(subject_code='s').exclude(subject_code='f')[:self.kwargs['count']]
        # The Northwest Now page ...
        elif the_category and self.wash_category:
            return APStory.objects.filter(category=the_category, published__lte=datetime.datetime.now()).exclude(consumer_ready=False).exclude(subject_code='j').exclude(subject_code='s').exclude(subject_code='f')[:self.kwargs['count']]
        # All other AP wire pages ...
        else:
            return APStory.objects.filter(category=the_category, published__lte=datetime.datetime.now()).exclude(consumer_ready=False).exclude(subject_code='j')[:self.kwargs['count']]

    def get_context_data(self, **kwargs):
        context = super(APCategoryCountListView, self).get_context_data(**kwargs)
        context.update({
            'current_site': Site.objects.get_current(),
            'category': self.kwargs['category'],
        })

        if self.template_name == 'ap_wfm/apstory_nwn_index.html':
            context.update({
                'wash_stories': APStory.objects.filter(category=self.wash_category, published__lte=datetime.datetime.now()).exclude(consumer_ready=False).exclude(subject_code='j')[:self.kwargs['count']],
                'page': {'title': 'The Wire', 'description_short': 'northwest now'}
            })
        else:
            context.update({
                'page': {'title': 'The Wire', 'description_short': PRETTY_NAME.get(self.kwargs['category'], self.kwargs['category'])}
            })

        return context

class PortlandStocks(ListView):

    def get_queryset(self):
        return APStory.objects.filter(category=15, subject_code='f').exclude(consumer_ready=False)[:self.kwargs['count']]

    def get_context_data(self, **kwargs):
        context = super(PortlandStocks, self).get_context_data(**kwargs)
        context.update({
            'current_site': Site.objects.get_current(),
            'page': {'title': 'the wire', 'description_short': 'regional business'}
        })
        return context

class OregonSports(ListView):

    template_name = 'ap_wfm/apstory_list.html'

    def get_queryset(self):
        return APStory.objects.filter(category=15, subject_code='s', published__lte=datetime.datetime.now()).exclude(consumer_ready=False)[:self.kwargs['count']]

    def get_context_data(self, **kwargs):
        context = super(OregonSports, self).get_context_data(**kwargs)
        context.update({
            'current_site': Site.objects.get_current(),
        })

        if self.template_name == 'ap_wfm/apstory_category_index.html':
            context.update({
                'pretty_name': 'oregon sports',
                'page': {'title': 'the wire', 'description_short': 'oregon sports'}
            })
        return context

class OregonNewsNoSportsNoBizNoLott(ListView):

    def get_queryset(self):
        return APStory.objects.filter(category=15, published__lte=datetime.datetime.now()).exclude(consumer_ready=False).exclude(subject_code='j').exclude(subject_code='s').exclude(subject_code='f')[:self.kwargs['count']]

    def get_context_data(self, **kwargs):
        context = super(OregonNewsNoSportsNoBizNoLott, self).get_context_data(**kwargs)
        context.update({
            'current_site': Site.objects.get_current(),
        })
        return context

class Lotteries(ListView):

    def get_queryset(self):
        return APStory.objects.filter(category=15, subject_code='j', published__lte=datetime.datetime.now()).exclude(consumer_ready=False)[:self.kwargs['count']]

    def get_context_data(self, **kwargs):
        context = super(Lotteries, self).get_context_data(**kwargs)
        context.update({
            'current_site': Site.objects.get_current(),
        })

        if self.template_name == 'ap_wfm/apstory_category_index.html':
            context.update({
                'pretty_name': 'lotteries',
                'page': {'title': 'the wire', 'description_short': 'Oregon, California lottery results'}
            })
        return context

def category_index(request):
    item_count = 3
    categories_dict = {
        'categories0': {
            'ore': APStory.objects.filter(category__name='ore', published__lte=datetime.datetime.now()).exclude(consumer_ready=False).exclude(subject_code='j').exclude(subject_code='s').exclude(subject_code='f')[:item_count],
        },
        'categories1': {
            'wash': APStory.objects.filter(category__name='wash', published__lte=datetime.datetime.now()).exclude(consumer_ready=False).exclude(subject_code='j').exclude(subject_code='s').exclude(subject_code='f')[:item_count],
        },
        'categories2': {
            'top': APStory.objects.filter(category__name='top', published__lte=datetime.datetime.now()).exclude(consumer_ready=False).exclude(subject_code='j').exclude(subject_code='s').exclude(subject_code='f')[:item_count],
        },
        'categories3': {
            'us': APStory.objects.filter(category__name='us', published__lte=datetime.datetime.now()).exclude(consumer_ready=False).exclude(subject_code='j').exclude(subject_code='s').exclude(subject_code='f')[:item_count],
        },
        'categories4': {
            'intl': APStory.objects.filter(category__name='intl', published__lte=datetime.datetime.now()).exclude(consumer_ready=False).exclude(subject_code='j').exclude(subject_code='s').exclude(subject_code='f')[:item_count],
        },
        'categories5': {
            'dc': APStory.objects.filter(category__name='dc', published__lte=datetime.datetime.now()).exclude(consumer_ready=False).exclude(subject_code='j').exclude(subject_code='s').exclude(subject_code='f')[:item_count],
        },
        'categories6': {
            'politics': APStory.objects.filter(category__name='politics', published__lte=datetime.datetime.now()).exclude(consumer_ready=False).exclude(subject_code='j').exclude(subject_code='s').exclude(subject_code='f')[:item_count],
        },
        'categories7': {
            'sports': APStory.objects.filter(category__name='sports', published__lte=datetime.datetime.now()).exclude(consumer_ready=False).exclude(subject_code='j').exclude(subject_code='s').exclude(subject_code='f')[:item_count],
        },
        'categories8': {
            'tech': APStory.objects.filter(category__name='tech', published__lte=datetime.datetime.now()).exclude(consumer_ready=False).exclude(subject_code='j').exclude(subject_code='s').exclude(subject_code='f')[:item_count],
        },
        'categories9': {
            'health': APStory.objects.filter(category__name='health', published__lte=datetime.datetime.now()).exclude(consumer_ready=False).exclude(subject_code='j').exclude(subject_code='s').exclude(subject_code='f')[:item_count],
        },
        'categories10': {
            'sci': APStory.objects.filter(category__name='sci', published__lte=datetime.datetime.now()).exclude(consumer_ready=False).exclude(subject_code='j').exclude(subject_code='s').exclude(subject_code='f')[:item_count],
        },
        'categories11': {
            'odd': APStory.objects.filter(category__name='odd', published__lte=datetime.datetime.now()).exclude(consumer_ready=False).exclude(subject_code='j').exclude(subject_code='s').exclude(subject_code='f')[:item_count],
        },
    }
    categories_dict['pretty_name'] = PRETTY_NAME

    return render(request, 'ap_wfm/apstory_categories_index.html', categories_dict)
