from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
import calendar
from calendar import HTMLCalendar
from django.contrib.auth.decorators import login_required
from journal.helpers import login_prohibited


@login_prohibited
def home(request) -> HttpResponse:
    """Display the application's start/home screen."""
    return render(request, 'home.html')


@login_required
def calendar_view(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    name = "Journaler"
    month = month.capitalize()
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    cal = HTMLCalendar().formatmonth(year, month_number)
    now = datetime.now()
    current_year = now.year
    current_month = now.month
    return render(
        request,
        template_name='calendar.html',
        context={
            "name": name,
            "year": year,
            "month": month,
            "month_number": month_number,
            "cal": cal,
            "current_year": current_year,
            "current_month": current_month,
        }
    )
