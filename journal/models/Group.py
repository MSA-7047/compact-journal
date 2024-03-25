from django.db import models


class Group(models.Model):

    group_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, blank=False)
    description = models.CharField(max_length=50, blank=True)

    class Meta:
        app_label = 'journal'

    def is_user_member(self, user):
        return self.group_membership_set.filter(user=user).exists()

    def __str__(self):
        return self.name
