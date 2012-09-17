from django.db import models

class APStory(models.Model):
    updated = models.DateTimeField(blank=True)
    published = models.DateTimeField(blank=True)
    consumer_ready = models.BooleanField(default=True)
    media_type = models.CharField(max_length=32)
    priority_numeric = models.IntegerField(blank=True)
    priority_legacy = models.CharField(max_length=5, blank=True)
    location = models.CharField(max_length=200, blank=True)
    contributor = models.CharField(max_length=100, blank=True)
    contributor_uri = models.CharField(max_length=125, blank=True)
    slugline = models.CharField(max_length=300)
    title = models.CharField(max_length=175)
    headline = models.CharField(max_length=200, blank=True)
    body = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = 'stories'
        ordering = ['-published']
    
    def __unicode__(self):
        return '%s ID:%s' % (self.headline, self.id)
    
    def image_count(self):
        return '%s' % self.image_set.count()

class Image(models.Model):
    apstory = models.ForeignKey(APStory)
    original_filename = models.CharField(max_length=125, default='AP photo')
    image = models.ImageField(upload_to='uploads/ap/images')
    alt_text = models.CharField(max_length=235, default='alt text')
    caption = models.TextField(blank=True)
    source = models.CharField(max_length=220, blank=True)
    photo_type = models.CharField(max_length=50, help_text=u'Horizontal or vertical') # only an attribute on full-size image
    
    def __unicode__(self):
        return self.original_filename