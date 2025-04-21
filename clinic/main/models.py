from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Doctor(models.Model):
    full_name = models.CharField('Фамилия Имя Отчество', max_length=100)
    specialization = models.CharField('Специализация', max_length=100)

    class Meta:
        verbose_name = 'Врач'
        verbose_name_plural = 'Врачи'

    def __str__(self):
        return f"{self.full_name} ({self.specialization})"

class Patient(models.Model):
    full_name = models.CharField(max_length=100, verbose_name="Фамилия Имя Отчество")

    class Meta:
        verbose_name = 'Пациент'
        verbose_name_plural = 'Пациенты'

    def __str__(self):
        return f"{self.full_name}"

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='Пациент')  # кто записался
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name='Врач')
    date = models.DateField('Дата приёма')
    time = models.TimeField('Начало приёма')  # начало приёма

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
        unique_together = ('doctor', 'date', 'time')  # чтобы не было двойной записи

    def __str__(self):
        return f"{self.patient.full_name} записан к {self.doctor} на {self.date} в {self.time}"