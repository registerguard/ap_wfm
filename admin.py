from django.contrib import admin
from ap_wfm.models import APStory

class APStoryAdmin(admin.ModelAdmin):
    list_display = ('headline', 'published', 'updated', 'contributor', 'consumer_ready', 'priority_numeric', 'priority_legacy', 'location',)
    
admin.site.register(APStory, APStoryAdmin)
