from datetime import datetime, time, timedelta
from django.utils import timezone
from rest_framework import serializers, status
from rest_framework.response import Response

from .models import Doctor, Patient, Appointment


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'full_name', 'specialization']


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'full_name']


class AppointmentCreateSerializer(serializers.ModelSerializer):
    doctor_full_name = serializers.CharField(write_only=True)
    patient_full_name = serializers.CharField(write_only=True)

    class Meta:
        model = Appointment
        fields = ['doctor_full_name', 'patient_full_name', 'date', 'time']

    def create(self, validated_data):
        # Получаем или создаем пациента
        patient_full_name = validated_data.pop('patient_full_name')
        patient, _ = Patient.objects.get_or_create(full_name=patient_full_name)

        # Получаем врача (должен существовать)
        doctor_full_name = validated_data.pop('doctor_full_name')
        try:
            doctor = Doctor.objects.get(full_name=doctor_full_name)
        except Doctor.DoesNotExist:
            raise serializers.ValidationError(
                {"error": f"Врач с ФИО '{doctor_full_name}' не найден"}
            )

        return Appointment.objects.create(
            doctor=doctor,
            patient=patient,
            **validated_data
        )

class AppointmentSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True)
    doctor_id = serializers.PrimaryKeyRelatedField(
        queryset=Doctor.objects.all(),
        source='doctor',
        write_only=True
    )
    patient = PatientSerializer(read_only=True)
    patient_id = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.all(),
        source='patient',
        write_only=True
    )

    class Meta:
        model = Appointment
        fields = ['id', 'doctor', 'doctor_id', 'patient', 'patient_id', 'date', 'time']

    def validate(self, data):
        doctor = data['doctor']
        date_val = data['date']
        time_val = data['time']
        now = timezone.now()

        """
        Проверка что дата не в прошлом
        """
        if date_val < now.date():
            raise serializers.ValidationError({
                "date": "Нельзя записаться на прошедшую дату"
            })

        """
        Проверка что не пытаемся записаться "сегодня, но время уже прошло"
        """
        if date_val == now.date() and time_val < now.time():
                raise serializers.ValidationError({
                    "time": "Нельзя записаться на прошедшее время сегодня"
                })

        """
        Проверка рабочего времени (пн-пт 9:00-18:00)
        """
        if date_val.weekday() >= 5:  # суббота или воскресенье
            raise serializers.ValidationError({
                "date": "Поликлиника не работает в выходные дни"
            })
        if time_val < time(9, 0) or time_val > time(17, 0):
            raise serializers.ValidationError({
                "time": "Запись возможна только с 9:00 до 18:00"
            })

        """
        Проверка занятости даты и времени у врача
        """
        if Appointment.objects.filter(
                doctor=doctor,
                date=date_val,
                time=time_val
        ).exists():
            raise serializers.ValidationError({
                "time": "Это время уже занято"
            })

        """
        Проверка пересечений временных интервалов
        """
        new_start = datetime.combine(date_val, time_val)
        new_end = new_start + timezone.timedelta(hours=1)
        # Находим все записи врача на эту дату
        overlapping = Appointment.objects.filter(
            doctor=doctor,
            date=date_val,
        )
        # Проверяем каждую запись на пересечение
        for appointment in overlapping:
            existing_start = datetime.combine(date_val, appointment.time)
            existing_end = existing_start + timezone.timedelta(hours=1)
            # Проверяем пересечение интервалов
            if (new_start < existing_end) and (new_end > existing_start):
                raise serializers.ValidationError({
                    "time": f"Время пересекается с существующей записью "
                            f"({appointment.time.strftime('%H:%M')}-"
                            f"{(existing_start + timezone.timedelta(hours=1)).time().strftime('%H:%M')})"
                })

        return data