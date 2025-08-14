from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.
TYPE = ((0, "friendly_message"), (1, "task_notification"))

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    featured_image = CloudinaryField('image', default="placeholder")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    scheduled_at = models.DateTimeField(null=True, blank=True)
    message_type = models.IntegerField(choices=TYPE, default=0)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f"Message {self.id} from {self.user.username} at {self.created_on}"
