from django.db import models

# Create your models here.

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.DurationField()
    is_active = models.BooleanField(default=True)
    photo = models.ImageField(upload_to='service_photos/', null=True, blank=True)

    def __str__(self):
        return self.name

class Appointment(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=100)
    patient_email = models.EmailField()
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.patient_name} - {self.service.name} on {self.appointment_date} at {self.appointment_time}"
