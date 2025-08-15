from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    scheduled_at = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',  # HTML5 calendar and time picker
                'class': 'form-control'
            }
        )
    )
    
    class Meta:
        model = Message
        fields = ['content', 'featured_image', 'scheduled_at', 'message_type']

