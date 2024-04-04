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
from journal.models.Notification import UserMessage
from journal.views.notifications import *
from journal.models.Cooldown import ActionCooldown
from django.db import transaction


def level_up_message(request):
    """
    Fetches unread messages for the request's user, sends a notification for each,
    and marks them as read.
    """
    user_messages = UserMessage.objects.filter(user=request.user, read=False)
    for msg in user_messages:
        messages.add_message(request, 35, msg.message)
        msg.read = True
        msg.save()


class ProfileView(LoginRequiredMixin, DetailView):
    """Display user profile screen"""

    def get_context_data(self, **kwargs):
        user = self.request.user
        recent_points = Points.objects.filter(user=user).order_by("-id")[:5]

        level_data = points_to_next_level(user)

        username = user.username

        context = super().get_context_data(**kwargs)
        context["total_points"] = calculate_user_points(user)
        context["points_to_next_level"] = level_data["points_to_next_level"]
        context["points_needed"] = level_data["points_needed"]
        context["recent_points"] = recent_points
        context["user_username"] = username
        return context

    template_name = "view_profile.html"

    def get(self, request, *args, **kwargs):
        level_up_message(request)
        return super().get(request, *args, **kwargs)

    def get_object(self):
        """Return the object (user) to be updated."""
        user = self.request.user
        return user


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Display user profile editing screen, and handle profile modifications."""

    model = UserForm
    template_name = "edit_profile.html"
    form_class = UserForm

    def get_object(self):
        """Return the object (user) to be updated."""
        return self.request.user

    def form_valid(self, form):
        """Process a valid form."""

        user = self.request.user

        if ActionCooldown.can_perform_action(user, "update_profile", cooldown_hours=1):
            messages.success(self.request, "Profile updated! Points awarded.")
            give_points(self.request, 20, "Profile Updated.")
        else:
            messages.success(
                self.request,
                "Profile updated! However, you must wait before getting points again.",
            )

        create_notification(self.request, "Profile was updated.", "info")
        give_points(self.request, 200, "Profile Updated.")

        return super().form_valid(form)

    def get_success_url(self):
        """Return redirect URL after successful update."""
        return reverse("view_profile")


@login_required
def dashboard(request):
    """Display the current user's dashboard."""
    today = datetime.now().date()

    current_user = request.user
    user_groups = current_user.groups.all()

    current_year = datetime.now().year
    current_month = datetime.now().strftime("%B")
    my_journals = current_user.journals.all()
    notifications = Notification.objects.filter(
        user=request.user, is_read=False
    ).order_by("-time_created")
    level_data = points_to_next_level(request.user)
    level_up_message(request)

    return render(
        request,
        "dashboard.html",
        {
            "user": current_user,
            "groups": user_groups,
            "current_year": current_year,
            "current_month": current_month,
            "my_journals": my_journals or None,
            "notifications": notifications,
            "total_points": calculate_user_points(request.user),
            "points_needed": level_data["points_needed"],
        },
    )


@login_required
def delete_account(request):
    if request.method == "POST":
        form = ConfirmDeletionForm(request.POST)
        if form.is_valid() and form.clean_confirmation():
            to_del = request.user

            with transaction.atomic():
                to_del.delete()
                logout(request)

            return redirect("home")

    else:
        form = ConfirmDeletionForm()

    return render(request, "delete_account.html", {"form": form, "is_account": True})


from django.db.models import Sum
from journal.models import Points


def calculate_user_points(user):
    """
    Calculate the total points for a given user.
    """
    total_points = Points.objects.filter(user=user).aggregate(total=Sum("points"))[
        "total"
    ]
    return total_points if total_points is not None else 0


def points_to_next_level(user):
    total_points = calculate_user_points(user)
    user_level, _ = Level.objects.get_or_create(user=user)
    level_data = user_level.calculate_level(total_points)
    return level_data


@login_required
def give_points(request, points, description):
    current_user = request.user

    Points.objects.create(user=current_user, points=points, description=description)
