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
from journal.forms import *
from journal.models import *
from journal.views.notifications import *
from django.db import transaction



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

        """Notification Creation"""
        notif_message = "Profile update message. It can be changed whenever I want it to."
        create_notification(self.request, notif_message, "info")
        
        user = self.request.user

        Points.objects.create(user=user, points=600, description="test")


        total_points = calculate_user_points(user)
        user_level = self.request.user.level.level         
        print(f"User Level: {user_level}")

        print(f"Total Points: {total_points}")

        messages.success(self.request, "Profile updated!")
        return super().form_valid(form)

    def get_success_url(self):
        """Return redirect URL after successful update."""
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)



@login_required
def dashboard(request):
    """Display the current user's dashboard."""
    today = datetime.now().date()

    current_user = request.user
    user_groups = current_user.groups.all()

    current_year = datetime.now().year
    current_month = datetime.now().strftime("%B")
    my_journals = current_user.journals.all()
    print(my_journals)
    notifications = Notification.objects.filter(user=request.user, is_read=False)

    return render(
        request,
        'dashboard.html',
        {
            'user': current_user,
            'groups': user_groups,
            'current_year': current_year, 'current_month': current_month,
            'my_journals': my_journals or None,
            'notifications': notifications
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

from django.db.models import Sum
from journal.models import Points

def calculate_user_points(user):
    """
    Calculate the total points for a given user.

    Parameters:
    - user: The User instance for whom to calculate points.

    Returns:
    - The total points as an integer.
    """
    total_points = Points.objects.filter(user=user).aggregate(total=Sum('points'))['total']
    return total_points if total_points is not None else 0


