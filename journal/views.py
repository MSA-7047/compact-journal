from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.views.generic.edit import FormView, UpdateView
from django.urls import reverse
from journal.forms import LogInForm, PasswordForm, UserForm, SignUpForm, CreateJournalForm, SendFriendRequestForm
from journal.helpers import login_prohibited
from django.views.generic import DetailView
from .models import Journal, FriendRequest, User


@login_required
def dashboard(request):
    """Display the current user's dashboard."""

    current_user = request.user
    return render(request, 'dashboard.html', {'user': current_user})


@login_prohibited
def home(request):
    """Display the application's start/home screen."""

    return render(request, 'home.html')


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
        user = self.request.user
        return user

    def get_success_url(self):
        """Return redirect URL after successful update."""
        messages.add_message(self.request, messages.SUCCESS, "Profile updated!")
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)


class SignUpView(LoginProhibitedMixin, FormView):
    """Display the sign up screen and handle sign ups."""

    form_class = SignUpForm
    template_name = "sign_up.html"
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)
    
@login_required
def view_friend_requests(request):
    requests = FriendRequest.objects.filter(user=request.user, is_accepted=False)

    sent_pending_invitations = request.user.sent_invitations.filter(status='pending')
    sent_accepted_invitations = request.user.sent_invitations.filter(status='accepted')
    sent_rejected_invitations = request.user.sent_invitations.filter(status='rejected')

    return render(request, 'friend_requests.html', {'requests': requests, 'sent_pending_invitations': sent_pending_invitations, 'sent_accepted_invitations': sent_accepted_invitations, 'sent_rejected_invitations': sent_rejected_invitations})

@login_required
def view_friends(request):
    user = request.user
    friends = user.friends.all()
    return render(request, 'friends.html', {"friends": friends})

@login_required
def send_friend_request(request, user_id):
    user = get_object_or_404(User, pk = user_id)
    friends = user.friends.all()

    if request.method == 'POST':
        form = SendFriendRequestForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            FriendRequest.objects.get_or_create(user=user, sender=request.user, status='pending')
            return redirect('send_request', user_id=user_id)
    else:
        form = SendFriendRequestForm()

    return render(request, 'friends.html', {'add_member_form': form, "user": user, "friends": friends})

@login_required
def accept_invitation(request, friend_request_id):
    friend_request = get_object_or_404(FriendRequest, id=friend_request_id, user=request.user, is_accepted=False)

    # Add the user to the team and mark the invitation as accepted
    friend_request.user.friends.add(friend_request.sender)
    friend_request.sender.friends.add(friend_request.user)
    friend_request.is_accepted = True
    friend_request.status = 'accepted'

    friend_request.save()
    #invitation.delete()

    return redirect('view_friend_requests')

@login_required
def reject_invitation(request, friend_request_id):
    friend_request = get_object_or_404(FriendRequest, id=friend_request_id, user=request.user, is_accepted=False)

    friend_request.status =  'rejected'
    friend_request.save()
    #invitation.delete()

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
@login_required    
def CreateJournalView(request):
    form = CreateJournalForm()
    current_user = request.user
    if (request.method == 'POST'):
        form = CreateJournalForm(request.POST)
        if (form.is_valid()):
            journal_title = form.cleaned_data.get(label="journal_title")
            journal_description = form.cleaned_data.get(label="journal_description")
            journal_bio = form.cleaned_data.get(label="journal_bio")
            journal_mood = form.cleaned_data.get(label="journal_mood")
            journal = Journal.objects.create(journal_title = journal_title, journal_description = journal_description, journal_bio = journal_bio, journal_mood = journal_mood)
            journal.save()
            current_user.add(journal)
            



    





    pass
    
