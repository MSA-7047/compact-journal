from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from libgravatar import Gravatar
from django_countries.fields import CountryField
from .Group import Group
from .FriendRequest import FriendRequest



class User(AbstractUser):
    """"""

    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^@\w{3,}$',
                message="Username must consist of @ followed by at least 3 alphanumerical characters"
            )
        ]
    )
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(unique=True, blank=False)
    friends = models.ManyToManyField('self', symmetrical=False, blank=True)
    dob = models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True, default='')
    groups = models.ManyToManyField(Group, through='GroupMembership')
    location = models.CharField(max_length=50, blank=False)
    nationality = CountryField(blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)


    class Meta:
        app_label = 'journal'
        ordering = ['last_name', 'first_name']

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def gravatar(self, size=120):
        gravatar_object = Gravatar(self.email)
        return gravatar_object.get_image(size=size, default='mp')

    def mini_gravatar(self):
        return self.gravatar(size=60)

    def send_friend_request(self, user):
        invitation, _ = FriendRequest.objects.get_or_create(recipient=user, sender=self)
        return invitation
    
    def accept_request(self, user):
    # Retrieve the friend request
        request = self.invitations.filter(recipient=self, sender=user, status='Pending').first()

        if not request:
            return False

        # Add the sender to the user's friends list
        self.friends.add(user)

        # Update the status of the friend request
        request.status = 'Accepted'
        request.save()

        return True

    def reject_request(self, user):
        request = self.invitations.filter(recipient=self, sender=user, status='Pending').first()
        if not request:
            return False
        request.status = 'Rejected'
        request.save()
        return True
