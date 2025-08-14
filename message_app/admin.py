from django.contrib import admin
from .models import Message
from django_summernote.admin import SummernoteModelAdmin


# Register your models here.
@admin.register(Message)
class MessageAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    list_display = ('user', 'created_on', 'scheduled_at')
