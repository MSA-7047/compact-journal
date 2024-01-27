"""
URL configuration for task_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from tasks import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('log_in/', views.LogInView.as_view(), name='log_in'),
    path('log_out/', views.log_out, name='log_out'),
    path('password/', views.PasswordView.as_view(), name='password'),
    path('profile/', views.ProfileUpdateView.as_view(), name='profile'),
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),
    path('friend_requests/', views.view_friend_requests, name='view_friend_requests'),
    path('friends/', views.view_friends, name='friends'),
    path('send_friend_request/<int:user_id>', views.send_friend_request, name='send_request'),
    path('freind_request/accept/<int:friend_request_id>', views.accept_invitation, name='accept_friend_request'),
    path('freind_request/reject/<int:friend_request_id>', views.reject_invitation, name='reject_friend_request'),
    path('delete_sent_request/<int:request_id>/', views.delete_sent_request, name='delete_sent_request'),
    path('remove_friend/<int:user_id>', views.remove_friend, name='remove_friend'),
]
