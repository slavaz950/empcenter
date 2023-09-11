from django.apps import AppConfig

#from django.conf import settings #

from django.dispatch import Signal
from .utilities import send_activation_notification

#

class MainConfig(AppConfig):
    #default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
verbose_name = 'Центр занятости'

# Объявляем сигнал user_registered и привязываем к нему обработчик
#sender = settings.AUTH_USER_MODEL
#user_registered = Signal(providing_args=['instance']) # 
user_registered = Signal('instance') 


def user_registered_dispatcher(sender, **kwargs):
    send_activation_notification(kwargs['instance'])

    user_registered.connect(user_registered_dispatcher)#
# user_registered.connect(sender='')