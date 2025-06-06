# Django-проект: Запись к врачу

Проект позволяет пользователям записываться к врачу, а администраторам — управлять приёмами через Django-админку.

---

## Возможности

- Просмотр списка врачей (ФИО, специализация)
- Запись к врачу с учётом времени и занятости
- Просмотр списка своих записей
- Административная панель для управления:
  - Врачами
  - Пользователями
  - Записями на приём

---

## Правила

- Приём длится **ровно 1 час**
- Время работы поликлиники: **Пн–Пт, 09:00–18:00**
- Нельзя записаться:
  - В нерабочее время
  - Если у врача уже есть приём на это время

---

## Postman коллекция

Файл коллекции: postman_collection.json
Импортируйте его в Postman, чтобы получить готовые запросы:
- GET /doctors
- GET /appointments
- GET /appointments/by_patient/?patient_id=...
- POST /appointments\
- GET /patients
  
Формат POST-запроса:
```bash
{
  "doctor_id": 1,
  "patient_id": "1",
  "date": "2025-04-21",
  "time": "9:00:00"
}
```

## Установка и запуск

### 1. Клонировать проект

```bash
git clone https://github.com/1chaayy/web-clinic.git
cd web-clinic
```

### 2. Docker
```bash
docker-compose up --build
```

### 3. Создаем суперпользователя
```bash
docker exec -it web-clinic-web-1 python clinic/manage.py createsuperuser
```
Введите:
- Имя пользователя
- Email (по желанию)
- Пароль


## Логин администратора
####  Зайти в админку: http://localhost:8000/admin/ или http://localhost:8000/
Логин и пароль те, что ты вводил при создании суперпользователя
