from django.contrib import admin
from .models import Post


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish_time', 'status')
    list_filter = ('status', 'create_time', 'publish_time', 'author')
    search_fields = ('title', 'body',)
    date_hierarchy = 'publish_time'
    ordering = ('status', 'publish_time')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)


