
from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from captcha.fields import CaptchaField

from .models import AdvUser, SuperRubric, SubRubric, Bb, AdditionalImage, \
    Comment
from .apps import user_registered


# Форма для ввода основных данных
class ChangeUserInfoForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Адрес электронной почты')

    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'first_name', 'last_name',
                  'send_messages')

# Форма для занесения сведений о новом пользователе
class RegisterUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Адрес электронной почты')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput,
      help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label='Пароль (повторно)',
      widget=forms.PasswordInput,
      help_text='Введите тот же самый пароль еще раз для проверки')

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
        if commit:
            user.save()
        user_registered.send(RegisterUserForm, instance=user)
        return user

    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'password1', 'password2',
                  'first_name', 'last_name', 'send_messages')


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
    
    
# Форма для ввода публикации, связанная с моделью Bb

# В форме будем выводить все поля модели Bb. Для поля автора публикации author зададим  
# в качестве элемента управления HiddenInput, т.е. скрытое поле - все равно значение туда 
# будет заноситься программно.
class BbForm(forms.ModelForm):
    class Meta:
        model = Bb
        fields = '__all__'
        widgets = {'author': forms.HiddenInput}

# Встроенный набор форм  AIFormSe связанный с моделью AdditionalImage в которые будут заноситься 
 # дополнительные иллюстрации 
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
