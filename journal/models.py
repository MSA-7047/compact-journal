from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from libgravatar import Gravatar
from django_countries.fields import CountryField

class Journal(models.Model):
    

    """Model used for creating Journals, with attached parameters."""
    #Defines the name
    journal_title = models.CharField(max_length=50, blank=False)
    # Defines the description
    journal_description = models.TextField(max_length=1000)
    #
    journal_bio = models.TextField(max_length=10000)
    #Defines the due Date
    entry_date = models.DateTimeField()
    #Mood tracker
    journal_mood = models.CharField(max_length=50, blank=False)



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
    friends = models.ManyToManyField('self',symmetrical=False, blank=True)
    dob = models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True, default='')    # This implementation could need refactoring based on calendar implementation
    location = models.CharField(max_length=50, blank=False)
    nationality = CountryField()
    date_joined = models.DateTimeField(auto_now_add=True)

    user_journals = models.ManyToManyField(Journal, related_name="user_journals")


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

    def send_friend_request(self, user):
        """Invite a user to join the team."""
        sender = self
        invitation, created = FriendRequest.objects.get_or_create(user=user, sender=sender)
        return invitation

    def accept_request(self, user):
        """Accept a team invitation for a user."""
        request = self.invitations.filter(user=user, is_accepted=False).first()
        if request:
            self.friends.add(user)
            request.is_accepted = True
            request.save()
            return True
        return False

    def reject_request(self, user):
        """Reject a team invitation for a user."""
        request = self.invitations.filter(user=user, is_accepted=False).first()
        if request:
            request.delete()
            return True
        return False
    
class FriendRequest(models.Model):
    """Model representing invitations for a team"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invitations')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invitations')
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

