# forms.py

from django import forms
from django.contrib.auth.models import User
from .models import Appointment

class AppointmentAdminForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        def user_label(obj):
            if obj.first_name and obj.last_name:
                return f"{obj.last_name} {obj.first_name}"
            return obj.username

        self.fields['patient'].label_from_instance = user_label
