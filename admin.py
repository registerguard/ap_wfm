from django.contrib import admin
from ap_wfm.models import APStory, Image

class ImageInline(admin.TabularInline):
    model = Image
    extra = 1

class APStoryAdmin(admin.ModelAdmin):
    save_on_top = True
    search_fields = ['title', 'headline', 'slugline',]
    list_display = ('id', 'created', 'keywords', 'title', 'headline', 'slugline', 'image_count', 'media_type', 'published', 'updated', 'contributor', 'consumer_ready', 'priority_numeric', 'priority_legacy', 'location',)
    inlines = [
        ImageInline,
    ]
admin.site.register(APStory, APStoryAdmin)
