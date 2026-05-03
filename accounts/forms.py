from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import UserProfile


class CustomUserCreationForm(UserCreationForm):
    """Форма регистрации с дополнительными полями"""

    first_name = (forms.CharField(label="Имя", max_length=100),)
    last_name = (forms.CharField(label="Фамилия", max_length=100),)
    phone = forms.CharField(max_length=20, required=False, label="Телефон")
    birth_date = forms.DateField(
        required=False,
        label="Дата рождения",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 3}), required=False, label="Адрес"
    )

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "birth_date",
            "address",
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Сохраняем дополнительные данные в профиль
            profile = user.profile
            profile.phone = self.cleaned_data["phone"]
            profile.birth_date = self.cleaned_data["birth_date"]
            profile.address = self.cleaned_data["address"]
            profile.save()
        return user


class ProfileUpdateForm(forms.ModelForm):
    """Форма обновления профиля"""

    class Meta:
        model = UserProfile
        fields = [
            "phone",
            "birth_date",
            "address",
            "medical_history",
            "emergency_contact",
            "avatar",
        ]
        widgets = {
            "first_name": forms.CharField(max_length=100),
            "last_name": forms.CharField(max_length=100),
            "birth_date": forms.DateInput(attrs={"type": "date"}),
            "medical_history": forms.Textarea(attrs={"rows": 4}),
            "emergency_contact": forms.TextInput(
                attrs={"placeholder": "Имя и телефон"}
            ),
        }
