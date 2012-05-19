from django.contrib import admin
from ap_wfm.models import APStory

class APStoryAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(APStory, APStoryAdmin)
