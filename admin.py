from django.contrib import admin
from ap_wfm.models import APStory, Image
from sorl.thumbnail.admin import AdminImageMixin

class ImageInline(AdminImageMixin, admin.TabularInline):
    model = Image
#     extra = 1

class APStoryAdmin(admin.ModelAdmin):
    save_on_top = True
    search_fields = ['title', 'headline', 'slugline', 'keywords', ]
    list_display = ('id', 'created', 'published', 'updated', 'keywords', 'title', 'headline', 'slugline', 'slug', 'categories', 'image_count', 'contributor', 'consumer_ready', 'subject_code', 'location',)
    list_filter = ('category', 'subject_code',)
    prepopulated_fields = {'slug': ('headline',)}

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
