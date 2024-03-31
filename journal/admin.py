from django.contrib import admin
from .models import Journal, GroupRequest, Entry

admin.site.register(Journal)
admin.site.register(GroupRequest)
admin.site.register(Entry)

# Register your models here.
#@admin.register(Journal)
#class JournalAdmin(admin.ModelAdmin):
    #list_display = ['journal_title', 'journal_description', 'journal_bio', 'entry_date', 'journal_mood', 'journal_owner']
