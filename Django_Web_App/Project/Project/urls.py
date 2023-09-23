"""Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views # this gives us built-in Login/Logout views.
# This (abv module) won't have default template
from django.urls import path, include
from django.conf import settings #check below url_patterns
from django.conf.urls.static import static
from users import views as user_views #Importing views.py from USERS dir

urlpatterns = [
    path("admin/", admin.site.urls),  # localhost:8000 Admin Login Page
    path("", include("blog.urls")),  # refers to blog/urls.py for PATH.
    # PATH is empty ("") bcoz we wanted to set (localhost:8000) as default page which shows the BLOG HOME Page
    path("register/", user_views.register, name = 'register'), # 'name' is name given to the path
    path("profile/", user_views.profile, name = 'profile'),
    path("login/", auth_views.LoginView.as_view(template_name = 'users/login.html'), name = 'login'),
    # By default Django looks for Login & logout template in registration/login.html
    # But since we don't have that users/login.html is passed as arg on .as_view(). Similarly for logout
    path("logout/", auth_views.LogoutView.as_view(template_name = 'users/logout.html'), name = 'logout'),
    path("password-reset/", auth_views.PasswordResetView.as_view(template_name = 'users/password_reset.html'),
            name = 'password_reset'),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(template_name = 'users/password_reset_done.html'),
            name = 'password_reset_done'),
    # This path is necessary. <uidb64>/<token> are mandatory security layers.
    path("password-reset/confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name = 'users/password_reset_confirm.html'),
            name = 'password_reset_confirm'),
    path("password-reset/complete/", auth_views.PasswordResetCompleteView.as_view(template_name = 'users/password_reset_complete.html'),
            name = 'password_reset_complete'),
]

"""
From Django documentation https://www.youtube.com/redirect?event=video_description&redir_token=QUFFLUhqa3RJazhpazlzbm45X2dScG5WMkZtelRWVnh2UXxBQ3Jtc0tsdzBhUnJJcS1zRkljZF80SC0tN3A2dXNSLWpYUzBZa1lFVUMyaExGYnZUbUJvR3E3RWtVTHhVMDlZRnVtbUF0UGMxVGlobFFvd20wYldNZ2pCWVNxUkVhem9oTVFWb1ltc1hvdk1CanE4ZDE0YkdoYw&q=https%3A%2F%2Fdocs.djangoproject.com%2Fen%2F2.1%2Fhowto%2Fstatic-files%2F%23serving-files-uploaded-by-a-user-during-development
This is only for development. Not production.

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... the rest of your URLconf goes here ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

So we place the import abv the code.
"""

# we got setting from the imports as mentioned in the documentation
# If we are in DEBUG mode (in production).
# Now the Profile page will work.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
