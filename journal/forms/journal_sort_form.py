from django import forms


class JournalSortForm(forms.Form):

    ORDER_CHOICES = [
        ('ascending', 'Ascending'),
        ('descending', 'Descending'),
    ]
    sort_by_entry_date = forms.ChoiceField(choices=ORDER_CHOICES)
