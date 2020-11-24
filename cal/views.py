from django.contrib.auth.decorators import login_required
from bootstrap_modal_forms.generic import BSModalCreateView
from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime, timedelta, date
from django.core.mail import EmailMessage
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import *
from .utils import Calendar
from .forms import EventForm, ReminderForm
import calendar


class EventListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'cal/events.html'
    context_object_name = 'events'
    ordering = ['-start_time']
    paginate_by = 5


class EventDetailView(LoginRequiredMixin, DetailView):
    model = Event

    def get_context_data(self, **kwargs):
        context = super(EventDetailView, self).get_context_data(**kwargs)
        self.request.session['id'] = self.object.pk
        return context


class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class CalendarView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'cal/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # use today's date for the calendar
        d = get_date(self.request.GET.get('month', None))
        # instantiate with today's year and date
        cal = Calendar(d.year, d.month)
        # call the formatmonth method with returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context


def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


class EventCreateView(LoginRequiredMixin, CreateView):
    # model = Event
    form_class = EventForm
    template_name = 'cal/event_form.html'

    def form_valid(self, form_class):
        form_class.instance.author = self.request.user
        return super().form_valid(form_class)


class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    form_class = EventForm

    def form_valid(self, form_class):
        form_class.instance.author = self.request.user
        return super().form_valid(form_class)

    def test_func(self):
        event = self.get_object()
        if self.request.user == event.author:
            return True
        return False


class ReminderCreateView(LoginRequiredMixin, CreateView):
    form_class = ReminderForm
    template_name = 'cal/create_reminder.html'

    def form_valid(self, form_class):
        form_class.instance.member = self.request.user
        myevent_id = self.request.session.get('id')
        form_class.instance.event = Event.objects.get(id=myevent_id)
        return super().form_valid(form_class)
    # success_message = 'Success: Your reminder has been created'
    # success_url = reverse_lazy('event-detail')


class UserEventView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'cal/events.html'
    context_object_name = 'events'

    def get_queryset(self):
        qs = super().get_queryset()
        # qs = Announcement.objects.filter(author=self.request.user)
        return qs.filter(author=self.request.user)


def index(request):
    return HttpResponse('Done!')


def send_reminder(request):
    reminders = Reminder.objects.filter(reminder_date=date.today())
    if reminders:
        email_subject = 'You have an upcoming event!'
        for reminder in reminders:
            html_message = render_to_string('cal/reminder_message.html', {'reminder': reminder,})
            # plain_message = strip_tags(html_message)
            to_email = reminder.member.email
            email = EmailMessage(email_subject, html_message, to=[to_email])
            email.content_subtype = 'html'
            email.send()
            Reminder.objects.filter(id=reminder.id).delete()
        messages.success(request, f'Reminder sent to users!')
        return redirect('ngo-about')
    else:
        return redirect('announcements-home')

