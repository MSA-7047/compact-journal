"""Forms for the journal app."""
from django import forms
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator
from .models import User, Group, GroupMembership, Journal, FriendRequest
from django_countries.widgets import CountrySelectWidget
from django_ckeditor_5.widgets import CKEditor5Widget
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta


class LogInForm(forms.Form):
    """Form enabling registered users to log in."""

    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

    def get_user(self):
        """Returns authenticated user if possible."""

        user = None
        if self.is_valid():
            username = self.cleaned_data.get('username')
            password = self.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
        return user


class UserForm(forms.ModelForm):
    """Form to update user profiles."""

    class Meta:
        """Form options."""

        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'dob',
            'bio',
            'location',
            'nationality'
        ]

        labels = {
            'dob': 'Date of Birth',
            'nationality': 'Nationality'
        }

        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }


class NewPasswordMixin(forms.Form):
    """Form mixing for new_password and password_confirmation fields."""

    new_password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        validators=[RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
            message='Password must contain an uppercase character, a lowercase '
                    'character and a number'
            )]
    )
    password_confirmation = forms.CharField(label='Password confirmation', widget=forms.PasswordInput())

    def clean(self):
        """Form mixing for new_password and password_confirmation fields."""

        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error('password_confirmation', 'Confirmation does not match password.')


class PasswordForm(NewPasswordMixin):
    """Form enabling users to change their password."""

    password = forms.CharField(label='Current password', widget=forms.PasswordInput())

    def __init__(self, user=None, **kwargs):
        """Construct new form instance with a user instance."""
        
        super().__init__(**kwargs)
        self.user = user

    def clean(self):
        """Clean the data and generate messages for any errors."""

        super().clean()
        password = self.cleaned_data.get('password')
        if self.user is not None:
            user = authenticate(username=self.user.username, password=password)
        else:
            user = None
        if user is None:
            self.add_error('password', "Password is invalid")

    def save(self):
        """Save the user's new password."""

        new_password = self.cleaned_data['new_password']
        if self.user is not None:
            self.user.set_password(new_password)
            self.user.save()
        return self.user


class SignUpForm(NewPasswordMixin, forms.ModelForm):
    """Form enabling unregistered users to sign up."""

    class Meta:
        """Form options."""

        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

    def save(self):
        """Create a new user."""

        super().save(commit=False)
        user = User.objects.create_user(
            self.cleaned_data.get('username'),
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            email=self.cleaned_data.get('email'),
            password=self.cleaned_data.get('new_password'),
        )
        return user


class GroupForm(forms.ModelForm):
    """Form allowing the user to create a group"""

    class Meta:
        model = Group
        fields = ['name']

    def save(self, commit=True, creator=None):
        group_instance = super().save(commit=False)
        if commit and not group_instance.pk:
            group_instance.save()
            GroupMembership.objects.create(
                user=creator,
                group=group_instance,
                is_owner=True
            )
        return group_instance


class SendFriendRequestForm(forms.Form):

    recipient = forms.ModelChoiceField(queryset=User.objects.all(), label='Select User')

    class Meta:
        model = FriendRequest
        fields = ['recipient']

    def __init__(self, *args, user=None,  **kwargs):
        friends = user.friends.all()
        super().__init__(*args, **kwargs)
        if friends is not None:
            self.fields['recipient'].queryset = User.objects.exclude(id__in=[user.id for user in friends]).exclude(id=user.id)


class CreateJournalForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # it is required to set it False,
        # otherwise it will throw error in console
        self.fields["journal_bio"].required = False

    # journal_title = forms.CharField(label="Title")
    # journal_description = forms.CharField(label="Description")
    # journal_bio = forms.CharField(label="Bio")
    # journal_mood = forms.ChoiceField(choices=(
    #     ('Happy', 'Happy'),
    #     ('Sad', 'Sad'),
    #     ('Angry', 'Angry'),
    #     ('Neutral', 'Neutral'),
    # ), required=True)


    # journal_title = forms.CharField(label="Title")
    # journal_description = forms.CharField(label="Description")
    # journal_bio = forms.CharField(label="Bio")
    # journal_mood = forms.CharField(label="Mood")

    class Meta:
        model = Journal

        fields = ['journal_title', 'journal_description', 'journal_bio', 'journal_mood', 'private']


