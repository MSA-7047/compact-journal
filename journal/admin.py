from django.contrib.admin import TabularInline, ModelAdmin
from django.contrib import admin
from django.db.models import Model
from .models import (
    FriendRequest,
    Group,
    GroupRequest,
    GroupMembership,
    User,
    Journal,
    Template,
    Notification,
    UserMessage,
    GroupEntry,
    Entry,
    Points,
    Level,
    ActionCooldown,
)


class GroupMembershpInline(TabularInline):
    model = GroupMembership
    extra = 1


class FriendRequestAdmin(ModelAdmin):
    list_display = (
        "recipient",
        "sender",
        "creation_date",
        "status",
        "is_accepted",
    )
    inlines = []


class GroupAdmin(ModelAdmin):
    list_display = (
        "group_id",
        "name",
    )
    inlines = [GroupMembershpInline]


class GroupRequestAdmin(ModelAdmin):
    list_display = (
        "recipient",
        "sender",
        "group",
        "creation_date",
        "status",
        "is_accepted",
    )
    inlines = []


class UserAdmin(ModelAdmin):
    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "friends",
        "dob",
        "bio",
        "groups",
        "location",
        "nationality",
        "date_joined",
    )
    inlines = [GroupMembershpInline]


class JournalAdmin(ModelAdmin):
    list_display = (
        "title",
        "summary",
        "entry_date",
        "private",
        "owner",
    )
    inlines = []


class TemplateAdmin(ModelAdmin):
    list_display = (
        "title",
        "description",
        "bio",
        "owner",
    )
    inlines = []


class NotificationAdmin(ModelAdmin):
    list_display = (
        "notification_type",
        "message",
        "time_created",
        "is_read",
        "user",
    )
    inlines = []


class UserMessageAdmin(ModelAdmin):
    list_display = (
        "user",
        "message",
        "read",
    )
    inlines = []


class GroupEntryAdmin(ModelAdmin):
    list_display = (
        "title",
        "summary",
        "content",
        "entry_date",
        "last_edited",
        "MOOD_OPTIONS",
        "mood",
        "last_edited_by",
        "owner",
    )
    inlines = []


class EntryAdmin(ModelAdmin):
    list_display = (
        "title",
        "summary",
        "content",
        "entry_date",
        "last_edited",
        "MOOD_OPTIONS",
        "mood",
        "last_edited",
        "owner",
        "private",
        "journal",
    )
    inlines = []


class PointsAdmin(ModelAdmin):
    list_display = (
        "user",
        "points",
        "description",
    )
    inlines = []


class LevelAdmin(ModelAdmin):
    list_display = (
        "user",
        "points",
        "current_level",
    )
    inlines = []


class CooldownAdmin(ModelAdmin):
    list_display = (
        "user",
        "action_type",
        "last_performed",
    )
    inlines = []


admin.site.register(FriendRequest, FriendRequestAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(GroupRequest, GroupRequestAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Journal, JournalAdmin)
admin.site.register(Template, TemplateAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(UserMessage, UserMessageAdmin)
admin.site.register(GroupEntry, GroupEntryAdmin)
admin.site.register(Entry, EntryAdmin)
admin.site.register(Points, PointsAdmin)
admin.site.register(Level, LevelAdmin)
admin.site.register(ActionCooldown, CooldownAdmin)
