from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.views.generic.edit import FormView, UpdateView
from django.urls import reverse, reverse_lazy
from journal.models import *
from journal.forms import *
from journal.helpers import login_prohibited
from django.views.generic import DetailView
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.contrib.messages.views import SuccessMessageMixin

from django.db import transaction
from .models.Notification import Notification

def createTemplate(currentUser):
    html_file_paths = [
        'journal/journal_templates/template1.html',
        'journal/journal_templates/template2.html',
        'journal/journal_templates/template3.html',
        'journal/journal_templates/template4.html',
        'journal/journal_templates/template5.html',
    ]

    for i, html_file_path in enumerate(html_file_paths, start=1):
        with open(html_file_path, 'r') as html_file:
            html_content = html_file.read()

        Template.objects.create(
            title=f"Default Template {i}",
            description=f"Description for Default Template {i}",
            bio=html_content,
            owner=currentUser
        )


@login_required
def dashboard(request):
    """Display the current user's dashboard."""
    today = datetime.now().date()

    current_user = request.user
    user_groups = current_user.groups.all()

    current_year = datetime.now().year
    current_month = datetime.now().strftime("%B")
    todays_journal = Journal.objects.filter(entry_date__date=today).filter(journal_owner=current_user)
    notifications = Notification.objects.filter(user=request.user, is_read=False)

    return render(
        request,
        'dashboard.html',
        {
            'user': current_user,
            'groups': user_groups,
            'current_year': current_year, 'current_month': current_month,
            'todays_journal': todays_journal or None,
            'notifications': notifications
        }
    )


@login_prohibited
def home(request):
    """Display the application's start/home screen."""

    return render(request, 'home.html')


@login_required
def group(request) -> HttpResponse:
    """Display the list of groups the current user is in"""
    current_user = request.user
    current_user_groups = current_user.groups.all()
    return render(request, 'group.html', {'user': current_user, 'groups': current_user_groups})


@login_required
def group_dashboard(request, given_group_id) -> HttpResponse:
    """Displays the journals & members of a given group"""
    current_user = request.user
    given_group = get_object_or_404(Group, pk=given_group_id)
    all_members_in_group = ...
    group_journals = ...
    is_owner = ...
    return render(
        request,
        'group_dashboard.html',
        {
            'group': given_group,
            'members': all_members_in_group,
            'journals': group_journals,
            'is_owner': is_owner
        }
    )


@login_required
def create_group(request) -> HttpResponse:
    """Display create group screen and handles create group form"""
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save(commit=True, creator=request.user)
            return redirect('groups')
    else:
        form = GroupForm()

    return render(request, 'create_group.html', {'form': form})


@login_required
def group(request) -> HttpResponse:
    """Display the list of groups the current user is in"""
    current_user = request.user
    current_user_groups = current_user.groups
    return render(request, 'group.html', {'user': current_user, 'groups': current_user_groups})


class LoginProhibitedMixin:
    """Mixin that redirects when a user is logged in."""

    redirect_when_logged_in_url = None

    def dispatch(self, *args, **kwargs):
        """Redirect when logged in, or dispatch as normal otherwise."""
        if self.request.user.is_authenticated:
            return self.handle_already_logged_in(*args, **kwargs)
        return super().dispatch(*args, **kwargs)

    def handle_already_logged_in(self, *args, **kwargs):
        url = self.get_redirect_when_logged_in_url()
        return redirect(url)

    def get_redirect_when_logged_in_url(self):
        """Returns the url to redirect to when not logged in."""
        if self.redirect_when_logged_in_url is None:
            raise ImproperlyConfigured(
                "LoginProhibitedMixin requires either a value for "
                "'redirect_when_logged_in_url', or an implementation for "
                "'get_redirect_when_logged_in_url()'."
            )
        else:
            return self.redirect_when_logged_in_url


