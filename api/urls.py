from django.urls import path
from .views import bbs, BbDetailView, comments

urlpatterns = [
    path('bbs/<int:pk>/comments/', comments),     # Список комментариев
    path('bbs/<int:pk>/', BbDetailView.as_view()),  # Сведения о выбранной публикации
    path('bbs/', bbs),  # Вывод списка публикаций
]