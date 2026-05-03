from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Создаёт суперпользователя с предустановленными параметрами"

    def handle(self, *args, **options):
        username = getattr(settings, "DEFAULT_SUPERUSER_USERNAME", "admin")
        email = getattr(settings, "DEFAULT_SUPERUSER_EMAIL", "admin@example.com")
        password = getattr(settings, "DEFAULT_SUPERUSER_PASSWORD", "admin123")

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(
                    f'Суперпользователь с именем "{username}" уже существует.'
                )
            )
            return

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(
            self.style.SUCCESS(f'Суперпользователь "{username}" успешно создан!')
        )
