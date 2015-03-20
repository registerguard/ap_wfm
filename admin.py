from django.contrib import admin
from ap_wfm.models import APStory, Image
from sorl.thumbnail.admin import AdminImageMixin

class ImageInline(AdminImageMixin, admin.TabularInline):
    model = Image
    extra = 1

class APStoryAdmin(admin.ModelAdmin):
    save_on_top = True
    search_fields = ['title', 'headline', 'slugline', 'keywords', ]
    list_display = ('id', 'created', 'published', 'updated', 'consumer_ready', 'headline', 'keywords', 'title', 'slugline', 'slug', 'categories', 'image_count', 'contributor', 'subject_code', 'location',)
    list_filter = ('category', 'subject_code',)
    ordering = ('-created',)
    prepopulated_fields = {'slug': ('headline',)}
    inlines = [
        ImageInline,
    ]

admin.site.register(APStory, APStoryAdmin)
