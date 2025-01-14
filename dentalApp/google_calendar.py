from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os.path
import pickle
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

SCOPES = ['https://www.googleapis.com/auth/calendar']
CREDENTIALS_FILE = os.path.join(settings.BASE_DIR, 'credentials.json')
TOKEN_FILE = os.path.join(settings.BASE_DIR, 'token.pickle')

def get_google_calendar_service():
    creds = None
    
    # Verificar si existe el archivo credentials.json
    if not os.path.exists(CREDENTIALS_FILE):
        logger.error(f"No se encontró el archivo credentials.json en {CREDENTIALS_FILE}")
        raise FileNotFoundError(
            "No se encontró el archivo credentials.json. Por favor, descárguelo de Google Cloud Console "
            "y colóquelo en la raíz del proyecto."
        )

    try:
        # Intentar cargar credenciales existentes
        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE, 'rb') as token:
                creds = pickle.load(token)
                logger.info("Credenciales cargadas desde token.pickle")

        # Si no hay credenciales válidas, crear nuevas
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                logger.info("Refrescando token expirado")
                creds.refresh(Request())
            else:
                logger.info("Iniciando flujo de autorización")
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_FILE, 
                    SCOPES,
                    redirect_uri='http://localhost:8080/'  # Especificar redirect_uri explícitamente
                )
                creds = flow.run_local_server(
                    port=8080,
                    prompt='consent',
                    access_type='offline'
                )
                logger.info("Nuevas credenciales obtenidas exitosamente")

            # Guardar las credenciales
            with open(TOKEN_FILE, 'wb') as token:
                pickle.dump(creds, token)
                logger.info("Credenciales guardadas en token.pickle")

        service = build('calendar', 'v3', credentials=creds)
        return service

    except Exception as e:
        logger.error(f"Error en la autenticación de Google Calendar: {str(e)}")
        raise

def create_calendar_event(appointment):
    try:
        service = get_google_calendar_service()
        
        # Convertir la fecha y hora a formato ISO
        start_datetime = datetime.combine(
            appointment.appointment_date,
            appointment.appointment_time
        ).isoformat()
        
        end_datetime = (
            datetime.combine(appointment.appointment_date, appointment.appointment_time) +
            timedelta(hours=1)
        ).isoformat()

        event = {
            'summary': f'Cita Dental - {appointment.patient_name}',
            'description': f'Servicio: {appointment.service.name}\n'
                         f'Paciente: {appointment.patient_name}\n'
                         f'Email: {appointment.patient_email}',
            'start': {
                'dateTime': start_datetime,
                'timeZone': 'America/Bogota',
            },
            'end': {
                'dateTime': end_datetime,
                'timeZone': 'America/Bogota',
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 30},
                ],
            },
        }

        event = service.events().insert(calendarId='primary', body=event).execute()
        logger.info(f"Evento creado exitosamente con ID: {event['id']}")
        return event['id']

    except Exception as e:
        logger.error(f"Error al crear evento en Google Calendar: {str(e)}")
        raise
