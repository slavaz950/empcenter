from django import forms
from .models import AdvUser
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from .apps import user_registered
from .models import SuperRubric, SubRubric

# Форма 
class ChangeUserInfoForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Адрес электронной почты')

    '''
    # Удалить если не потребуется
    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'send_messages')
    '''

    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'first_name', 'last_name', 'send_messages')
        
 # Форма Регистрации  
class RegisterUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Адрес электронной почты')
    password1 = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput,
                                help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label='Пароль (повторно)',
                                widget=forms.PasswordInput,
                                help_text='Введите тот же самый пароль для проверки')

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if password1:
            password_validation.validate_password(password1)
        return password1

    def clean(self):
        super().clean()
        ##cleaned_data = super().clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError(
                ' Введённые пароли не совпадают', code='password_mismatch')}
            raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = True  # Является ли пользователь активным False по умолчанию
        user.is_activated = True # Выполнил ли пользователь процедуру активации False по умолчанию
        if commit:
            user.save()
        user_registered.send(RegisterUserForm, instance=user)
        return user

    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'password1', 'password2', 
                  'first_name', 'last_name', 'send_messages')

    '''
    # Удалить если не потребуется
    class Meta:
        model = AdvUser
        fields = ('email','password1','password2')
    '''

# Форма Рубрик  (делаем поле надрубрики super_rubric обязательным)
class SubRubricForm(forms.ModelForm): 
    super_rubric = forms.ModelChoiceField(
        queryset=SuperRubric.objects.all(),empty_label=None, label='Надрубрика', required=True)
    
    class Meta:
        model = SubRubric
        fields = '__all__'
        
# Форма поиска
class SearchForm(forms.Form):
    keyword = forms.CharField(required=False, max_length=20, label='')


