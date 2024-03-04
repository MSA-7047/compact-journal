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
from journal.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    
    path('log_in/', LogInView.as_view(), name='log_in'),
    path('log_out/', log_out, name='log_out'),
    
    path('password/', PasswordView.as_view(), name='password'),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),
    path('view_profile/', ProfileView.as_view(), name='view_profile'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('sign_up/', SignUpView.as_view(), name='sign_up'),
    
    path('create_journal_view/', create_journal, name='create_journal_view'),
    path('change_journal_bio/<int:journalID>/', ChangeJournalBio, name='change_journal_bio'),
    path('change_journal_description/<int:journalID>/', ChangeJournalDescription, name='change_journal_description'),
    path('change_journal_title/<int:journalID>/', ChangeJournalTitle, name='change_journal_title'),
    
    path('friend_requests/', view_friend_requests, name='view_friend_requests'),
    path('friends/', view_friends, name='view_friends'),
    path('send_friend_request/<int:user_id>', send_friend_request, name='send_request'),
    path('friend_request/accept/<int:friend_request_id>', accept_invitation, name='accept_friend_request'),
    path('friend_request/reject/<int:friend_request_id>', reject_invitation, name='reject_friend_request'),
    path('delete_sent_request/<int:friend_request_id>/', delete_sent_request, name='delete_sent_request'),
    path('remove_friend/<int:user_id>', remove_friend, name='remove_friend'),
    
    path('calendar/<int:year>/<str:month>/', calendar_view, name='calendar' ),
    path('all_entries/', all_journal_entries_view, name='all_entries'),
    path('my_journals/', my_journals_view, name='my_journals'),
    
    path('groups/', group, name='groups'),
    path('create_group/',create_group, name='create_group'),

    path('notifications/<int:notification_id>/', views.mark_notification_as_read, name='mark_notification_as_read'),
    path('notifications/', views.mark_all_notification_as_read, name='mark_all_notification_as_read')
    #path('notifications/', views.notifications_panel, name='notifications_panel'),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)