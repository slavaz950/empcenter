from django.apps import AppConfig

"""
# Прописалось по умолчанию
class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

"""
# Целевой вариант
class ApiConfig(AppConfig):
    name = 'api'
    
    
    