class LogInView(LoginProhibitedMixin, View):
    """Display login screen and handle user login."""

    http_method_names = ['get', 'post']
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def get(self, request):
        """Display log in template."""

        self.next = request.GET.get('next') or ''
        return self.render()

    def post(self, request):
        """Handle log in attempt."""

        form = LogInForm(request.POST)
        self.next = request.POST.get('next') or settings.REDIRECT_URL_WHEN_LOGGED_IN
        user = form.get_user()
        if user is not None:
            login(request, user)
            return redirect(self.next)
        messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
        return self.render()

    def render(self):
        """Render log in template with blank log in form."""

        form = LogInForm()
        return render(self.request, 'log_in.html', {'form': form, 'next': self.next})


def log_out(request):
    """Log out the current user"""

    logout(request)
    return redirect('home')


class PasswordView(LoginRequiredMixin, FormView):
    """Display password change screen and handle password change requests."""

    template_name = 'password.html'
    form_class = PasswordForm

    def get_form_kwargs(self, **kwargs):
        """Pass the current user to the password change form."""

        kwargs = super().get_form_kwargs(**kwargs)
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        """Handle valid form by saving the new password."""

        form.save()
        login(self.request, self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect the user after successful password change."""

        messages.add_message(self.request, messages.SUCCESS, "Password updated!")
        return reverse('dashboard')


class ProfileView(LoginRequiredMixin, DetailView):
    """Display user profile screen"""

    template_name = "view_profile.html"

    def get_object(self):
        """Return the object (user) to be updated."""
        user = self.request.user
        return user


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Display user profile editing screen, and handle profile modifications."""

    model = UserForm
    template_name = "profile.html"
    form_class = UserForm

    def get_object(self):
        """Return the object (user) to be updated."""
        return self.request.user

    def form_valid(self, form):
        """Process a valid form."""
        create_notification(self.request)
        messages.success(self.request, "Profile updated!")
        return super().form_valid(form)

    def get_success_url(self):
        """Return redirect URL after successful update."""
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)


class SignUpView(LoginProhibitedMixin, FormView):
    """Display the sign up screen and handle sign ups."""

    form_class = SignUpForm
    template_name = "sign_up.html"
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def form_valid(self, form):
        self.object = form.save()
        createTemplate(self.object)
        login(self.request, self.object)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)


def get_friend_requests_and_sent_invitations(user):
    requests = FriendRequest.objects.filter(recipient=user, is_accepted=False)
    sent_pending_invitations = user.sent_invitations.filter(status='pending')
    sent_accepted_invitations = user.sent_invitations.filter(status='accepted')
    sent_rejected_invitations = user.sent_invitations.filter(status='rejected')
    return requests, sent_pending_invitations, sent_accepted_invitations, sent_rejected_invitations


@login_required
def view_friend_requests(request):
    requests, sent_pending_invitations, sent_accepted_invitations, sent_rejected_invitations = get_friend_requests_and_sent_invitations(request.user)
    form = SendFriendRequestForm(user=request.user)
    create_notification(request)

    return render(request, 'friend_requests.html', {'form': form, 'requests': requests, 'sent_pending_invitations': sent_pending_invitations, 'sent_accepted_invitations': sent_accepted_invitations, 'sent_rejected_invitations': sent_rejected_invitations})


@login_required
def view_friends(request):
    friends = request.user.friends.all()
    return render(request, 'friends.html', {"friends": friends})


@login_required
def view_friends_profile(request, friendID):
    friend = get_object_or_404(User, id=friendID)
    return render(request, 'view_friends_profile.html', {"user": friend})


@login_required
def send_friend_request(request, user_id):
    if request.method == 'POST':
        form = SendFriendRequestForm(request.POST, user=request.user)
        if form.is_valid():
            recipient = form.cleaned_data['recipient']
            FriendRequest.objects.get_or_create(recipient=recipient, sender=request.user, status='pending')
            return redirect('send_request', user_id=user_id)
    else:
        form = SendFriendRequestForm(user=request.user)

    requests, sent_pending_invitations, sent_accepted_invitations, sent_rejected_invitations = get_friend_requests_and_sent_invitations(request.user)

    return render(request, 'friend_requests.html', {'form': form, 'requests': requests, 'sent_pending_invitations': sent_pending_invitations, 'sent_accepted_invitations': sent_accepted_invitations, 'sent_rejected_invitations': sent_rejected_invitations})