class EditJournalInfoForm(forms.ModelForm):

    # class Meta:
    #     model = Journal
    #     fields = ['journal_title', 'journal_description', 'journal_bio']



    # def save(self, commit=True):
    #     instance = super().save(commit=False)
    #     instance.journal_title = self.cleaned_data['journal_title']
    #     instance.journal_description = self.cleaned_data['journal_description']
    #     instance.journal_bio = self.cleaned_data['journal_bio']
    #     if commit:
    #         instance.save()
    #     return instance

    #journal_bio = forms.CharField(widget=CKEditor5Widget(config_name='extends'), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # it is required to set it False,
        # otherwise it will throw error in console
        self.fields["journal_bio"].required = False

    class Meta:
        model = Journal
        fields = ['journal_title', 'journal_description', 'journal_bio', 'journal_mood']


class JournalFilterForm(forms.Form):

    entry_date = forms.ChoiceField(choices=(
        ('', '---------'),
        ('24h', 'Within 24 Hours'),
        ('3d', 'Within 3 Days'),
        ('1w', 'Within 1 Week'),
        ('1m', 'Within 1 Month'),
        ('6m+', '6+ Months')
    ), required=False)

    mood = forms.ChoiceField(choices=(
        ('', '---------'),
        ('Happy', 'Happy'),
        ('Sad', 'Sad'),
        ('Angry', 'Angry'),
        ('Neutral', 'Neutral'),
    ), required=False)

    title_search = forms.CharField(required=False)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def filter_tasks(self):

        myjournals = Journal.objects.all()
        #label = self.cleaned_data.get('label')
        title_contains = self.cleaned_data.get('title_contains')
        entry_date = self.cleaned_data.get('entry_date')
        mood = self.cleaned_data.get('mood')

        #if label:
           # tasks = tasks.filter(label=label)
        if title_contains:
            myjournals = myjournals.filter(journal_title__icontains=title_contains)
        if mood:
            myjournals = myjournals.filter(journal_mood = mood)
        if entry_date:
            if entry_date == '24h':
                time_threshold = timezone.now() - timedelta(days=1)
                myjournals = myjournals.filter(entry_date__gte=time_threshold)
            elif entry_date == '3d':
                time_threshold = timezone.now() - timedelta(days=3)
                myjournals = myjournals.filter(entry_date__gte=time_threshold)
            elif entry_date == '1w':
                time_threshold = timezone.now() - timedelta(weeks=1)
                myjournals = myjournals.filter(entry_date__gte=time_threshold)
            elif entry_date == '1m':
                time_threshold = timezone.now() - timedelta(weeks=4)
                myjournals = myjournals.filter(entry_date__gte=time_threshold)
            elif entry_date == '6m+':
                time_threshold = timezone.now() - timedelta(weeks=26)
                myjournals = myjournals.filter(entry_date__gte=time_threshold)

        return myjournals


class JournalSortForm(forms.Form):

    ORDER_CHOICES = [
        ('ascending', 'Ascending'),
        ('descending', 'Descending'),
    ]
    sort_by_entry_date = forms.ChoiceField(choices=ORDER_CHOICES)


class ConfirmAccountDeleteForm(forms.Form):
    confirmation = forms.CharField(label='Type "YES" to confirm deletion', max_length=3)


class CreateTemplateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["bio"].required = False

    class Meta:
        model = Template
        fields = ['title', 'description', 'bio',]


class SendGroupRequestForm(forms.Form):
    recipient = forms.ModelChoiceField(queryset=User.objects.all(), label='Select User')
    def __init__(self, *args, currentUser=None, **kwargs):
        super().__init__(*args, **kwargs)
        if currentUser is not None:
            self.fields['recipient'].queryset = User.objects.exclude(username=currentUser.username)

