from django.http import HttpResponse
from django.shortcuts import render
from journal.helpers import login_prohibited


@login_prohibited
def home(request) -> HttpResponse:
    """Display the application's start/home screen."""
    return render(request, 'home.html')
