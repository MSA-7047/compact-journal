from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from libgravatar import Gravatar

class User(AbstractUser):
    """Model used for user authentication, and team member related information."""

    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[RegexValidator(
            regex=r'^@\w{3,}$',
            message='Username must consist of @ followed by at least three alphanumericals'
        )]
    )
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(unique=True, blank=False)


    class Meta:
        """Model options."""

        ordering = ['last_name', 'first_name']

    def full_name(self):
        """Return a string containing the user's full name."""

        return f'{self.first_name} {self.last_name}'

    def gravatar(self, size=120):
        """Return a URL to the user's gravatar."""

        gravatar_object = Gravatar(self.email)
        gravatar_url = gravatar_object.get_image(size=size, default='mp')
        return gravatar_url

    def mini_gravatar(self):
        """Return a URL to a miniature version of the user's gravatar."""
        
        return self.gravatar(size=60)


class Group(models.Model):
    """Model used for information about a group"""

    name = models.CharField(max_length=30, blank=False, validators=[RegexValidator(regex=r'^[a-zA-Z]+$', message='Name must consist of letters only')])
    group_id = models.AutoField(primary_key=True)

    def is_user_member(self, user):
        """Check if a user is a member of the group"""
        return self.groupmembership_set.filter(user=user).exists()

    def __str__(self):
        return self.name


class GroupMembership(models.Model):
    """Model used to check whether a user is a member of a group"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    is_owner = models.BooleanField(blank=False, default=False)

    class Meta:
        unique_together = "user", "group"
