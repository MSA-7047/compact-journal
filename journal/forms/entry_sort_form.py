from django import forms


class EntrySortForm(forms.Form):
    """Form sorting Entries in a Journal in ascending or descending order."""
    
    ORDER_CHOICES = [
        ('ascending', 'Ascending'),
        ('descending', 'Descending'),
    ]
    sort_by_entry_date = forms.ChoiceField(choices=ORDER_CHOICES)
