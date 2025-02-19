from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in Post._meta.fields if field.name not in ['some_field_to_exclude']
    ] + ['edit_link']

    def edit_link(self, obj):
        url = reverse('admin:{}_{}_change'.format(obj._meta.app_label, obj._meta.model_name), args=[obj.id])
        return format_html('<a href="{}">Edit</a>', url)

    edit_link.short_description = 'Edit'
