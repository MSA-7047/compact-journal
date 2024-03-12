from django import forms
from journal.models import Group, GroupMembership


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