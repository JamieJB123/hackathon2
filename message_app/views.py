from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.utils import timezone
from .models import Message

class HomePage(TemplateView):
    """
    Displays home page"
    """
    template_name = 'index.html'



def get_message_api(request):
    now = timezone.now()
    message = Message.objects.filter(scheduled_at__lte=now).order_by('-scheduled_at').first()
    if message:
        return JsonResponse({
            'message': {
                'scheduled_at': message.scheduled_at.strftime('%Y-%m-%d %H:%M'),
                'content': message.content
            }
        })
    else:
        return JsonResponse({'message': None})


def display(request):
    now = timezone.now()
    message = None
    if request.user.is_authenticated:
        message = Message.objects.filter(
            user=request.user,
            scheduled_at__gt=timezone.now()
        ).order_by('scheduled_at').first()
    return render(request, 'message_app/display.html', {'message': message})
