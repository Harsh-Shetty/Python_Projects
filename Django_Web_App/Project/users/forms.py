"""
class UserRegisterForm creates E-mail field for Registration form in users/views.py def register

Forms (UserUpdateForm &  )provide a way for users to update thier
username, E-mail & PROFILE PICTURE

Imported modules
User: Creats user model for creating/managing user info
UserCreationForm: Gives us forms like Registration form
Profile: Imports class Profile from user/moddels.py. We use it to dvelop a 
         way to update Profile Picture. 
"""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

"""
Inherits from UserCreationForm.
For forms.EmailField(), by default required = True. That means this field
must be filled. If email = forms.EmailField(required = False), its not
mandatory.
"""

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    """
    model User interacts with class UserRegisterForm bcoz whenever the form
    validates its going to create new user.
    Account created (form.save() in users/views.py in def register) will be
    saved in this model User.
    fields will appear in the form in the exact order as given below.
    password1 is pass & password2 is pass confirmation
    """
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

"""
Form to update Username & E-mail
"""

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        # Only E-mail & username updated
        fields = ['username', 'email']

"""
Form to update Profile Picture
"""

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image'] # field to update. Remember it should be 
        # fields (plural) not field (singular) 