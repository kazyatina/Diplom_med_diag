from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import ContactForm
from .models import ContactInfo, Doctor, Service


def home(request):
    services = Service.objects.all()[:3]  # первые 3 услуги
    contact_info = ContactInfo.objects.first()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Сообщение отправлено!")
            return redirect("core:home")
    else:
        form = ContactForm()
    return render(
        request,
        "core/home.html",
        {"services": services, "contact_info": contact_info, "form": form},
    )


def about(request):
    doctors = Doctor.objects.all()
    return render(request, "core/about.html", {"doctors": doctors})


def services(request):
    services = Service.objects.all()
    return render(request, "core/services.html", {"services": services})


def contacts(request):
    contact_info = ContactInfo.objects.first()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Сообщение отправлено!")
            return redirect("core:contacts")
    else:
        form = ContactForm()
    return render(
        request, "core/contacts.html", {"contact_info": contact_info, "form": form}
    )
