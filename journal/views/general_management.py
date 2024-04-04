from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from datetime import datetime
import calendar
from calendar import HTMLCalendar
from django.contrib.auth.decorators import login_required
from journal.helpers import login_prohibited


@login_prohibited
def home(request: HttpRequest) -> HttpResponse:
    """Display the application's start/home screen."""
    return render(request, 'home.html')

