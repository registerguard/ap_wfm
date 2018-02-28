from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.db import models
from django.http import HttpResponse
from django.utils import simplejson
from ap_wfm.templatetags.humanize_list import humanize_list
from sorl.thumbnail import ImageField, get_thumbnail

def json_response(func):
    """
    https://coderwall.com/p/k8vb_a
    A decorator that takes a view response and turns it
    into json. If a callback is added through GET or POST
    the response is JSONP.
    """
    def decorator(request, *args, **kwargs):
        objects = func(request, *args, **kwargs)
        if isinstance(objects, HttpResponse):
            return objects
        try:
            data = simplejson.dumps(objects)
            if 'callback' in request.REQUEST:
                # a jsonp response!
                data = '%s(%s);' % (request.REQUEST['callback'], data)
                return HttpResponse(data, "text/javascript")
        except:
            data = simplejson.dumps(str(objects))
        return HttpResponse(data, "application/json")
    return decorator

class Category(models.Model):
    CATEGORY_CHOICES = (
        (22, 'arts'),
        (19, 'business'),
        (13, 'federal'),
        (27, 'entertainment'),
        (21, 'health'),
        (20, 'international'),
        (25, 'oddities'),
        (15, 'oregon'),
        (23, 'politics'),
        (14, 'region'),
        (17, 'science'),
        (24, 'sports'),
        (18, 'technology'),
        (26, 'top news'),
        (1, 'national'),
        (4, 'washington state'),
        (12, 'weather'),
    )
    name = models.CharField(max_length=100, unique=True, choices=CATEGORY_CHOICES)
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def __unicode__(self):
        return self.name

class APStory(models.Model):
    category = models.ManyToManyField(Category)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(blank=True)
    published = models.DateTimeField(blank=True)
    management_id = models.CharField(max_length=150)
    consumer_ready = models.BooleanField(default=True)
    media_type = models.CharField(max_length=32)
    priority_numeric = models.IntegerField(blank=True)
    priority_legacy = models.CharField(max_length=5, blank=True)
    subject_code = models.CharField(max_length=128, blank=True)
    location = models.CharField(max_length=200, blank=True)
    contributor = models.CharField(max_length=100, blank=True)
    contributor_uri = models.CharField(max_length=125, blank=True)
    byline = models.CharField(max_length=220, blank=True)
    byline_title = models.CharField(max_length=150, blank=True)
    slugline = models.CharField(max_length=300)
    title = models.CharField(max_length=175)
    keywords = models.CharField(max_length=180)
    headline = models.CharField(max_length=260, blank=True)
    slug = models.SlugField(max_length=300)
    body = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = 'stories'
        ordering = ['-updated']
    
    def __unicode__(self):
        return '%s ID:%s' % (self.headline, self.id)

    def get_absolute_url(self):
        # return '//{}/apf/{}/{}/'.format('projects.registerguard.com', self.category.all()[0].get_name_display(), self.slug)
        return '//projects.registerguard.com/apf/%s/%s/' % (self.category.all()[0].get_name_display(), self.slug)

    def image_count(self):
        return self.image_set.count()

    def practical_update(self):
        '''
        Answers the question of whether the interval between published and
        updated is greater than 120 seconds.
        '''
        time_diff = self.updated - self.published
        if time_diff.seconds < 120:
            return False
        else:
            return True

    def categories(self):
        return humanize_list([ item.name for item in self.category.all() ])
    
    def to_json_dict(self):
        return {
            'headline': self.headline,
#             'link': self.slug,
            'url': '%s%s' % (Site.objects.get_current().name, reverse('ap_story_detail', args=[self.category.filter(apstory__slug=self.slug)[0].name, self.slug]))
        }

class Image(models.Model):
    apstory = models.ForeignKey(APStory, null=True, on_delete=models.SET_NULL)
    original_filename = models.CharField(max_length=125, default='AP photo')
    image = ImageField(upload_to='ap/images', max_length=225)
    alt_text = models.CharField(max_length=235, default='alt text')
    caption = models.TextField(blank=True)
    source = models.CharField(max_length=220, blank=True)
    photo_type = models.CharField(max_length=50, help_text=u'Horizontal or vertical', blank=True) # only an attribute on full-size image
    
    def __unicode__(self):
        return self.original_filename

    def to_json_image_dict(self):
        json_image = get_thumbnail(self.image, '990x990')
        return {
            'description': self.caption,
            'byline': self.source,
            'image': json_image.url
        }
