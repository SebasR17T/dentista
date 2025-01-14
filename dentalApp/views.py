from django.views.generic import TemplateView, ListView, DetailView
from django.shortcuts import render, redirect
from .models import Service, Appointment, SocialMediaSettings
from .forms import AppointmentForm
import datetime
from django.contrib import messages
from django.utils import timezone
from .google_calendar import create_calendar_event

class BaseContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['social_media'] = SocialMediaSettings.objects.first()
        return context

class HomePageView(BaseContextMixin, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.filter(is_active=True)
        return context

class ServiceListView(BaseContextMixin, ListView):
    model = Service
    template_name = 'dentalApp/service_list.html'
    context_object_name = 'services'

class ServiceDetailView(BaseContextMixin, DetailView):
    model = Service
    template_name = 'dentalApp/service_detail.html'
    context_object_name = 'service'

class AppointmentCreateView(BaseContextMixin, TemplateView):
    template_name = 'dentalApp/appointment_form.html'

    def get(self, request, *args, **kwargs):
        form = AppointmentForm()    
        return self.render_to_response({'form': form})

    def post(self, request, *args, **kwargs):
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment_date = form.cleaned_data['appointment_date']
            appointment_time = form.cleaned_data['appointment_time']
            appointment_datetime = timezone.datetime.combine(appointment_date, appointment_time)
            start_time = appointment_datetime
            end_time = appointment_datetime + timezone.timedelta(hours=1)
            appointments = Appointment.objects.filter(appointment_date__range=(start_time, end_time))

            if appointments.count() >= 6:
                messages.error(request, 'No hay citas disponibles para esta fecha y hora. Por favor, elija otra fecha u hora.')
                return self.render_to_response({'form': form})

            # Guardar la cita
            appointment = form.save()
            
            try:
                # Crear evento en Google Calendar
                event_id = create_calendar_event(appointment)
                appointment.google_calendar_event_id = event_id
                appointment.save()
                messages.success(request, 'Cita agendada con éxito y agregada a Google Calendar.')
            except Exception as e:
                messages.warning(request, 'Cita agendada con éxito, pero hubo un problema al agregarla a Google Calendar.')
            
            return redirect('HomePageView')

        return self.render_to_response({'form': form})

def about(request):
    return render(request, 'dentalApp/about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        # Here you can add logic to handle the form submission
        # For example, send an email or save to database
        return render(request, 'dentalApp/contact.html', {'success': True})
    return render(request, 'dentalApp/contact.html')
