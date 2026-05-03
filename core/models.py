from django.db import models


class Doctor(models.Model):
    name = models.CharField("ФИО", max_length=200)
    specialty = models.CharField("Специальность", max_length=100)
    is_active = models.BooleanField(default=True)
    photo = models.ImageField("Фото", upload_to="doctors/", blank=True, null=True)
    service = models.ForeignKey(
        "Service",
        on_delete=models.CASCADE,
        related_name="service",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.name} - {self.specialty}"

    class Meta:
        verbose_name = "Доктор"
        verbose_name_plural = "Доктора"


class Service(models.Model):
    title = models.CharField("Название услуги", max_length=200)
    description = models.TextField("Краткое описание", blank=True, null=True)
    full_description = models.TextField("Полное описание", blank=True, null=True)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=0, default=500)
    image = models.ImageField(
        "Изображение", upload_to="services/", blank=True, null=True
    )
    duration = models.IntegerField(default=30)
    created_at = models.DateTimeField(auto_now_add=True)
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="doctor", null=True, blank=True
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"


class ContactInfo(models.Model):
    address = models.TextField("Адрес")
    phone = models.CharField("Телефон", max_length=20)
    email = models.EmailField("Email")
    map_embed = models.TextField("Код карты", blank=True)

    class Meta:
        verbose_name = "Контакты"
        verbose_name_plural = "Контакты"


class ContactMessage(models.Model):
    name = models.CharField("Имя", max_length=100)
    email = models.EmailField("Email", blank=True)
    phone = models.CharField("Телефон", max_length=20)
    message = models.TextField("Сообщение")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    def __str__(self):
        return f"Сообщение от {self.name}"

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
