from django.urls import path
from .views import ServiceListView, ServiceDetailView, HomePageView, AppointmentCreateView
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('services/', ServiceListView.as_view(), name='ServiceListView'),
    path('services/<int:pk>/', ServiceDetailView.as_view(), name='ServiceDetailView'),
    path('', HomePageView.as_view(), name='HomePageView'),
    path('agendar-cita/', AppointmentCreateView.as_view(), name='agendar_cita'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    # ...existing code...
] 