@login_required
def accept_invitation(request, friend_request_id):
    friend_request = get_object_or_404(FriendRequest, id=friend_request_id, recipient=request.user, is_accepted=False)

    # Add the user to the team and mark the invitation as accepted
    friend_request.recipient.friends.add(friend_request.sender)
    friend_request.sender.friends.add(friend_request.recipient)
    friend_request.is_accepted = True
    friend_request.status = 'accepted'

    friend_request.save()

    return redirect('view_friend_requests')


@login_required
def reject_invitation(request, friend_request_id):
    friend_request = get_object_or_404(FriendRequest, id=friend_request_id, recipient=request.user, is_accepted=False)
    friend_request.status = 'rejected'
    friend_request.save()
    return redirect('view_friend_requests')


@login_required
def delete_sent_request(request, friend_request_id):
    friend_request = get_object_or_404(FriendRequest, id=friend_request_id, sender=request.user)
    friend_request.delete()
    return redirect('view_friend_requests')


@login_required
def remove_friend(request, user_id):
    friend = get_object_or_404(User, id = user_id)
    request.user.friends.remove(friend)
    friend.friends.remove(request.user)
    return redirect('friends')

# class AddJournal(SuccessMessageMixin, CreateView):
#     form_class = CreateJournalForm
#     model = Journal
#     template_name = "add_journal.html"
#     success_message = "Added Succesfully"
#     success_url = reverse_lazy('dashboard')


# class JournalDetail(DetailView):
#     model = Journal
#     context_object_name = 'journal'
#     template_name = "journal_detail.html"


class JournalDetail(DetailView):
    model = Journal
    template_name = 'journal_detail.html'

    def get_object(self, queryset=None):
        journal_id = self.kwargs.get('journal_id')
        queryset = self.get_queryset().filter(id=journal_id)
        obj = queryset.first()
        return obj


def journal_detail_view(request, journalID):
    # Retrieve the journal object based on the journal_id
    current_user = request.user
    journal = Journal.objects.get(id=journalID)

    # Pass the journal object to the template context
    return render(request, 'journal_detail.html', {'user': current_user, 'journal': journal})


@login_required    
def create_journal(request):
    today = datetime.now().date()

    current_user = request.user
    form_class = CreateJournalForm
    model = Journal
    template_name = "create_journal.html"
    success_message = "Added Succesfully"
    form = CreateJournalForm()
    current_user = request.user
    if (request.method == 'POST'):
        form = CreateJournalForm(request.POST)
        if (form.is_valid()):
            journal_title = form.cleaned_data.get("journal_title")
            journal_description = form.cleaned_data.get("journal_description")
            journal_bio = form.cleaned_data.get("journal_bio")
            journal_mood = form.cleaned_data.get("journal_mood")
            is_private = form.cleaned_data.get("private")
            journal_owner = current_user
            journal = Journal.objects.create(
                journal_title = journal_title,
                journal_description = journal_description,
                journal_bio = journal_bio,
                journal_mood = journal_mood,
                journal_owner = journal_owner,
                private = is_private
            )
            journal.save()
            #old render that would stick on create journal view after creating journal, thus repeating entry when reloaded
            #return render(request, 'dashboard.html', {'form': form, 'user': current_user, 'current_year': current_year, 'current_month': current_month, 'todays_journal': todays_journal or None})
            return redirect('/dashboard/')
        else:
            return render(request, 'create_journal.html', {'form': form, 'title': "Create Journal"})
    else:
        return render(request, 'create_journal.html', {'form': form, 'title': "Create Journal"})


