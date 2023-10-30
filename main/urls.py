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


from django.urls import path

from .views import index, other_page, BBLoginView, profile, BBLogoutView, \
    ChangeUserInfoView, BBPasswordChangeView, RegisterUserView, \
    RegisterDoneView, user_activate, DeleteUserView, BBPasswordResetView, \
    BBPasswordResetDoneView, BBPasswordResetConfirmView, \
    BBPasswordResetCompleteView, by_rubric, detail, profile_bb_detail, \
    profile_bb_add, profile_bb_change, profile_bb_delete


app_name = 'main'
urlpatterns = [
    path('accounts/register/activate/<str:sign>/', user_activate,
                                                   name='register_activate'),  # Страница активации пользователя
    
    path('accounts/register/done/', RegisterDoneView.as_view(),
                                    name='register_done'),   # Сообщение об успешной активации
    
    path('accounts/register/', RegisterUserView.as_view(),name='register'),   # Страница регистрации пользователя
    
    path('accounts/logout/', BBLogoutView.as_view(), name='logout'),   # Страница выхода
    
    path('accounts/password/change/', BBPasswordChangeView.as_view(),
                                      name='password_change'),   #  Страница смены пароля
    
    path('accounts/profile/delete/', DeleteUserView.as_view(),
                                     name='profile_delete'),    # Страница удаления пользователя
    
    path('accounts/profile/change/', ChangeUserInfoView.as_view(),
                                     name='profile_change'),   #  Страница правки основных данных
    
    path('accounts/profile/change/<int:pk>/', profile_bb_change,
                                              name='profile_bb_change'),   #
    
    path('accounts/profile/delete/<int:pk>/', profile_bb_delete,
                                              name='profile_bb_delete'),    #
    
    path('accounts/profile/add/', profile_bb_add, name='profile_bb_add'),   #
    
    path('accounts/profile/<int:pk>/', profile_bb_detail,
                                       name='profile_bb_detail'),   #
    
    path('accounts/profile/', profile, name='profile'),  # Страница пользовательского профиля
    
    path('accounts/password/reset/done/', BBPasswordResetDoneView.as_view(),
                                          name='password_reset_done'),    #
    
    path('accounts/password/reset/', BBPasswordResetView.as_view(),
                                     name='password_reset'),   #
    
    path('accounts/password/confirm/complete/',
                                    BBPasswordResetCompleteView.as_view(),
                                    name='password_reset_complete'),  #
    
    path('accounts/password/confirm/<uidb64>/<token>/',
                                    BBPasswordResetConfirmView.as_view(),
                                    name='password_reset_confirm'),   #
    
    path('accounts/login/', BBLoginView.as_view(), name='login'),  # Страница входа
    
    path('<int:rubric_pk>/<int:pk>/', detail, name='detail'),  #
    
    path('<int:pk>/', by_rubric, name='by_rubric'),   #
    
    path('<str:page>/', other_page, name='other'),  # Вспомогательные страницы  
    
    path('', index, name='index'),   # Главная страница
]
