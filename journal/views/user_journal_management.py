from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from journal.models import Journal, Entry, User
from journal.forms import CreateEntryForm, CreateJournalForm, EntryFilterForm, EntrySortForm
from django.contrib import messages
from journal.views.notifications import *
from journal.views.user_management import *
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseRedirect,
    JsonResponse,
    Http404,
)
from django.utils.translation import gettext as _
from django_ckeditor_5.forms import UploadFileForm
from django_ckeditor_5.views import image_verify, handle_uploaded_file, NoImageException
from django.shortcuts import render


@login_required
def create_journal(request: HttpRequest) -> HttpResponseRedirect:
    if request.method == "POST":
        form = CreateJournalForm(request.POST)
        if form.is_valid():

            journal = form.save(commit=False)
            journal.owner = request.user
            journal.save()

            if ActionCooldown.can_perform_action(
                request.user, "create_journal", cooldown_hours=1
            ):
                messages.success(request, "New Journal Created! Points awarded.")
                give_points(request, 20, "New Journal Created.")
            else:
                messages.success(
                    request,
                    "New journal created! However, you must wait before getting points again.",
                )

            create_notification(
                request, f"New journal {journal.title} created!", "info"
            )

            return redirect(reverse("dashboard")) 
    else:
        form = CreateJournalForm()

    return render(request, "create_journal.html", {"form": form})


def create_first_journal(current_user: User) -> None:
    Journal.objects.create(
        title="Welcome To Compact Journals",
        summary="""This is your first Compact Journal!
         With each Compact Journal you can create a daily entry to keep track of your activites, productivity as well as your mood.
         Create as many Journals as you like!
         The Journal Dashboard is where you create your daily entry, edit, delete and store your previous entries (press the button below to access).
        """,
        owner=current_user,
    )


@login_required
def edit_journal(
    request: HttpRequest, journal_id: int
) -> HttpResponseRedirect | HttpResponse:

    try:
        journal_instance = Journal.objects.get(id=journal_id)
    except ObjectDoesNotExist:
        messages.warning(
            request,
            "You have attempted to access an invalid URL, redirected to dashboard",
        )
        return redirect(reverse("dashboard"))

    if request.user != journal_instance.owner:
        messages.warning(
            request,
            "You have attempted to access a journal that is not yours, redirected to dashboard",
        )
        return redirect(reverse("dashboard"))

    if request.method == "POST":
        form = CreateJournalForm(request.POST, instance=journal_instance)
        if form.is_valid():
            form.save()
            create_notification(
                request, f"Journal {journal_instance.title} was edited.", "info"
            )
            return redirect(
                reverse("dashboard")
            )  # Redirect to the dashboard page after saving
    else:
        form = CreateJournalForm(instance=journal_instance)

    context = {
        "form": form,
        "journal": journal_instance,
        "title": "Update Journal",
        "update": True,
    }
    return render(request, "create_journal.html", context)


@login_required
def delete_journal(request: HttpRequest, journal_id: int) -> HttpResponseRedirect:

    try:
        journal_instance = Journal.objects.get(id=journal_id)
    except ObjectDoesNotExist:
        messages.warning(
            request,
            "You have attempted to access an invalid URL, redirected to dashboard",
        )
        return redirect(reverse("dashboard"))

    if request.user != journal_instance.owner:
        messages.warning(
            request,
            "You have attempted to delete a journal that is not yours, redirected to dashboard",
        )
        return redirect(reverse("dashboard"))

    create_notification(request, f"Journal {journal_instance.title} deleted.", "info")

    journal_instance.delete()
    return redirect("dashboard")


@login_required
def all_journals_view(
    request: HttpRequest, user_id: int
) -> HttpResponse | HttpResponseRedirect:
    """Renders a template holding all of the user's journals"""

    try:
        viewing_user = User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        messages.warning(
            request,
            "You have attempted to view a user's journal who doesn't exist, redirected to dashboard",
        )
        return redirect(reverse("dashboard"))

    current_user = request.user
    viewing_user = User.objects.get(id=user_id)
    currently_logged_in = current_user == viewing_user
    journals = viewing_user.journals.all()
    return render(
        request, 
        'my_journals.html',
        {
            'viewing_user': viewing_user,
            'user': request.user,
            'journals': journals,
            "is_logged_in": currently_logged_in
        }
    )


@login_required
def journal_dashboard(
    request: HttpRequest, journal_id: int
) -> HttpResponse | HttpResponseRedirect:
    """Renders a HTML documnet for the journal, holding all its details"""
    current_user = request.user
    today = datetime.now().date()

    try:
        journal_instance = Journal.objects.get(id=journal_id)
    except ObjectDoesNotExist:
        messages.warning(
            request,
            "You have attempted to access an invalid URL, redirected to dashboard",
        )
        return redirect(reverse("dashboard"))

    if request.user != journal_instance.owner:
        messages.warning(
            request,
            "You have attempted to access a journal that is not yours, redirected to dashboard",
        )
        return redirect(reverse("dashboard"))

    journal_entries = journal_instance.entries.all()
    todays_entry = journal_entries.filter(entry_date__date=today)
    return render(
        request,
        "journal_dashboard.html",
        {
            "user": current_user,
            "journal": journal_instance,
            "journal_entries": journal_entries,
            "todays_entry": todays_entry,
        },
    )


@login_required
def view_entry(
    request: HttpRequest, entry_id: int
) -> HttpResponse | HttpResponseRedirect:
    current_user = request.user

    try:
        entry = Entry.objects.get(id=entry_id)
        referer_url = request.META.get(
            "HTTP_REFERER", f"/journal_dashboard/{entry.id}/"
        )
    except ObjectDoesNotExist:
        messages.warning(
            request,
            "You have attempted to access an invalid URL, redirected to dashboard",
        )
        return redirect(reverse("dashboard"))

    return render(
        request,
        "view_entry.html",
        {
            "user": current_user,
            "entry": entry,
            "referer_url": referer_url,
        },
    )


