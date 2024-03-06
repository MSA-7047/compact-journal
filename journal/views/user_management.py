from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView

from journal.models import *


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


@login_required
def dashboard(request):
    """Display the current user's dashboard."""
    today = datetime.now().date()

    current_user = request.user
    user_groups = current_user.groups.all()

    current_year = datetime.now().year
    current_month = datetime.now().strftime("%B")
    todays_journal = Journal.objects.filter(entry_date__date=today)

    return render(
        request,
        'dashboard.html',
        {
            'user': current_user,
            'groups': user_groups,
            'current_year': current_year, 'current_month': current_month,
            'todays_journal': todays_journal or None
        }
    )


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
