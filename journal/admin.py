from django.contrib import admin
from .models import Journal

admin.site.register(Journal)
# Register your models here.
#@admin.register(Journal)
#class JournalAdmin(admin.ModelAdmin):
    #list_display = ['journal_title', 'journal_description', 'journal_bio', 'entry_date', 'journal_mood', 'journal_owner']
