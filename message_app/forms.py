from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content', 'featured_image', 'scheduled_at', 'message_type']

