from django.contrib import admin
from .models import Service, Appointment, SocialMediaSettings

# Register your models here.
admin.site.register(Service)
admin.site.register(Appointment)

@admin.register(SocialMediaSettings)
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
