from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.shortcuts import redirect, render

from appointments.models import Appointment

from .forms import CustomUserCreationForm, ProfileUpdateForm
from .models import UserProfile


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, "Регистрация прошла успешно!")
                return redirect("accounts:profile")
            except Exception as e:
                messages.error(request, f"Ошибка при сохранении пользователя: {e}")
                print(f"Ошибка сохранения пользователя: {e}")  # Логирование ошибки
        else:
            # Показываем ошибки формы пользователю
            messages.error(request, "Пожалуйста, исправьте ошибки в форме.")
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("accounts:profile")
    else:
        form = AuthenticationForm()
    return render(request, "accounts/login.html", {"form": form})


@login_required
def profile(request):
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль успешно обновлён!")
            return redirect("accounts:profile")
    else:
        form = ProfileUpdateForm(instance=profile)
    appointments = profile.get_upcoming_appointments()
    context = {
        "profile": profile,
        "form": form,
        "appointments": appointments,
    }
    return render(request, "accounts/profile.html", context)


def user_logout(request):
    """Представление для выхода пользователя из системы"""
    logout(request)
    messages.info(request, "Вы успешно вышли из системы.")
    return redirect("core:home")  # перенаправляем на главную страницу


@login_required
def update_avatar(request):
    if request.method != "POST":
        return JsonResponse(
            {"success": False, "error": "Неверный метод запроса"}, status=405
        )

    if not request.FILES.get("avatar"):
        return JsonResponse({"success": False, "error": "Файл не загружен"}, status=400)

    # Получаем или создаём профиль
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)

    avatar_file = request.FILES["avatar"]

    # Валидация изображения
    allowed_types = ["image/jpeg", "image/png", "image/jpg"]
    if avatar_file.content_type not in allowed_types:
        return JsonResponse(
            {"success": False, "error": "Допустимы только файлы JPG/PNG"}, status=400
        )

    # Ограничение размера (2 МБ)
    if avatar_file.size > 2 * 1024 * 1024:
        return JsonResponse(
            {"success": False, "error": "Файл слишком большой (максимум 2 МБ)"},
            status=400,
        )

    try:
        # Удаляем старый аватар, если он есть
        if profile.avatar and profile.avatar.name:
            if default_storage.exists(profile.avatar.name):
                default_storage.delete(profile.avatar.name)

        # Сохраняем новый аватар
        filename = default_storage.save(
            f"avatars/{request.user.id}_{avatar_file.name}", avatar_file
        )
        profile.avatar.name = filename
        profile.save()

        return JsonResponse(
            {
                "success": True,
                "avatar_url": request.build_absolute_uri(
                    f"{settings.MEDIA_URL}{profile.avatar.name}"
                ),
            }
        )
    except Exception as e:
        print(f"Ошибка сохранения аватара: {e}")  # Лог в консоль сервера
        return JsonResponse(
            {"success": False, "error": f"Ошибка при сохранении: {str(e)}"}, status=500
        )


@login_required
def get_medical_history(request):
    # Получаем записи пользователя (прошедшие и будущие)
    records = Appointment.objects.filter(user=request.user).order_by(
        "-date"
    )  # сортировка по дате (новые сверху)

    data = []
    for record in records:
        data.append(
            {
                "date": record.date.strftime("%d.%m.%Y %H:%M"),
                "service": record.service.title if record.service else "Не указано",
                "doctor": f"{record.doctor.name}",
            }
        )

    return JsonResponse({"records": data})
