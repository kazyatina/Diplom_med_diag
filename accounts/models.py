from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from appointments.models import Appointment


class UserProfile(models.Model):
    """Профиль пользователя с дополнительной информацией"""

    USER_TYPES = [
        ("patient", "Пациент"),
        ("doctor", "Врач"),
        ("admin_staff", "Административный персонал"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    user_type = models.CharField(
        "Тип пользователя", max_length=20, choices=USER_TYPES, default="patient"
    )
    first_name = (models.CharField("Имя", max_length=100),)
    last_name = (models.CharField("Фамилия", max_length=100),)
    phone = models.CharField("Телефон", max_length=20, blank=True)
    birth_date = models.DateField("Дата рождения", null=True, blank=True)
    address = models.TextField("Адрес", blank=True)
    medical_history = models.TextField(
        "Медицинская история",
        blank=True,
        help_text="Информация о хронических заболеваниях, аллергиях и т.д.",
    )
    emergency_contact = models.CharField(
        "Экстренный контакт",
        max_length=100,
        blank=True,
        help_text="Имя и телефон для экстренных случаев",
    )
    avatar = models.ImageField("Аватар", upload_to="avatars/", null=True, blank=True)
    is_verified = models.BooleanField("Верифицирован", default=False)
    created_at = models.DateTimeField("Создан", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлён", auto_now=True)

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"

    def __str__(self):
        return f"Профиль {self.user.get_full_name() or self.user.username}"

    @property
    def full_name(self):
        """Полное имя пользователя"""
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}"
        return self.user.username

    def get_appointment_count(self):
        """Количество записей пользователя"""

        return Appointment.objects.filter(user=self.user).count()

    def get_upcoming_appointments(self):
        """Ближайшие записи пользователя"""

        return Appointment.objects.filter(
            user=self.user, date__gte=timezone.now().date(), status="scheduled"
        ).order_by("date", "time")


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Создаёт профиль пользователя при создании учётной записи"""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Сохраняет профиль пользователя при сохранении учётной записи"""
    instance.profile.save()
