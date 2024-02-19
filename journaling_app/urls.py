"""
URL configuration for journaling_app project.

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
from journal import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('log_in/', views.LogInView.as_view(), name='log_in'),
    path('log_out/', views.log_out, name='log_out'),
    path('password/', views.PasswordView.as_view(), name='password'),
    path('profile/', views.ProfileUpdateView.as_view(), name='profile'),
    path('view_profile/', views.ProfileView.as_view(), name='view_profile'),
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),
<<<<<<< HEAD
    path('create_journal_view/', views.CreateJournalView, name='create_journal_view'),
    path('change_journal_bio/<int:journalID>/', views.ChangeJournalBio, name='change_journal_bio'),
    path('change_journal_description/<int:journalID>/', views.ChangeJournalDescription, name='change_journal_description'),
    path('change_journal_title/<int:journalID>/', views.ChangeJournalTitle, name='change_journal_title'),
=======
    path('create_journal_view/', views.create_journal, name='create_journal_view'),
    path('change_journal_bio/', views.ChangeJournalBio, name='change_journal_bio'),
    path('change_journal_description/', views.ChangeJournalDescription, name='change_journal_description'),
    path('change_journal_title/', views.ChangeJournalTitle, name='change_journal_title'),
>>>>>>> main
    path('friend_requests/', views.view_friend_requests, name='view_friend_requests'),
    path('friends/', views.view_friends, name='friends'),
    path('send_friend_request/<int:user_id>', views.send_friend_request, name='send_request'),
    path('friend_request/accept/<int:friend_request_id>', views.accept_invitation, name='accept_friend_request'),
    path('friend_request/reject/<int:friend_request_id>', views.reject_invitation, name='reject_friend_request'),
    path('delete_sent_request/<int:friend_request_id>/', views.delete_sent_request, name='delete_sent_request'),
    path('remove_friend/<int:user_id>', views.remove_friend, name='remove_friend'),
    path('calendar/<int:year>/<str:month>/', views.calendar_view, name='calendar' ),
<<<<<<< HEAD
    path('all_entries/', views.all_journal_entries_view, name='all_entries'),

]
=======
    path('groups/', views.group, name='groups'),
    path('create_group/', views.create_group, name='create_group')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
>>>>>>> main
