"""WEB PAGE for USER to Register. Django class UserCreationForm is used 
to get default Registration FORM. It is modified to user defined class UserRegisterForm
in users/forms.py to add E-mail field in the default form.

WEB PAGE for user PROFILE.

Imported modules:
UserCreationForm: Gives us forms like built-in Registration form
Messages: Gives us flash messages (pop-up windows for success).
Redirect: Redirects us to certain url
login_required: Makes sure PROFILE page is inaccessible until a user has logged in.
                It redirects to LOGIN page if a request is made to PROFILE page by an
                unlogged user. Once logged in through the redirected LOGIN page. The user
                will be sent to PROFILE page instead of HOME page.
                This is a decorator. By default Django looks for the profile in the
                path /accounts/login/?next=/profile/ (which doesn't exist in this project) 
                if this decorator is addded.
                So we add LOGIN_URL = 'login' (login refers to url_pattern in Project/urls.py)
                in the last part of Project/settings.py file.
UserRegisterForm: class UserRegisterForm from users/forms.py for E-mail
                  field to be created in the form. This to be used instead
                  of UserCreationForm module as this user defined module
                  inherits from UserCreationForm with E-mail field added to
                  built-in Username, pass & confirm pass field.
UserUpdateForm: Updates Username & E-mail
ProfileUpdateForm: Updates Profile picture of users

Template for flash message in blog/template/blog/base.html in line 60
"""

from django.shortcuts import render, redirect
#from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

"""POST is a method to get info.
In this case user info for registrtion.
Refer templates/users/register.html for POST method in line 7
"""
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST) # cr8s form to get info & store it
        # is_valid checks if the whether already exists in DB and whether the pass is correct and matching.
        # If validation fails then it exits the loop & just returns render otherise it redirects to Login page
        # The 3rd arg in return render ('form': form) refers to form created abv.
        # That's why the refreshed page has values previously feeded for pass & username &
        # Django adds some error megs for invalid usrname and pass  
        if form.is_valid():
            # valid form is stored in built-in cleaned_data dict.
            form.save() # Vals filled in form saved and thus a user acc is created. It also hashes the pass in the background.
            # Get 'username' from the dict
            username = form.cleaned_data.get('username') # this line runs even without form.save() i.e Usname is fetched
            # but user acc isn't actually created
            messages.success(request, f'Account created for {username}! Now you can Login')
            return redirect('login') # login is name of url pattern for Login page
            # login is present in project/urls.py
    else:
        # this never runs. Just here due to convention
        form = UserRegisterForm() # creates blank form. Vals feeded
        # in this form is not stored and the page simply refreshes.  
    # 3rd arg below is context. Refer blog/views.py
    return render(request, 'users/register.html', {'form': form, 'title': 'Sign Up'})

@login_required
def profile(request):
    if request.method == 'POST':
        # We are trying to store new data so we require POST
        # instance of user is passed to show the currently stored data i.e data b4
        # being updated. user details (usrname & E-mail) for u_form & current
        # Profile pic of user for p_form.
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES,
                                   instance=request.user.profile)
        # request.FILES is required as a Image file is being uploaded from
        # file  system. This arg sends the request to the file  system
        # for the image.
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Account Updated!')
            return redirect('profile')
    else:
        # this never runs. Just here due to convention
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'title': 'Profile',
        'u_form': u_form,
        'p_form': p_form
    }
    # users/templates/users/profile.html is the full path but Django
    # demands it to be only users/profile.html
    return render(request, 'users/profile.html', context)
    