@login_required    
def create_template(request):

    current_user = request.user
    form = CreateTemplateForm()
    if (request.method == 'POST'):
        form = CreateTemplateForm(request.POST)
        if (form.is_valid()):
            template = Template.objects.create(
                title = form.cleaned_data.get("title"),
                description = form.cleaned_data.get("description"),
                bio = form.cleaned_data.get("bio"),
                owner = current_user,
            )
            template.save()
            return redirect('/select-template/')
        else:
            return render(request, 'create_template.html', {'form': form})
    else:
        return render(request, 'create_template.html', {'form': form, 'title': "Create Template"})
    

def select_template(request):
    currentUser = request.user
    templates = Template.objects.filter(owner=currentUser)
    return render(request, 'select_template.html', {"templates": templates})

@login_required
def DeleteTemplate(request,templateID):
    template= get_object_or_404(Template, id=templateID)
    template.delete()
    return redirect('select_template')

def create_journal_From_Template(request, templateID):
    current_user = request.user
    template = get_object_or_404(Template, id = templateID)
    journal = Journal.objects.create(
                journal_title = template.title,
                journal_description = template.description,
                journal_bio = template.bio,
                journal_mood = "neutral",
                journal_owner = current_user,
                private = False
            )
    journal.save()
    return redirect("edit_journal", journalID=journal.id)

@login_required
def EditTemplate(request, templateID): 
    template = get_object_or_404(Template, id=templateID)
    if request.method == 'POST':
        form = CreateTemplateForm(request.POST, instance=template)
        if form.is_valid():
            form.save()
            return redirect('select_template')  # Redirect to the detail view of the edited journal
    else:
        form = CreateTemplateForm(instance=template)

    return render(request, 'create_template.html', {'form': form, 'template': template, 'title': "Update Template"})


@login_required
def EditJournal(request, journalID): 

    journal = get_object_or_404(Journal, id=journalID)

    if request.method == 'POST':
        form = CreateJournalForm(request.POST, instance=journal)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirect to the detail view of the edited journal
    else:
        form = CreateJournalForm(instance=journal)

    return render(request, 'create_journal.html', {'form': form, 'journal': journal, 'title': "Update Journal"})


@login_required
def DeleteJournal(request, journalID):
    journal = get_object_or_404(Journal, id=journalID)
    journal.delete()
    return redirect('dashboard')


@login_required
def ChangeJournalDescription(request, journalID):
    journal = get_object_or_404(Journal, id=journalID)
    
    if request.method == 'POST':
        form = EditJournalDescriptionForm(request.POST, instance=journal)
        if form.is_valid():
            new_description = form.cleaned_data['journal_description']
            journal.journal_description = new_description
            journal.save()
            return redirect('all_entries')
    else:
        form = EditJournalDescriptionForm(instance=journal)
    
    return render(request, 'change_journal_description.html', {'form': form, 'journal': journal})


