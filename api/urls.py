from django.urls import path
from .views import bbs
from .views import BbDetailView
from .views import comments


urlspatterns = [
    path('bbs/<int:pk>/comments/', comments),     # Список комментариев
    path('bbs/<int:pk>/', BbDetailView.as_view()),  # Сведения о выбранном объявлении
    path('bbs/', bbs),
]