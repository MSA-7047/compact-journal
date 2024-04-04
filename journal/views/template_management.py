from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from journal.models import Journal, Template, Entry
from journal.forms import CreateTemplateForm
from journal.views.notifications import create_notification
from journal.models.Cooldown import ActionCooldown
from journal.views.user_management import give_points
from django.contrib import messages

#creates 5 templates that are generated everytime a user signs up
def generate_generic_templates(currentUser):
    html_file_paths = [
        'journal/journal_templates/template1.html',
        'journal/journal_templates/template2.html',
        'journal/journal_templates/template3.html',
        'journal/journal_templates/template4.html',
        'journal/journal_templates/template5.html',
    ]
    template_titles = [
        'General Wellbeing Template',
        'Study Plan Template',
        'Gym Tracking Template',
        'Another Template',
        'Last Template',
    ]
    template_summaries = [
        'This template is a general entry to track your wellbeing today',
        'Use this template to keep track of your daily study plans and revision goals',
        'Use this template to keep track of workouts and progress in the gym',
        'to be decided',
        'to be decided',
    ]

    for i, html_file_path in enumerate(html_file_paths, start=1):
        with open(html_file_path, 'r') as html_file:
            html_content = html_file.read()

        Template.objects.create(
            title= template_titles[i - 1],
            description = template_summaries[i - 1],
            bio = html_content,
            owner = currentUser
        )


@login_required    
def create_template(request, journal_id):
    current_user = request.user
    form = CreateTemplateForm()

    if request.method == 'POST':
        form = CreateTemplateForm(request.POST)
        if form.is_valid():
            template = form.save(commit=False)
            template.owner = current_user
            template.save()

            action_allowed = ActionCooldown.can_perform_action(request.user, 'create_template', cooldown_hours=1)
            if action_allowed:
                messages.success(request, "New Custom Template Created! Points awarded.")
                give_points(request, 20, "New Custom Template Created.")
            else:
                messages.success(request, "New custom template created! However, you must wait before getting points again.")
            
            notif_message = f"New custom template {template.title} created!"
            create_notification(request, notif_message, "info")

            return redirect(f'/select_template/{journal_id}')

    return render(request, 'create_template.html', {'form': form, 'title': "Create Template"})
    
@login_required
def select_template(request, journal_id):
    currentUser = request.user
    journal = Journal.objects.get(id = journal_id)
    templates = Template.objects.filter(owner=currentUser)
    return render(request, 'select_template.html', {"templates": templates, "journal":journal})

@login_required
def DeleteTemplate(request,template_id,journal_id):
    template= get_object_or_404(Template, id=template_id)
    create_notification(request, f"The template {template.title} has been deleted.", "info")
    template.delete()
    return redirect(f'/select_template/{journal_id}')

@login_required
def create_journal_From_Template(request, template_id, journal_id):
    current_user = request.user
    template = get_object_or_404(Template, id = template_id)
    journal = Journal.objects.get(id=journal_id)
    entry = Entry.objects.create(
                title = template.title,
                summary = template.description,
                content = template.bio,
                mood = "neutral",
                owner = current_user,
                journal = journal,
                private = False
            )
    entry.save()

    notif_message = f"New entry {entry.title} created in {journal.title} journal."
    give_points(request, 50, notif_message)
    create_notification(request, notif_message, "info")

    return redirect("edit_entry", entry_id=entry.id)

@login_required
def EditTemplate(request, template_id, journal_id): 
    template = get_object_or_404(Template, id=template_id)
    if request.method == 'POST':
        form = CreateTemplateForm(request.POST, instance=template)
        if form.is_valid():
            form.save()

            notif_message = f"The template {template.title} has been edited."
            create_notification(request, notif_message, "info")

            return redirect(f'/select_template/{journal_id}')  # Redirect to the detail view of the edited journal
    else:
        form = CreateTemplateForm(instance=template)

    return render(request, 'create_template.html', {'form': form, 'template': template, 'title': "Edit Template"})

