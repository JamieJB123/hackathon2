from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from .models import Message
from .forms import MessageForm


class HomePage(TemplateView):
    """
    Displays home page"
    """
    template_name = 'index.html'


@login_required
def AdminPage(request):
    future_messages = Message.objects.filter(
        user=request.user,
        scheduled_at__gt=timezone.now()
    ).order_by('scheduled_at')

    if request.method == "POST":
        message_form = MessageForm(data=request.POST)
        if message_form.is_valid():
            message = message_form.save(commit=False)
            message.user = request.user
            message.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Comment submitted and awaiting approval'
            )

    message_form = MessageForm()

    return render(request, 'message_app/admin-page.html', {
        'future_messages': future_messages,
        "message_form": message_form,
    })