@login_required
def calendar_view(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    name = "Journaller"
    month = month.capitalize()
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    cal = HTMLCalendar().formatmonth(year, month_number)
    now = datetime.now()
    current_year = now.year
    current_month = now.month
    return render(request,
                'calendar.html', {
                "name": name,
                "year": year,
                "month": month,
                "month_number": month_number,
                "cal": cal,
                "current_year": current_year,
                "current_month": current_month,
                }
                )


@login_required
def all_journal_entries_view(request):
    current_user = request.user
    # current_year = datetime.now().year
    # current_month = datetime.now().strftime("%B")
    journal_existence = Journal.objects.filter(journal_title__isnull=False)
    return render(request, 'my_journals.html', { 'user': current_user,  'journal_existence': journal_existence or False})


@login_required
def my_journals_view(request, userID):
    current_user = get_object_or_404(User, id=userID)
    isLoggedInUser = current_user == request.user
    if request.method == 'POST':
        filter_form = JournalFilterForm(current_user, request.POST)

        if filter_form.is_valid():
            myJournals = filter_form.filter_tasks()
            myJournals = myJournals.filter(journal_owner=current_user)
            sort_form = JournalSortForm(request.POST)
            if sort_form.is_valid():
                sort_order = sort_form.cleaned_data['sort_by_entry_date']
                if sort_order == 'descending':
                    myJournals = myJournals.order_by("entry_date")
                    myJournals = myJournals.reverse()
                elif sort_order == 'ascending':
                    myJournals = myJournals.order_by("entry_date")
        else:
            sort_form = JournalSortForm()
            myJournals = Journal.objects.filter(journal_owner=current_user)
            if not isLoggedInUser:
                myJournals = myJournals.filter(private=False)
            context = {

            'filter_form': filter_form,
            'sort_form': sort_form,
            'show_alert':True,
            'myJournals': myJournals,
            'user': current_user,
            'isUserCurrentlyLoggedIn': isLoggedInUser
            }
            return render(request, 'My_Journals.html', context)
        
        if not isLoggedInUser:
            myJournals = myJournals.filter(private=False)


        context = {
            'filter_form': filter_form,
            'sort_form': sort_form,
            'myJournals': myJournals,
            'user': current_user,
            'isUserCurrentlyLoggedIn': isLoggedInUser
        }
        
        return render(request, 'my_journals.html', context) 
    
    myJournals = Journal.objects.filter(journal_owner=current_user)

    if not isLoggedInUser:
            myJournals = myJournals.filter(private=False)



    filter_form = JournalFilterForm(current_user)
    sort_form = JournalSortForm()

    context = {
            'filter_form': filter_form,
            'sort_form': sort_form,
            'myJournals': myJournals or False,
            'user': current_user,
            'isUserCurrentlyLoggedIn': isLoggedInUser
        }

    return render(request, 'my_journals.html', context)


@login_required
def edit_group(request, group_id):
    """Allows owner of the group to edit the group."""
    group = get_object_or_404(Group, pk=group_id)

    if request.user != group.owner:
        # User is not the owner, return forbidden response
        return HttpResponseForbidden('You are not authorized to edit this group')

    if request.method != 'POST':
        form = GroupForm(instance=group)
        return render(request, 'edit_group.html', {'form': form})

    form = GroupForm(request.POST, instance=group)
    if form.is_valid():
        form.save()
        return JsonResponse({'message': 'Group edited successfully'})

    return JsonResponse({'errors': form.errors}, status=400)


@login_required
def send_group_request(request):
    """Allows a user to send a group request."""
    if request.method == 'POST':
        form = SendGroupRequestForm(request.POST, currentUser=request.user)
        if form.is_valid():
            recipient = form.cleaned_data['recipient']
            GroupRequest.objects.create(sender=request.user, recipient=recipient)
            return redirect('home')
    else:
        form = SendGroupRequestForm(currentUser=request.user)
    return render(request, 'send_group_request.html', {'form': form})


@login_required
def accept_group_request(request, group_request_id):
    """Allows a user that has a sent request to accept the request."""
    group_request = get_object_or_404(GroupRequest, id=group_request_id, recipient=request.user, is_accepted=True)

    # Add the user to the group
    group = group_request.group  # Assuming group_request has a ForeignKey to Group model
    user = group_request.sender  # The user who sent the group request

    # Create GroupMembership for the user
    GroupMembership.objects.create(user=user, group=group)

    group_request.status = 'accepted'
    group_request.save()
    #invitation.delete()

    return redirect('group')

@login_required
def reject_invitation(request, group_request_id):
    """Allows the user with the sent friend request to reject it"""
    group_request = get_object_or_404(GroupRequest, id=group_request_id, recipient=request.user, is_accepted=False)
    group_request.status =  'rejected'
    group_request.save()
    #invitation.delete()
    return redirect('group')



@login_required
def delete_account(request):
    if request.method == 'POST':
        form = ConfirmAccountDeleteForm(request.POST)
        if form.is_valid() and form.cleaned_data['confirmation'].upper() == "YES":
            to_del = request.user

            with transaction.atomic():
                to_del.delete()
                logout(request)

            return redirect('home')
        else:
            form.add_error('confirmation', 'Please enter "YES" to confirm deletion.')
    else:
        form = ConfirmAccountDeleteForm()

    return render(request, 'delete_account.html', {'form': form})
  

@login_required
def create_notification(request):
    current_user = request.user

    Notification.objects.create(
        user=current_user,
        message="This is a test notification message."
    )

    print("I am testing the notifications system, object creation. If this message shows, it works :)")
    messages.success(request, "Notification created!")
    
@login_required
def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    if notification.is_read:
        notification.is_read = False
    else:
        notification.is_read = True
    time = notification.timeCreated.strftime("%Y-%m-%d %H:%M:%S")
    messages.success(request, f"Notification for the {notification.notification_type} created at {time} was marked as read.")
    notification.save()

    return redirect(notification.get_absolute_url())


@login_required
def mark_all_notification_as_read(request):
    Notification.objects.filter(user=request.user).update(is_read=True)
    messages.success(request, "All notifications cleared.")
    return redirect('dashboard')

def notification_context(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user, is_read=False)
        return {'notifications': notifications}
    else:
        return {'notifications': []}
    
# @login_required
# def notifications_panel(request):
#     # Fetch notifications for the current user
#     notifications = Notification.objects.filter(user=request.user)


@login_required
def delete_sent_request(request, friend_request_id):
    """Deletes the friend request once it is accepted or deleted."""
    group_request = get_object_or_404(GroupRequest, id=group_request_id, recipient=request.user, is_accepted=False)
    group_request.delete()
    return redirect('group')

@login_required
def delete_group(request, group_id):
    """Allows the owner to delete the group"""
    group = get_object_or_404(Group, pk=group_id)

    if request.user == group.owner:
        # Only allow deletion via POST method to prevent accidental deletions
        if request.method == 'POST':
            group.delete()
            return redirect('home')
        else:
            # Handle GET requests (e.g., show a confirmation page)
            return render(request, 'confirm_group_deletion.html', {'group': group})
    else:
        return HttpResponseForbidden('You are not authorized to delete this group.')

@login_required
def leave_group(request, group_id):
    """Allows users to leave a group"""
    group = get_object_or_404(Group, pk=group_id)
    user = request.user

    if user == group.owner:
        if group.members.count() == 1:
            # The owner is the only member, delete the group
            group.delete()
            return redirect('home')
        else:
            # The owner must select a new owner before leaving
            if request.method == 'POST':
                new_owner_id = request.POST.get('new_owner')
                new_owner = get_object_or_404(User, pk=new_owner_id)
                group.owner = new_owner
                group.save()

            return render(request, 'select_new_owner.html', {'group': group})
    else:
        group_membership = GroupMembership.objects.get(group=group, user=user)
        group_membership.delete()

        if group.members.count() == 0:
            group.delete()

        return redirect('home')

@login_required
def remove_player_from_group(request, group_id, player_id):
    """Allows the owner to remove a player from the group."""


    group = get_object_or_404(Group, id=group_id)
    player = get_object_or_404(User, id=player_id)

    if request.user != group.owner:
        return HttpResponseForbidden('You are not authorized to remove a player from this group.')

    if player == group.owner:
        messages.error(request, "The owner cannot be removed from the group.")
        return redirect('group_detail', group_id=group.id)

    try:
        membership = GroupMembership.objects.get(group=group, user=player)
    except GroupMembership.DoesNotExist:
        messages.error(request, f"{player.username} is not a member of the group.")
        return redirect('group_detail', group_id=group.id)

    membership.delete()
    messages.success(request, f"Successfully removed {player.username} from the group.")

    if group.members.count() == 0:
        group.delete()
        messages.info(request, "The group has been deleted as there are no members left.")

    return redirect('group_detail', group_id=group.id)
