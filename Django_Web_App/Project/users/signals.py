"""
This will create a Profile for each new user and assign deafult profile pics
for all users.
Django documentation recommends doing things this way

Imported Modules:
post_save: Will create a post_save signal when a user
           is created.
User: Creates user model for creating/managing user info
      User will act as sender of the signal here.
receiver: It receives the signal. Its a decorator which takes signal and
          sender as args. This joins all the functions together.
          post_save signal when a user is created. User sends signal.
          receiver receives signals then creates profile
Profile: Profile class is imported from the current dir i.e users/models.py 
"""

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

"""
When user is saved (sender=User) send signal (post_save)
Receiver receives signals then creates profile.
create_profile all the args that post_save passed to it i.e the
instance of the user (connected through sender=User)created.
if that user was created:
    then create a Profile object with user=instance of the User created.
"""
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        # creates profile evertime a user is created
        Profile.objects.create(user=instance)

#saves profile evetime a user is saved
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    # saves previously created instance i.e  user aling with profile
    instance.profile.save()

# Now send import this signal into users/apps.py ready func.