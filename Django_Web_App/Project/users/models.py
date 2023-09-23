"""
Model for Profile Page.

After coding here is done head for CLI for uploading images.
For procedure check Django_Web_App/cmd for profile.txt

Default image will be named default.jpg. Images r uploded to profile_pics dir,
which will be created due to this code, in Django_Web_App\Project. We don't want profile_pics dir to
clutter up the root dir.
To clean up/organise the dir we add, MEDIA_ROOT = os.path.join(BASE_DIR, 'media') & MEDIA_URL = '/media/' 
to the last part of Django_Web_App\Project\Project\settings.py file.
Check the comments there for code explanation. Also, import os in settings.py
New dir created in Project\media\profile_pics. Delete old profile_pics dir.
Paste whatever pic you want to be default profile picture in the Django_Web_App\Project\media dir.

Imported modules:
User: Creates user model for creating/managing user info
models: Gives Data model. Creates fields for various kinds of data input in
        that model. models.ImageField also requires Pillow package. Which is python
        pack for image related operations. Follow aforementioned cmd for profile.txt
"""

from django.db import models
from django.contrib.auth.models import User
from PIL  import Image

class Profile(models.Model):
    # User will have direct reltionship (OneToOneField) with profile.
    # on_delete: If User is deleted so is the profile.
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    image = models.ImageField(default = 'default.jpg', upload_to = 'profile_pics')

    """
    Gives username for the PROFILE in CLI instead of vauge Profile objects. 
    Username is fetched from cleaned_data dict in users/views.py 
    """
    def __str__(self):
        return f'{self.user.username} Profile'

    """
    Profile Pic Image resizing
    """
    def save(self, *args, **kwargs):
        # This in-built in model parent class. This runs regarless when the Profile is saved.
        super(Profile, self).save(*args, **kwargs) 
        # Open Image of th current instance
        img = Image.open(self.image.path)
        if img.height > 600 or img.width > 600:
            output_size = (500,500) #Tuple for max size
            img.thumbnail(output_size) # image resized to 500x500
            img.save(self.image.path) # overrides the selected image and
            # saves the resized image instead.
