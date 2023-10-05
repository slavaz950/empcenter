"""empcenter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


"""  Маршруты  уровня приложения  """

from . import views
from main.views import other_page
from django.urls import path
from main.views import index
from main.views import BBLoginView
from main.views import profile
from main.views import BBLogoutView
from main.views import ChangeUserInfoView
from main.views import BBPasswordChangeView
from main.views import RegisterUserView, RegisterDoneView
from .views import user_activate
from .views import DeleteUserView
#from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetView



app_name = 'main'
urlpatterns = [
    path('accounts/register/activate/<str:sign>', user_activate, name='register_activate'),
    path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('accounts/logout/', BBLogoutView.as_view(), name='logout'),
    path('accounts/password/change/', BBPasswordChangeView.as_view(), name='password_change'),
    path('accounts/profile/delete/', DeleteUserView.as_view(), name='profile_delete'),
    path('accounts/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    path('accounts/profile/',profile, name='profile'),
    path('accounts/login/', BBLoginView.as_view(), name='login'), 
    path('<str:page>/', other_page, name='other'), 
    path('', index, name='index'),
    
  
     
     
]

