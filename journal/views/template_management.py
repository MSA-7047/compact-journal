from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from django.urls import reverse, reverse_lazy
from journal.models import *
from journal.forms import *

def generate_generic_templates(currentUser):
    html_file_paths = [
        'journal/journal_templates/template1.html',
        'journal/journal_templates/template2.html',
        'journal/journal_templates/template3.html',
        'journal/journal_templates/template4.html',
        'journal/journal_templates/template5.html',
    ]

    for i, html_file_path in enumerate(html_file_paths, start=1):
        with open(html_file_path, 'r') as html_file:
            html_content = html_file.read()

        Template.objects.create(
            title=f"Default Template {i}",
            description=f"Description for Default Template {i}",
            bio=html_content,
            owner=currentUser
        )


@login_required    
def create_template(request):

    current_user = request.user
    form = CreateTemplateForm()
    if (request.method == 'POST'):
        form = CreateTemplateForm(request.POST)
        if (form.is_valid()):
            template = Template.objects.create(
                title = form.cleaned_data.get("title"),
                description = form.cleaned_data.get("description"),
                bio = form.cleaned_data.get("bio"),
                owner = current_user,
            )
            template.save()
            return redirect('/select-template/')
        else:
            return render(request, 'create_template.html', {'form': form})
    else:
        return render(request, 'create_template.html', {'form': form, 'title': "Create Template"})
    

def select_template(request):
    currentUser = request.user
    templates = Template.objects.filter(owner=currentUser)
    return render(request, 'select_template.html', {"templates": templates})

@login_required
def DeleteTemplate(request,templateID):
    template= get_object_or_404(Template, id=templateID)
    template.delete()
    return redirect('select_template')

def create_journal_From_Template(request, templateID):
    current_user = request.user
    template = get_object_or_404(Template, id = templateID)
    journal = Journal.objects.create(
                journal_title = template.title,
                journal_description = template.description,
                journal_bio = template.bio,
                journal_mood = "neutral",
                journal_owner = current_user,
                private = False
            )
    journal.save()
    return redirect("edit_journal", journalID=journal.id)

@login_required
def EditTemplate(request, templateID): 
    template = get_object_or_404(Template, id=templateID)
    if request.method == 'POST':
        form = CreateTemplateForm(request.POST, instance=template)
        if form.is_valid():
            form.save()
            return redirect('select_template')  # Redirect to the detail view of the edited journal
    else:
        form = CreateTemplateForm(instance=template)

    return render(request, 'create_template.html', {'form': form, 'template': template, 'title': "Update Template"})