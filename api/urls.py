"""

from django.urls import path
from .views import bbs, BbDetailView, comments
#from .views import BbDetailView
#from .views import comments


urlspatterns = [
    path('bbs/<int:pk>/comments/', comments),     # Список комментариев
    path('bbs/<int:pk>/', BbDetailView.as_view()),  # Сведения о выбранном объявлении
    path('bbs/', bbs),
]
"""

## именно в этом блоке нестыковка была
from django.urls import path

from .views import bbs, BbDetailView, comments

urlpatterns = [
    path('bbs/<int:pk>/comments/', comments),
    path('bbs/<int:pk>/', BbDetailView.as_view()),
    path('bbs/', bbs),
]