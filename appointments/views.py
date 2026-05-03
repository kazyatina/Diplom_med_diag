from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render

from .forms import AppointmentForm
from .models import Appointment


@login_required
def create_appointment(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST, user=request.user)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.save()
            messages.success(request, "Запись на приём успешно создана!")
            return redirect("accounts:profile")
    else:
        service_id = request.GET.get("service")
        initial = {}
        if service_id:
            initial["service"] = service_id
        form = AppointmentForm(initial=initial, user=request.user)
    return render(request, "appointments/create.html", {"form": form})


@login_required
def cancel_appointment(request, appointment_id):
    if request.method != "POST":
        return JsonResponse(
            {"success": False, "error": "Метод не поддерживается"},
            status=405,
        )

    try:
        appointment = Appointment.objects.get(id=appointment_id, user=request.user)
        if appointment.status == "cancelled":
            return JsonResponse({"success": True, "message": "Запись уже отменена"})

        appointment.status = "cancelled"
        appointment.save()
        return JsonResponse({"success": True, "message": "Запись успешно отменена"})
    except Appointment.DoesNotExist:
        return JsonResponse(
            {"success": False, "error": "Запись не найдена"},
            status=404,
        )
