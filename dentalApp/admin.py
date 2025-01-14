from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _
from .models import Service, Appointment, SocialMediaSettings

class MyAdminSite(AdminSite):
    site_header = _('Clínica Dental Administration')
    site_title = _('Clínica Dental Admin')
    index_title = _('Panel de Administración')

admin_site = MyAdminSite(name='myadmin')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'price']
    search_fields = ['name']
    list_filter = ['price']
    ordering = ['name']

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    # La configuración actual es correcta, solo necesitamos que el modelo tenga el campo status
    list_display = ['patient_name', 'service', 'appointment_date', 'appointment_time', 'status', 'created_at']
    list_filter = ['appointment_date', 'service', 'status']
    search_fields = ['patient_name', 'patient_email', 'patient_phone']
    date_hierarchy = 'appointment_date'
    readonly_fields = ['created_at']
    list_editable = ['status']
    fieldsets = (
        ('Información del Paciente', {
            'fields': ('patient_name', 'patient_email', 'patient_phone')
        }),
        ('Detalles de la Cita', {
            'fields': ('service', 'appointment_date', 'appointment_time', 'status')
        }),
        ('Notas', {
            'fields': ('notes',)
        }),
        ('Información del Sistema', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(SocialMediaSettings)
class SocialMediaSettingsAdmin(admin.ModelAdmin):
    list_display = ['whatsapp_number', 'phone_number', 'email', 'get_active_channels']
    fieldsets = (
        ('WhatsApp', {
            'fields': ('whatsapp_number', 'is_whatsapp_active'),
            'classes': ('wide',)
        }),
        ('Teléfono', {
            'fields': ('phone_number', 'is_phone_active'),
            'classes': ('wide',)
        }),
        ('Email', {
            'fields': ('email', 'is_email_active'),
            'classes': ('wide',)
        }),
        ('Redes Sociales', {
            'fields': ('facebook_url', 'is_facebook_active', 'instagram_url', 'is_instagram_active'),
            'classes': ('wide',)
        }),
    )

    def get_active_channels(self, obj):
        active = []
        if obj.is_whatsapp_active:
            active.append('WhatsApp')
        if obj.is_phone_active:
            active.append('Teléfono')
        if obj.is_email_active:
            active.append('Email')
        if obj.is_facebook_active:
            active.append('Facebook')
        if obj.is_instagram_active:
            active.append('Instagram')
        return ', '.join(active)
    get_active_channels.short_description = 'Canales Activos'

    def has_add_permission(self, request):
        return not SocialMediaSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
