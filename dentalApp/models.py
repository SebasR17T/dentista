from django.db import models

# Create your models here.

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=166)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.DurationField()
    is_active = models.BooleanField(default=True)
    photo = models.ImageField(upload_to='media/service_photos/', null=True, blank=True)

    def __str__(self):
        return self.name

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
        ('completada', 'Completada'),
    ]
    
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=100)
    patient_email = models.EmailField()
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pendiente',
        verbose_name='Estado'
    )
    google_calendar_event_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.patient_name} - {self.service.name} on {self.appointment_date} at {self.appointment_time}"

class SocialMediaSettings(models.Model):
    whatsapp_number = models.CharField(max_length=20, help_text="Formato: 573202274345")
    phone_number = models.CharField(max_length=20, help_text="Formato: +573202274345")
    email = models.EmailField()
    facebook_url = models.URLField(verbose_name="URL de Facebook")
    instagram_url = models.URLField(verbose_name="URL de Instagram")
    is_whatsapp_active = models.BooleanField(default=True)
    is_phone_active = models.BooleanField(default=True)
    is_email_active = models.BooleanField(default=True)
    is_facebook_active = models.BooleanField(default=True)
    is_instagram_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Configuración de Redes Sociales"
        verbose_name_plural = "Configuración de Redes Sociales"

    def __str__(self):
        return "Configuración de Redes Sociales"
