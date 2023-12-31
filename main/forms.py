
from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from captcha.fields import CaptchaField

from .models import AdvUser, SuperRubric, SubRubric, Bb, AdditionalImage, \
    Comment
from .apps import user_registered


    #TYPE_ACCOUNT = (
    # ('VAC', 'Вакансии'),
    # ('RES', 'Резюме'),
   # )

# Форма для ввода основных данных
class ChangeUserInfoForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Адрес электронной почты')

# Вложеный класс Meta внутри которого указываем характеристики для нашего целевого класса ChangeUserInfoForm
    class Meta:
        model = AdvUser # Указываем модель с которой работаем 
        fields = ('username', 'email', 'first_name', 'last_name','send_messages') # Какие поля должны быть выведены внутри формы

# Форма для занесения сведений о новом пользователе
class RegisterUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Адрес электронной почты')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput,
      help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label='Пароль (повторно)',
      widget=forms.PasswordInput,
      help_text='Введите тот же самый пароль еще раз для проверки')
   
    account_add_vacancy = forms.BooleanField(
                  label='Аккаунт для добавления вакансии (для работодателей)')
    account_add_resume = forms.BooleanField(
                  label='Аккаунт для добавления резюме (поиск работы)')
   

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if password1:
            password_validation.validate_password(password1)
        return password1

    def clean(self):
        super().clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError(
              'Введенные пароли не совпадают', code='password_mismatch')}
            raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False # Является ли пользователь активным по умолчанию False
        user.is_activated = False # Выполнил ли пользователь процедуру активации по умолчанию False
        user.group = 'Пользователь'
        
        # УСЛОВИЕ
        # Если Пользователь выбрал оба вида аккаунтов или не одного выводим сообщение (либо возбуждаем исключение)
        # " Вы не можете выбрать одновременно как оба вида учётной записи так и не одного."
        
        if commit:
            user.save()
        user_registered.send(RegisterUserForm, instance=user)
        return user

    class Meta:
        model = AdvUser
        fields = ( 
                  'username', 'email', 'password1', 'password2',
                  'first_name', 'last_name', 'send_messages')

#'account_type',

# Форма Рубрик (делаем поле "Надрубрики" SuperRubric обязательным)
class SubRubricForm(forms.ModelForm):
    super_rubric = forms.ModelChoiceField(queryset=SuperRubric.objects.all(),
                                        empty_label=None, label='Надрубрика',
                                        required=True)

    class Meta:
        model = SubRubric
        fields = '__all__'


# Форма поиска
class SearchForm(forms.Form):
    keyword = forms.CharField(required=False, max_length=20, label='')
 
    
 # ФОРМА ДЛЯ ДОБАВЛЕНИЯ ПУБЛИКАЦИИ
class BbForm(forms.ModelForm):
    # Конструктор прописывается для того чтобы в выпадающем списке на странице (в случае если не выбрано
  #def __init__(self,*args,**kwargs):   
     #super().__init__(*args, **kwargs)  
     #self.fields['rubric'].empty_label = 'Категория не выбрана'
        
 class Meta:
            model = Bb
            #fields = '__all__'
            fields = ('author','rubric','title','organization','content','image','schedule','experience','education',
                 'empoloyment_area','salary_from','salary_up_to','telephone','email',
                    'name_contact','account_adds_vacancy','account_adds_resume' ) 
            # 
            # 
                
            labels = {'author' : 'Имя пользователя','rubric': 'Категория ','title': 'Должность ','content': 'О вакансии/ О себе ','image': 'Изображение ',
                'schedule': 'График работы ','experience': 'Опыт работы ','education': 'Образование ',
                'empoloyment_area': 'Район трудоустройства ','salary_from': 'Зарплата от ','salary_up_to': 'Зарплата до',
                'telephone': 'Телефон ','email': 'Электронная почта',
                'name_contact': 'Контактное лицо','organization': 'Организация',
                'account_adds_vacancy': 'Вакансия','account_adds_resume': 'Резюме'
                 }
            
           # 
    
            help_texts = {'rubric': 'Укажите категорию в которой хотите разместить Вашу публикацию. ',
            'title': 'Укажите Должность) ',
            'author' : '',
            'content': 'Расскажите, в зависимости от ситуации о вакансии или о себе. ',
            'image': 'Добавьте изображение (Не обязательно) ',
            'schedule': 'Выберите из списка график работы. ',
            'experience': 'выберите из списка оптимальное значение подходящее для Вашего конкретного случая.  ',
            'education': 'Выберите из списка соответствующий уровень образования . ',
            'empoloyment_area': 'Укажите регион или адрес местонахождения вакансии. ',
            'salary_from': 'Укажите минимальный уровень заработной платы. ',
            'salary_up_to': 'Укажите максимальный уровень зарплаты (Если такой предел имеется). Иначе оставьте это поле пустым.  ',
            'telephone': 'Укажите телефон для связи. ',
            'email': 'Укажите адрес электронной почты для связи. ',
            'name_contact': 'Укажите как к Вам можно обращаться (Фамилия, Имя и т.п..)',
            'organization': 'Если вы публикуете вакансию.Укажите название своей организации. При публикации Резюме это поле заполнять не нужно ',
            'account_adds_vacancy': '',
            'account_adds_resume': '' 
            
    }
            widgets = {'author': forms.HiddenInput  # Делаем поле скрытым (значение передаётся автоматически)
                      # 'account_adds_vacancy': forms.HiddenInput, # Делаем поле скрытым (значение передаётся автоматически)
                      # 'account_adds_resume': forms.HiddenInput # Делаем поле скрытым (значение передаётся автоматически)
                        } 
        
AIFormSet = inlineformset_factory(Bb, AdditionalImage, fields='__all__')


# Форма комментариев оставленных зарегистрированными пользователями
class UserCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('is_active',)
        widgets = {'bb': forms.HiddenInput}


    """  Поле is_active (признак будет ли комментарий выводится на странице) уберём из форм,
        поскольку оно требуется лишь администрации сайта. У поля bb, хранящего ключ объявления, с которым 
        связан комментарий, укажем в качестве элемента управления скрытое поле 
    """

# Форма Комментариев оставленных Незарегистрированными пользователями сайта (Гостями) 
class GuestCommentForm(forms.ModelForm):
    captcha = CaptchaField(label='Введите текст с картинки',
              error_messages={'invalid': 'Неправильный текст'})

    class Meta:
        model = Comment
        exclude = ('is_active',)
        widgets = {'bb': forms.HiddenInput}
