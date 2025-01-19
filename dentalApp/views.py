from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import Service, Appointment, SocialMediaSettings
from .forms import AppointmentForm
import datetime
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta

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

class AppointmentCreateView(BaseContextMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'dentalApp/appointment_form.html'
    success_url = reverse_lazy('lista_citas')

    def form_valid(self, form):
        messages.success(self.request, 'Cita agendada exitosamente.')
        return super().form_valid(form)

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
