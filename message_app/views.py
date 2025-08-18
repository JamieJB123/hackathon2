from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from .models import Message

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
    message = Message.objects.filter(
        user=request.user,
        scheduled_at__gt=timezone.now()).order_by('scheduled_at').first()
    if message:
        time_diff = message.scheduled_at - now
        if message.message_type == 0:
            show_message = 0 <= time_diff.total_seconds() <= 120
        else:
            show_message = 0 <= time_diff.total_seconds() <= 1800  # 1800 seconds = 30 minutes
        return JsonResponse({
            'message': {
                'scheduled_at': message.scheduled_at.strftime('%Y-%m-%d %H:%M'),
                'content': message.content
            },
            'show_message': show_message,
            'username1': request.user.username
        })
    else:
        return JsonResponse({'message': None, 'show_message': False, 'username1': request.user.username})


def display(request):
    now = timezone.now()
    message = Message.objects.filter(
        user=request.user,
        scheduled_at__gt=timezone.now()
    ).order_by('scheduled_at').first()
    if not message:
        return render(request, 'message_app/display.html', {'message': None, 'show_message': False})
    else:
        time_diff = message.scheduled_at - now
        if message.message_type == 0:
            show_message = 0 <= time_diff.total_seconds() <= 60 #1 minute
        else:
            show_message = 0 <= time_diff.total_seconds() <= 1800  # 1800 seconds = 30 minutes
        return render(request, 'message_app/display.html', {'message': message, 'show_message': show_message})


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
                'Message created successfully'
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

@login_required
def edit_message(request, message_id):
    message = get_object_or_404(Message, id=message_id, user=request.user)

    if request.method == "POST":
        message_form = MessageForm(data=request.POST, instance=message)
        if message_form.is_valid():
            message = message_form.save(commit=False)
            message.user = request.user
            message.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Message updated successfully'
            )
            return redirect('admin_page')
        else:
            messages.add_message(request, messages.ERROR, 'Error updating message. Please try again.')
    else:
        message_form = MessageForm(instance=message)

    return render(request, 'message_app/edit_message.html', {
        'message_form': message_form,
    })
