"""
Model for Posts. Command Line used to create posts.
Refer Cmd_codes file from Users\DELL\Desktop\Python codes\Django_Web_App
for commands.

Imported modules:
User: Creates user model for creating/managing user info
models: Gives Data model. Creates fields for various kinds of data input in
        that model.
"""
from django.db import models
from embed_video.fields import EmbedVideoField
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(null=True, blank=True)
    video = EmbedVideoField(null=True, blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # (on_delete) Posts made by user deleted when user is deleted

    """
    Gives title of the Post (<Queryset [<Post: Blog 1>]>) for in CLI for the cmds like
    Post.objects.all() instead of vauge Post objects (<Queryset [<Post:Post Object(1)>]>)
    """

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})
