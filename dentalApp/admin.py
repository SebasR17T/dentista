from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _
from .models import Service, Appointment, SocialMediaSettings

# Customizing the AdminSite
class MyAdminSite(AdminSite):
    site_header = _('Dental Web Administration')
    site_title = _('Dental Web Admin')
    index_title = _('Welcome to Dental Web Admin')

admin_site = MyAdminSite(name='myadmin')

# Register your models here.
admin_site.register(Service)
admin_site.register(Appointment)

@admin.register(SocialMediaSettings, site=admin_site)
class SocialMediaSettingsAdmin(admin.ModelAdmin):
    list_display = ['whatsapp_number', 'phone_number', 'email']
    fieldsets = (
        ('WhatsApp', {
            'fields': ('whatsapp_number', 'is_whatsapp_active'),
        }),
        ('Teléfono', {
            'fields': ('phone_number', 'is_phone_active'),
        }),
        ('Email', {
            'fields': ('email', 'is_email_active'),
        }),
        ('Redes Sociales', {
            'fields': ('facebook_url', 'is_facebook_active', 'instagram_url', 'is_instagram_active'),
        }),
    )

    def has_add_permission(self, request):
        # Limitar a una sola instancia
        return not SocialMediaSettings.objects.exists()
