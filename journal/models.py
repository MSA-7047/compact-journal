from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from libgravatar import Gravatar

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
    dob = models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True, default='')    # This implementation could need refactoring based on calendar implementation
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
