from django.contrib.admin import TabularInline, ModelAdmin
from django.contrib import admin
from django.db.models import Model
from .models import (
    Journal,
    User,
    Group,
    GroupJournal,
    GroupMembership,
    Template,
    Entries,
    Notification,
)


class GroupMembershipInline(TabularInline):
    """"""

    model: Model = GroupMembership
    extra: int = 1


class FriendshipInline(TabularInline):
    """"""

    model: Model = User
    extra: int = 1


class OwnershipInline(TabularInline):
    """"""

    model: Model = User


class GroupOwnershipInline(TabularInline):
    """"""

    model: Model = Group


class JournalEntryInline(TabularInline):
    """"""


class UserAdmin(ModelAdmin):
    """"""

    list_display: tuple[str] = (
        "username",
        "first_name",
        "last_name",
        "email",
        "dob",
        "bio",
        "location",
        "nationality",
        "date_joined",
    )
    inlines: list[TabularInline] = [GroupMembershipInline, FriendshipInline]


class JournalAdmin(ModelAdmin):
    """"""

    list_display: tuple[str] = (
        "journal_title",
        "journal_description",
        "journal_bio",
        "entry_date",
        "last_edited",
        "journal_mood",
        "private",
    )
    inlines: list[TabularInline] = [OwnershipInline]


class GroupAdmin(ModelAdmin):
    """"""

    list_display: tuple[str] = ("name",)
    inlines: list[TabularInline] = [GroupMembershipInline]


class GroupJournalAdmin(ModelAdmin):
    """"""

    list_display: tuple[str] = (
        "journal_title",
        "journal_description",
        "journal_bio",
        "entry_date",
        "last_edited",
        "journal_mood",
        "private",
    )
    inlines: list[TabularInline] = [GroupOwnershipInline]


class TemplateAdmin(ModelAdmin):
    """"""

    list_display: tuple[str] = ("title", "description", "bio")
    inlines: list[TabularInline] = [OwnershipInline]


class EntriesAdmin(ModelAdmin):
    """"""

    list_display: tuple[str] = ("",)
    inlines: list[TabularInline] = []


class NotificationAdmin(ModelAdmin):
    """"""

    list_display: tuple[str] = ("notification_type", "message", "time_created", "read")
    inlines: list[TabularInline] = [OwnershipInline]


admin.site.register(User, UserAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Journal, JournalAdmin)
admin.site.register(GroupJournal, GroupJournalAdmin)
admin.site.register(Template, TemplateAdmin)
admin.site.register(Notification, NotificationAdmin)
