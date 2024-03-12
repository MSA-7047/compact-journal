from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.views.generic.edit import FormView, UpdateView
from django.urls import reverse, reverse_lazy
from journal.models import *
from journal.forms import *
from journal.helpers import login_prohibited
from django.views.generic import DetailView
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.contrib.messages.views import SuccessMessageMixin

from django.db import transaction
from .models.Notification import Notification




  

