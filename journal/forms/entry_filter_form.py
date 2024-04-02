from datetime import timedelta, datetime
from django import forms
from django.utils import timezone
from journal.models import Entry


class EntryFilterForm(forms.Form):

    entry_date = forms.ChoiceField(
        choices=(
            ('', '---------'),
            ('24h', 'Within 24 Hours'),
            ('3d', 'Within 3 Days'),
            ('1w', 'Within 1 Week'),
            ('1m', 'Within 1 Month'),
            ('6m+', '6+ Months')
        ), 
        required=False
    )

    mood = forms.ChoiceField(
        choices=(
            ('', '---------'),
            ("Sad", "Sad"),
            ("Happy", "Happy"),
            ("Angry", "Angry"),
            ("Neutral", "Neutral"),
            ("Excited", "Excited"),
            ("Confused", "Confused"),
            ("Surprised", "Surprised"),
            ("Hopeful", "Hopeful"),
            ("Frustrated", "Frustrated"),
            ("Grateful", "Grateful"),
            ("Relaxed", "Relaxed"),
            ("Optimistic", "Optimistic"),
            ("Anxious", "Anxious"),
        ), 
        required=False
    )

    title_search = forms.CharField(required=False)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def get_time_range(interval: str) -> datetime:
        return timezone.now() - {
            '24h': timedelta(days=1),
            '3d': timedelta(days=3),
            '1w': timedelta(weeks=1),
            '1m': timedelta(weeks=4),
            '6m+': timedelta(weeks=26),
        }[interval]

    def filter_entries(self, journal):
        
        myjournals = Entry.objects.filter(journal=journal)
        title_contains = self.cleaned_data.get('title_search')
        entry_date = self.cleaned_data.get('entry_date')
        mood = self.cleaned_data.get('mood')

        if title_contains:
            myjournals = myjournals.filter(title__icontains=title_contains)
        if mood:
            myjournals = myjournals.filter(mood = mood)

        if entry_date:
            myjournals = myjournals.filter(
                entry_date__gte=EntryFilterForm.get_time_range(entry_date)
            )

        return myjournals
