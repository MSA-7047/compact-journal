from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from journal.helpers import login_prohibited


@login_prohibited
def home(request: HttpRequest) -> HttpResponse:
    """Display the application's start/home screen."""
    return render(request, 'home.html')

