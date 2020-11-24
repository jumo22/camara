from django.contrib.auth.models import User
from cal.models import Reminder, Event
from datetime import date
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def send_reminder():
    reminders = Reminder.objects.filter(reminder_date=date.today())
    if reminders:
        email_subject = 'You have an upcoming event!'
        for reminder in reminders:
            html_message = render_to_string('cal/reminder_message.html', {'reminder': reminder,})
            to_email = reminder.member.email
            email = EmailMessage(email_subject, html_message, to=[to_email])
            email.content_subtype = 'html'
            email.send()
            # Reminder.objects.filter(id=reminder.id).delete()
    else:
        pass
