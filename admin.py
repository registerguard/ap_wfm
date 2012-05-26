from django.contrib import admin
from ap_wfm.models import APStory, Image

class ImageInline(admin.TabularInline):
    model = Image
    extra = 1

class APStoryAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('title', 'headline', 'published', 'updated', 'contributor', 'consumer_ready', 'priority_numeric', 'priority_legacy', 'location',)
    inlines = [
        ImageInline,
    ]
admin.site.register(APStory, APStoryAdmin)
