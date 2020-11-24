from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm, DateTimeInput, DateInput
from bootstrap_modal_forms.forms import BSModalForm
from .models import Event, Reminder


class EventForm(ModelForm):

    class Meta:
        model = Event
        widgets = {
            'start_time': DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'end_time': DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        fields = ['title', 'description', 'start_time', 'end_time', 'image', 'tag', 'facebookurl']
        labels = {'facebookurl': 'Facebook event link'}

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)


class ReminderForm(ModelForm):
    # member = forms.ModelChoiceField(User.objects)
    # event = forms.ModelChoiceField(Event.objects)

    class Meta:
        model = Reminder
        widgets = {
            'reminder_date': DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }
        fields = ['reminder_date']

        def __init__(self, *args, user, event, **kwargs):
            super(ReminderForm, self).__init__(*args, **kwargs)

            # self.fields['member'].queryset = User.objects.filter(member=user)
            # self.fields['event'].queryset = Event.objects.filter(event=event)
            # input_formats to parse HTML5 datetime-local input to date field
            self.fields['reminder_date'].input_formats = ('%Y-%m-%d',)

