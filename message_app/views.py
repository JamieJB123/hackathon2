from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Message
from .forms import MessageForm


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

@login_required
def message_delete(request, pk):
    message = get_object_or_404(Message, pk=pk, user=request.user)
    if request.method == "POST":
        message.delete()
        messages.success(request, "Message deleted successfully.")
        return redirect("admin_page")
    # Optionally, render a confirmation page if not POST
    return render(request, "message_app/message_confirm_delete.html", {"message": message})
