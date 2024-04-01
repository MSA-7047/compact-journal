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
    path('ckeditor5/image_upload/', custom_upload_file, name='custom_ck_editor_5_upload_file'),

    path('log_in/', LogInView.as_view(), name='log_in'),
    path('log_out/', log_out, name='log_out'),
    
    path('password/', PasswordView.as_view(), name='password'),
    path('edit_profile/', ProfileUpdateView.as_view(), name='edit_profile'),
    path('view_profile/', ProfileView.as_view(), name='view_profile'),
    path('view_friends_profile/<int:friendID>', view_friends_profile, name='view_friends_profile'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('sign_up/', SignUpView.as_view(), name='sign_up'),

    path('create_journal/', create_journal, name='create_journal'),
    path('journal_dashboard/<int:journal_id>/', journal_dashboard, name='journal_dashboard'),
    path('delete_journal/<int:journal_id>/', delete_journal, name='delete_journal'),
    path('edit_journal/<int:journal_id>/', edit_journal, name='edit_journal'),

    path('create_entry/<int:journal_id>', create_entry, name='create_entry'),
    path('delete_entry/<int:entry_id>/', delete_entry, name='delete_entry'),
    path('edit_entry/<int:entry_id>/', edit_entry, name='edit_entry'),
    path('view_entry/<int:entry_id>/', view_entry, name='view_entry'),

    path('select_template/<int:journal_id>', select_template, name='select_template'),
    path('create_template/<int:journal_id>', create_template, name='create_template'),
    path('create_journal_with_template/<int:template_id>/<int:journal_id>/', views.create_journal_From_Template, name='create_journal_with_template'),
    path('delete_template/<int:template_id>/<int:journal_id>/', DeleteTemplate, name='delete_template'),
    path('edit_template/<int:template_id>/<int:journal_id>/', EditTemplate, name='edit_template'),

    path('ckeditor5/', include('django_ckeditor_5.urls')),


    
    path('friend_requests/', view_friend_requests, name='view_friend_requests'),
    path('friends/', view_friends, name='view_friends'),
    path('send_friend_request/<int:user_id>', send_friend_request, name='send_request'),
    path('friend_request/accept/<int:friend_request_id>', accept_invitation, name='accept_friend_request'),
    path('friend_request/reject/<int:friend_request_id>', reject_invitation, name='reject_friend_request'),
    path('delete_sent_request/<int:friend_request_id>/', delete_sent_request, name='delete_sent_request'),
    path('remove_friend/<int:user_id>', remove_friend, name='remove_friend'),
    

    path('view_journal_entries/<int:user_id>/<int:journal_id>/', view_journal_entries, name='journal_entries'),
    path('view_journals/<int:user_id>/', all_journals_view, name='view_journals'),
    
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
        'groups/<int:group_id>/send_group_request/', send_group_request, name='send_group_request'
    ),
    path('groups/<int:group_id>/accept-group-request', accept_group_request, name='accept_group_request'),
    path('groups/<int:group_id>/reject-group-request', reject_group_request, name='reject_group_request'),

    path('groups/<int:group_id>/select-new-owner', select_new_owner, name='select_new_owner'),

    path('groups/<int:group_id>/create-group-journal', create_group_journal, name='create_group_journal'),
    path('groups/<int:group_id>/edit_group_journal/<int:journal_id>', edit_group_journal, name='edit_group_journal'),
    path('groups/<int:group_id>/delete_group_journal/<int:journal_id>', delete_group_journal, name='delete_group_journal'),
    path('groups/<int:group_id>/view_group_journals', view_group_journals, name='view_group_journals'),

    path('export_entry_as_PDF/<int:entry_id>/', export_single_entry_as_PDF, name='export_entry'),
    path('export_journal_as_PDF/<str:journal_entries>', export_journal_as_PDF, name='export_journal'),




] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
