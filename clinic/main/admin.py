from django.contrib import admin

from .forms import AppointmentAdminForm
from .models import Appointment, Doctor, Patient


# Register your models here.
class AppointmentAdmin(admin.ModelAdmin):
    form = AppointmentAdminForm

admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Patient)

# Inline для отображения записей прямо на странице врача
class AppointmentInline(admin.StackedInline):
    model = Appointment
    extra = 0  # не показывать пустые формы

# Настройка админки врача
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    inlines = [AppointmentInline]

