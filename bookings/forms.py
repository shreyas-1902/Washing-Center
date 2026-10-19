# bookings/forms.py
from django import forms
from .models import Booking
from django.forms import DateInput, TimeInput

class BookingForm(forms.ModelForm):
    scheduled_date = forms.DateField(widget=DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    scheduled_time = forms.TimeField(widget=TimeInput(attrs={'type': 'time', 'class': 'form-control'}))

    class Meta:
        model = Booking
        fields = ['scheduled_date', 'scheduled_time', 'phone', 'notes']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your phone number'}),
            'notes': forms.Textarea(attrs={'rows':3, 'class': 'form-control'}),
        }

    def clean(self):
        cleaned = super().clean()
        date = cleaned.get('scheduled_date')
        time = cleaned.get('scheduled_time')
        if date and time:
            from datetime import datetime
            dt = datetime.combine(date, time)
            cleaned['scheduled_at'] = dt
        return cleaned