@login_required
def create_entry(
    request: HttpRequest, journal_id: int
) -> HttpResponse | HttpResponseRedirect:

    today = datetime.now().date()
    current_user = request.user

    try:
        journal_instance = Journal.objects.get(id=journal_id)
    except ObjectDoesNotExist:
        messages.warning(
            request,
            "You have attempted to access an invalid URL, redirected to dashboard",
        )
        return redirect(reverse("dashboard"))

    if request.user != journal_instance.owner:
        messages.warning(
            request,
            "You have attempted to access a journal that is not yours, redirected to dashboard",
        )
        return redirect(reverse("dashboard"))

    if Entry.objects.filter(journal=journal_instance, entry_date__date=today).exists():
        messages.warning(
            request,
            "Daily entry already created, edit or delete todays journal. Redirected to dashboard",
        )
        return redirect(reverse("dashboard"))

    if request.method == "POST":
        form = CreateEntryForm(request.POST)
        if form.is_valid():

            entry = form.save(commit=False)
            entry.owner = current_user
            entry.journal = journal_instance
            entry.save()
            entry.journal.last_entry_date = today
            entry.journal.save()

            notif_message = (
                f"New entry {entry.title} created in {entry.journal.title} journal."
            )
            give_points(request, 50, notif_message)
            create_notification(request, notif_message, "info")

            return redirect(f"/journal_dashboard/{journal_instance.id}")
    else:
        form = CreateEntryForm()

    context = {'form': form, 'title': 'Create Entry'}
    return render(request, 'create_entry.html', context)

@login_required
def edit_entry(
    request: HttpRequest, entry_id: int
) -> HttpResponse | HttpResponseRedirect:

    try:
        entry_instance = Entry.objects.get(id=entry_id)
    except ObjectDoesNotExist:
        messages.warning(
            request,
            "You have attempted to access an invalid URL, redirected to dashboard",
        )
        return redirect(reverse("dashboard"))

    if request.user != entry_instance.owner:
        messages.warning(
            request,
            "You have attempted to edit an entry that is not yours, redirected to dashboard",
        )
        return redirect(reverse("dashboard"))

    if request.method == "POST":
        form = CreateEntryForm(request.POST, instance=entry_instance)
        if form.is_valid():
            form.save()
            notif_message = f"Entry {entry_instance.title} edited in {entry_instance.journal.title} journal."
            create_notification(request, notif_message, "info")
            return redirect(f"/journal_dashboard/{entry_instance.journal.id}")
    else:
        form = CreateEntryForm(instance=entry_instance)

    context = {"form": form, "entry": entry_instance, "title": "Update Entry"}
    return render(request, "create_entry.html", context)


@login_required
def delete_entry(request: HttpRequest, entry_id: int) -> HttpResponseRedirect:

    try:
        entry_instance = Entry.objects.get(id=entry_id)
    except ObjectDoesNotExist:
        messages.warning(
            request,
            "You have attempted to access an invalid URL, redirected to dashboard",
        )
        return redirect(reverse("dashboard"))

    if request.user != entry_instance.owner:
        messages.warning(
            request,
            "You have attempted to edit an entry that is not yours, redirected to dashboard",
        )
        return redirect(reverse("dashboard"))

    journal = entry_instance.journal

    yesterday = datetime.now() - timedelta(days=1)
    journal.last_entry_date = yesterday

    journal.save()

    entry_instance.delete()
    return redirect(f"/journal_dashboard/{journal.id}")


@login_required
def view_journal_entries(
    request: HttpRequest, user_id: int, journal_id: int
) -> HttpResponse:

    current_user = get_object_or_404(User, id=user_id)
    current_journal = get_object_or_404(Journal, id=journal_id)
    is_user_logged_in = request.user == current_user

    filter_form = EntryFilterForm(current_user, request.POST or None)
    sort_form = EntrySortForm(request.POST or None)

    if request.method == "POST" and filter_form.is_valid() and sort_form.is_valid():
        journal_entries = filter_form.filter_entries(current_journal)
        sort_order = sort_form.cleaned_data["sort_by_entry_date"]
        journal_entries = journal_entries.order_by(
            "-entry_date" if sort_order == "descending" else "entry_date"
        )
    else:
        journal_entries = current_journal.entries.all()

    if not is_user_logged_in:
        journal_entries = journal_entries.filter(private=False)

    context = {
        'filter_form': filter_form,
        'sort_form': sort_form,
        'journal_entries': journal_entries,
        'journal_param': my_journals_to_journal_param(journal_entries),
        'viewing_user': current_user,
        'user': request.user,
        'journal': current_journal,
        'is_logged_in': is_user_logged_in,
    }

    return render(request, "view_all_journal_entries.html", context)

#returns a string comma seperated list of ID values representing the entries in a journal to be exported
def my_journals_to_journal_param(journal_entries):

    journals = []
    for journal in journal_entries:
        journals.append(f"{journal.id}")
    journal_param = ",".join(journals)
    return journal_param


def custom_upload_file(request: HttpRequest) -> JsonResponse:
    """Allows the upload of images into a CKeditor field"""
    if request.method != "POST":
        raise Http404(_("Page not found."))

    form = UploadFileForm(request.POST, request.FILES)
    try:
        image_verify(request.FILES["upload"])
    except NoImageException as ex:
        return JsonResponse({"error": {"message": f"{ex}"}})

    if form.is_valid():
        url = handle_uploaded_file(request.FILES["upload"])
        return JsonResponse({"url": url})
