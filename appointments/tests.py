import json
from datetime import date, time

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from appointments.models import Appointment
from core.models import Doctor, Service


class CancelAppointmentViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        # Создаём Doctor с правильным именем поля
        self.doctor = Doctor.objects.create(
            name="Test Doctor",
            specialty="Therapy",  # исправлено: specialty вместо specialization
        )
        # Создаём Service
        self.service = Service.objects.create(
            title="Test Service",
            description="Test description",
            price=1000,
            duration=30,
        )
        # Используем объекты date и time
        appointment_date = date(2026, 5, 10)
        appointment_time = time(14, 0)

        self.appointment = Appointment.objects.create(
            user=self.user,
            service=self.service,
            doctor=self.doctor,
            date=appointment_date,
            time=appointment_time,
            status="scheduled",
        )
        self.client.login(username="testuser", password="testpass123")

    def test_cancel_appointment_success(self):
        """Тест успешной отмены записи"""
        url = reverse("appointments:cancel_appointment", args=[self.appointment.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data["success"])
        self.assertIn("успешно отменена", response_data["message"])

        # Проверяем, что статус обновился в БД
        updated_appointment = Appointment.objects.get(id=self.appointment.id)
        self.assertEqual(updated_appointment.status, "cancelled")

    def test_cancel_nonexistent_appointment(self):
        """Тест отмены несуществующей записи"""
        url = reverse("appointments:cancel_appointment", args=[999])
        response = self.client.post(url)

        self.assertEqual(response.status_code, 404)
        response_data = json.loads(response.content)
        self.assertFalse(response_data["success"])
        self.assertIn("не найдена", response_data["error"])

    def test_cancel_already_cancelled_appointment(self):
        """Тест отмены уже отменённой записи"""
        # Сначала отменяем запись
        self.appointment.status = "cancelled"
        self.appointment.save()

        url = reverse("appointments:cancel_appointment", args=[self.appointment.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data["success"])
        self.assertIn("уже отменена", response_data["message"])

    def test_cancel_other_user_appointment(self):
        """Тест попытки отменить запись другого пользователя"""
        other_user = User.objects.create_user(
            username="otheruser", password="otherpass123"
        )
        # Создаём doctor для другого пользователя с правильным полем
        other_doctor = Doctor.objects.create(
            name="Other Doctor",
            specialty="Cardiology",  # исправлено: specialty вместо specialization
        )
        # Создаём service для другого пользователя
        other_service = Service.objects.create(
            title="Other Service",
            description="Other description",
            price=1500,
            duration=45,
        )
        other_date = date(2026, 5, 11)
        other_time = time(15, 0)

        other_appointment = Appointment.objects.create(
            user=other_user,
            service=other_service,
            doctor=other_doctor,
            date=other_date,
            time=other_time,
            status="scheduled",
        )

        url = reverse("appointments:cancel_appointment", args=[other_appointment.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, 404)
        response_data = json.loads(response.content)
        self.assertFalse(response_data["success"])
        self.assertIn("не найдена", response_data["error"])

    def test_get_request_not_allowed(self):
        """Тест GET-запроса (должен быть запрещён)"""
        url = reverse("appointments:cancel_appointment", args=[self.appointment.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 405)
        response_data = json.loads(response.content)
        self.assertFalse(response_data["success"])
        self.assertIn("не поддерживается", response_data["error"])
