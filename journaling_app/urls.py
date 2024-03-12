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
from django.urls import path, include
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
    path('view_friends_profile/<int:friendID>', view_friends_profile, name='view_friends_profile'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('sign_up/', SignUpView.as_view(), name='sign_up'),

    path('create-journal/', create_journal, name='create_journal'),
    path('select-template/', select_template, name='select_template'),
    path('create-template/', create_template, name='create_template'),
    path('createJournalWithTemplate/<int:templateID>/', views.create_journal_From_Template, name='create_journal_with_template'),
    path('edit_journal/<int:journalID>/', EditJournal, name='edit_journal'),
    path('journal/<int:journalID>/', journal_detail_view, name='journal_detail'),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('delete_journal/<int:journalID>/', DeleteJournal, name='delete_journal'),
    path('delete_template/<int:templateID>/', DeleteTemplate, name='delete_template'),
    path('edit_template/<int:templateID>/', EditTemplate, name='edit_template'),

    
    path('friend_requests/', view_friend_requests, name='view_friend_requests'),
    path('friends/', view_friends, name='view_friends'),
    path('send_friend_request/<int:user_id>', send_friend_request, name='send_request'),
    path('friend_request/accept/<int:friend_request_id>', accept_invitation, name='accept_friend_request'),
    path('friend_request/reject/<int:friend_request_id>', reject_invitation, name='reject_friend_request'),
    path('delete_sent_request/<int:friend_request_id>/', delete_sent_request, name='delete_sent_request'),
    path('remove_friend/<int:user_id>', remove_friend, name='remove_friend'),
    
    path('calendar/<int:year>/<str:month>/', calendar_view, name='calendar'),
    path('all_entries/', all_journal_entries_view, name='all_entries'),
    path('my_journals/<int:userID>/', my_journals_view, name='my_journals'),
    path('view_friends_journals/<int:userID>/', my_journals_view, name='view_friends_journals'),
    
    path('groups/', group, name='groups'),


    path('notifications/<int:notification_id>/', mark_notification_as_read, name='mark_notification_as_read'),
    path('notifications/', mark_all_notification_as_read, name='mark_all_notification_as_read'),
    #path('notifications/', views.notifications_panel, name='notifications_panel'),

    path('create_group/', create_group, name='create_group'),
    path('groups/<int:group_id>/', group_dashboard, name='group_dashboard'),
    path('groups/<int:group_id>/edit', edit_group, name='edit_group'),
    path('groups/<int:group_id>/leave', leave_group, name='leave_group'),
    path('groups/<int:group_id>/delete', delete_group, name='delete_group'),
    path(
        'groups/<int:group_id>/remove_player/<int:player_id>',
        remove_player_from_group,
        name='remove_player_from_group'
    ),
    path(
        'invite_to_group/', send_group_request, name='invite_group_member'
    )


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
