from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from core.models import Doctor, Service

User = get_user_model()


class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, null=False, default=1
    )
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=False, default=1)
    date = models.DateField("Дата приёма")
    time = models.TimeField("Время приёма")
    notes = models.TextField("Примечания", blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("scheduled", "Запланировано"),
            ("completed", "Завершено"),
            ("cancelled", "Отменено"),
        ],
        default="scheduled",
    )
    created_at = models.DateTimeField("Создано", auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.service.title}"

    class Meta:
        verbose_name = "Запись на прием"
        verbose_name_plural = "Записи на прием"

    def save(self, *args, **kwargs):
        # Если статус не «Отменено», проверяем дату и время
        if self.status != "cancelled":
            # Объединяем дату и время в один объект datetime
            appointment_datetime = timezone.make_aware(
                timezone.datetime.combine(self.date, self.time)
            )
            now = timezone.now()

            if appointment_datetime < now:
                self.status = "completed"
            else:
                self.status = "scheduled"

        super().save(*args, **kwargs)
