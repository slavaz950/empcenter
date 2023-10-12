# Контроллеры
from typing import Any
from django.db import models
from django.shortcuts import render
from django.http import HttpResponse,Http404 #
from django.template import TemplateDoesNotExist #
from django.template.loader import get_template #
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from main.models import AdvUser
from main.forms import ChangeUserInfoForm
from django.contrib.auth.views import PasswordChangeView
from django.views.generic.edit import CreateView
from main.forms import RegisterUserForm
from django.views.generic.base import TemplateView
from django.core.signing import BadSignature
from .utilities import signer
from django.views.generic.edit import DeleteView
from django.contrib.auth import logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import SubRubric, Bb
from .forms import SearchForm

# Контроллер-функция для рубрик (Пустой)
def by_rubric(request, pk):
    rubric = get_object_or_404(SubRubric, pk=pk)
    bbs = Bb.objects.filter(is_active=True, rubric=pk)
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        q = Q(title__icontains=keyword) | Q(content__icontains=keyword)
        bbs = bbs.filter(q)
    else:
        keyword = ''
    
    form = SearchForm(initial={'keyword': keyword})
    paginator = Paginator(bbs, 2)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {'rubric': rubric, 'page': page, 'bbs': page.object_list, 'form': form}
    return render(request, 'main/by_rubric.html', context)
        
   

# Контроллер для удаления пользователя
class DeleteUserView(LoginRequiredMixin,DeleteView):
    model = AdvUser
    template_name = 'main/delete_user.html'
    success_url = reverse_lazy('main:index')
    
    def setup(self,request,*args,**kwargs):
        self.user_id = request.user.pk
        return super().setup(request,*args,**kwargs)
    
    def post(self,request,*args,**kwargs):
        logout(request)
        messages.add_message(request,messages.SUCCESS,'Пользователь удалён')
        return super().post(request,*args,**kwargs)
    
    def get_object(self,queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)



def user_activate(request, sign):  # Контроллер для активации пользователя
        try:
            username = signer.unsign(sign)
        except BadSignature:
            return render(request, 'main/bad_signature.html')
        user = get_object_or_404(AdvUser, username=username)
        if user.is_activated:
            template = 'main/user_is_activated.html'
        else:
            template = 'main/activation_done.html'
            user.is_active = True
            user.is_activated = True
            user.save()
        return render(request, template)


@login_required # Декоратор который проверяет залогинился ли пользователь
def profile(request):  # Контроллер страницы пользовательского профиля
        return render(request, 'main/profile.html') 
    
    # Контроллер регистрирующий пользователя
class RegisterUserView(CreateView):
    model = AdvUser
    template_name = 'main/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('main:register_done') # В случае удачи переходим на страницу .....

# Контроллер выводящий сообщение об успешной регистрации
class RegisterDoneView(TemplateView):
    template_name = 'main/register_done.html'

# Контроллер класса  изменяющий пароль пользователя
class BBPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'main/password_change.html'
    success_url = reverse_lazy('main:profile')
    success_message = 'Пароль пользователя изменён'
    
# Контроллер класса "Входа"   #########
class BBLoginView(LoginView):
    template_name = 'main/login.html' 
    
# Контроллер класса "Выхода" ################
class BBLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'main/logout.html'  


# Контроллер класса изменяющий данные пользователя
class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AdvUser
    template_name = 'main/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_message = 'Данные пользователя изменены'
    success_url = reverse_lazy('main:profile')  #

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)
    
    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)
    
    
    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class BBLoginView(LoginView): # Класс для реализации контроллера страницы входа
    template_name = 'main/login.html'


class BBLogoutView(LoginRequiredMixin, LogoutView): # Класс для реализации контроллера страницы выхода
        template_name = 'main/logout.html'
    

def index(request):  # Контроллер для Главной страницы
    return render(request, 'main/index.html')

def other_page(request, page):  # Контроллер для вспомагательных страниц
    try:
 # Имя выводимой страницы получаем из параметра page, добавляем к нему путь и расширение
 # получив тем самым полный путь к нужному шаблону и пытаемся загрузить его вызвав get_template
 # Если загрузка прошла успешно, то формируем на основе этого шаблона страницу.
 # Если же шаблон загрузить не удалось получаем исключение TemplateDoesNotExist перехватываем
 # это исключение и возбуждаем другое исключение, которое приведёт к отправке страницы
 # с сообщение об ошибке 404 (запрошенная страница не существует).       
        template = get_template('main/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request)) 



# Веб-страница сведений о выбранном объявлении
def detail(request, rubric_pk, pk):
    bb = get_object_or_404(Bb, pk=pk)
    ais = bb.additionalimage_set.all()
    context = {'bb': bb, 'ais' : ais}
    return render(request, 'main/detail.html', context)
# Помимо самой публикации, которую мы помещаем в переменную bb контекста шаблона, также готовим перечень
# связанных с ним дополнительных иллюстраций, записав его в переменную ais

     

# Create your views here.
#
#
