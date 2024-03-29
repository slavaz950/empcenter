from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404 #  HttpResponse позволяет отправить текстовое содержимое
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.contrib.auth.views import LoginView, LogoutView, \
    PasswordChangeView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView, CreateView, \
    DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.core.signing import BadSignature
from django.contrib.auth import logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q


from .models import AdvUser, SubRubric, Bb, Comment
from .forms import ChangeUserInfoForm, RegisterUserForm, SearchForm, \
 UserCommentForm, GuestCommentForm,BbForm , AIFormSet
from .utilities import signer

# Контроллер для главной страницы
def index(request):
    bbs = Bb.objects.filter(is_active=True)[:10]
    context = {'bbs': bbs}
    return render(request, 'main/index.html', context)


"""

# Контроллер для отображения всех вакансий
def show_vacancy(request,pk):
  #vacancy = Bb.objects.filter(is_active=True, account_adds_vacancy=True)
  #context = {'vacancy':vacancy}
 # return render (request, 'main/show_vacancy.html', context)




#def by_rubric(request, pk):
    rubric = get_object_or_404(SubRubric, pk=pk)
    #bbs = Bb.objects.filter(is_active=True, rubric=pk)
    bbs = Bb.objects.filter(is_active=True, account_adds_vacancy=True)
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
    #context = {'page': page, 'bbs': page.object_list,'form': form}
    context = {'rubric': rubric, 'page': page, 'bbs': page.object_list,'form': form}
    
    return render (request, 'main/show_vacancy.html', context)
# return render(request, 'main/by_rubric.html', context)



#context = {'rubric': rubric, 'page': page, 'bbs': page.object_list,'form': form}













# Контроллер для отображения всех резюме
def show_resume(request):
    resume = Bb.objects.filter(is_active=True, account_adds_resume=True)
    context = {'resume':resume}
    return render (request, 'main/show_resume.html', context)


"""


# Контроллер для вспомогательных страниц
def other_page(request, page):
    try:
        template = get_template('main/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))

# Контроллер класса "Входа"
class BBLoginView(LoginView):
    template_name = 'main/login.html'


@login_required  # Декоратор который проверяет залогинился ли пользователь
def profile(request):  # Контроллер страницы пользовательского профиля
    bbs = Bb.objects.filter(author=request.user.pk) # Фильтрация публикаций по значению поля author
    context = {'bbs': bbs}  # (Ключ автора объявления, которым является зарегистрированный пользователь), сравнивая
     # это значение с ключом текущего пользователя 
    return render(request, 'main/profile.html', context)


 # Контроллер класса "Выхода"
class BBLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'main/logout.html'


 # Контролер класса изменяющий данные пользователя
class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin,
                                              UpdateView):
    model = AdvUser
    template_name = 'main/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('main:profile')
    success_message = 'Данные пользователя изменены'
# В процессе работы контроллер должен извлечь из модели AdvUser запись представляющую текущего пользователя
    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk  # Получаем ключ текущего пользователя (сохраняем его в атрибуте user_id)
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)
    
    
 # Контроллер класса изменяющий пароль пользователя
class BBPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin,
                                                PasswordChangeView):
    template_name = 'main/password_change.html'
    success_url = reverse_lazy('main:profile')
    success_message = 'Пароль пользователя изменен'


 # Контроллер класса регистрирующий пользователя
class RegisterUserView(CreateView):
    model = AdvUser
    
    
    template_name = 'main/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('main:register_done')


 # Контроллер класс выводящий сообщение об успешной регистрации
class RegisterDoneView(TemplateView):
    template_name = 'main/register_done.html'
    
    
 # Контроллер для активации пользователя
def user_activate(request, sign):
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



 # Контроллер класса для удаления пользовтеля
class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = AdvUser
    template_name = 'main/delete_user.html'
    success_url = reverse_lazy('main:index')

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Пользователь удален')
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)



class BBPasswordResetView(PasswordResetView):
    template_name = 'main/password_reset.html'
    subject_template_name = 'email/reset_letter_subject.txt'
    email_template_name = 'email/reset_letter_body.txt'
    success_url = reverse_lazy('main:password_reset_done')

class BBPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'main/password_reset_done.html'

class BBPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'main/password_confirm.html'
    success_url = reverse_lazy('main:password_reset_complete')

class BBPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'main/password_complete.html'

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
    
    # ПАГИНАТОР
    paginator = Paginator(bbs, 10)  # Число в параметрах это количество постов выводимых на на одной странице
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    
    
    context = {'rubric': rubric, 'page': page, 'bbs': page.object_list,
               'form': form}
    return render(request, 'main/by_rubric.html', context)

def detail(request, rubric_pk, pk):
    bb = Bb.objects.get(pk=pk)
    ais = bb.additionalimage_set.all()
    comments = Comment.objects.filter(bb=pk, is_active=True)
    initial = {'bb': bb.pk}
    if request.user.is_authenticated:
        initial['author'] = request.user.username
        form_class = UserCommentForm
    else:
        form_class = GuestCommentForm
    form = form_class(initial=initial)
    if request.method == 'POST':
        c_form = form_class(request.POST)
        if c_form.is_valid():
            c_form.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Комментарий добавлен')
        else:
            form = c_form
            messages.add_message(request, messages.WARNING,
                                 'Комментарий не добавлен')
    context = {'bb': bb, 'ais': ais, 'comments': comments, 'form': form}
    return render(request, 'main/detail.html', context)

@login_required # только зарегистрированным пользователям
def profile_bb_detail(request, pk):  # вывод страницы сведений о публикации 
    bb = get_object_or_404(Bb, pk=pk)
    ais = bb.additionalimage_set.all()
    comments = Comment.objects.filter(bb=pk, is_active=True)
    context = {'bb': bb, 'ais': ais, 'comments': comments}
    return render(request, 'main/profile_bb_detail.html', context)


# ДОБАВЛЕНИЕ ПУБЛИКАЦИИ
@login_required  # только зарегистрированным пользователям
def profile_bb_add(request): # Добавление публикации
   
  
   if request.method == 'POST':
     form = BbForm(request.POST, request.FILES)
     if form.is_valid():
         
        ''' 
         if request.user.account_add_vacancy:
             bb.user.account_adds_vacancy = True
         else:
            bb.user.account_adds_resume = True
            '''
            
     bb = form.save()
     formset = AIFormSet(request.POST, request.FILES, instance=bb)
     if formset.is_valid():
            formset.save()
            messages.add_message(request, messages.SUCCESS,
                                     'Объявление добавлено')
     return redirect('main:profile')
   else:
       # Автоматизируем вставку в поля значений по умолчанию
    form = BbForm(initial={'author': request.user.pk,
                               'email': request.user.email 
                               ,
                               'account_adds_vacancy': request.user.account_add_vacancy, 
                               'account_adds_resume': request.user.account_add_resume })
    formset = AIFormSet()
    context = {'form': form, 'formset': formset}
    return render(request, 'main/profile_bb_add.html', context)
   
   
@login_required  #  только зарегистрированным пользователям
def profile_bb_change(request, pk):  # Исправление публикации
    bb = get_object_or_404(Bb, pk=pk)
    if request.method == 'POST':
        form = BbForm(request.POST, request.FILES, instance=bb) 
        
        if form.is_valid():
            bb = form.save()
            formset = AIFormSet(request.POST, request.FILES, instance=bb)
            if formset.is_valid():
                formset.save()
                messages.add_message(request, messages.SUCCESS,
                                     'Объявление исправлено')
                return redirect('main:profile')
    else:
         form = BbForm(instance=bb)
         formset = AIFormSet(instance=bb)
        
        
    context = {'form': form, 'formset': formset}
    return render(request, 'main/profile_bb_change.html', context)





@login_required  # только зарегистрированным пользователям
def profile_bb_delete(request, pk): # Удаление публикации
    bb = get_object_or_404(Bb, pk=pk)
    if request.method == 'POST':
        bb.delete()
        messages.add_message(request, messages.SUCCESS, 'Объявление удалено')
        return redirect('main:profile')
    else:
        context = {'bb': bb}
        return render(request, 'main/profile_bb_delete.html', context)
