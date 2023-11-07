

from django.apps import AppConfig
from django.dispatch import Signal

from .utilities import send_activation_notification

class MainConfig(AppConfig):
    name = 'main'
    verbose_name = 'Центр занятости'

#user_registered = Signal(providing_args=['instance'])
user_registered = Signal('instance') 

def user_registered_dispatcher(sender, **kwargs):
    send_activation_notification(kwargs['instance'])

user_registered.connect(user_registered_dispatcher)
