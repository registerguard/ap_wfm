from django.db import models

class APStory(models.Model):
    updated = models.DateTimeField(blank=True)
    published = models.DateTimeField(blank=True)
    consumer_ready = models.BooleanField(default=True)
    priority = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=200, blank=True)
    contributor = models.CharField(max_length=100, blank=True)
    contributor_uri = models.CharField(max_length=125, blank=True)
    headline = models.CharField(max_length=200, blank=True)
    body = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = 'stories'
    
    def __unicode__(self):
        return self.headline

class Image(models.Model):
    apstory = models.ForeignKey(APStory)
    filepath = models.CharField(max_length=500, blank=True)
    
    def __unicode__(self):
        return self.filename