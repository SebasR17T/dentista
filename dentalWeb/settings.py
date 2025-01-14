# ...existing code...

# Google Calendar Settings
GOOGLE_CALENDAR_ENABLED = True
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'google_calendar.log',
        },
    },
    'loggers': {
        'dentalApp.google_calendar': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        },
    },
}

# ...existing code...
