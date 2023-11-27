from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save

from .utilities import get_timestamp_path, send_new_comment_notification


#from django.views.generic.base import setup   # Скорее всего не понадобиться - УДАЛИТЬ
#from django.views.generic.base import setup  # Скорее всего не понадобиться - УДАЛИТЬ
#from django.views import View  # Скорее всего не понадобиться - УДАЛИТЬ


# Модель пользователя


class AdvUser(AbstractUser):
    
    TYPE_ACCOUNT = (
    ('VAC', 'Вакансии'),
    ('RES', 'Резюме'),
    )
    
    
    is_activated = models.BooleanField(default=True, db_index=True,
                                       verbose_name='Прошел активацию?')
    
    
    """
    account_add_vacancy = models.BooleanField(default=False,
                  verbose_name='Аккаунт для добавления вакансии (для работодателей)')
    account_add_resume = models.BooleanField(default=False,
                  verbose_name='Аккаунт для добавления резюме (поиск работы)')
    """
    
    
    send_messages = models.BooleanField(default=True,
                  verbose_name='Слать оповещения о новых комментариях?') 
    
    account_type = models.CharField(max_length=100, default='RES', 
	choices = TYPE_ACCOUNT, verbose_name='Тип учётной записи')
    
    
      
    # Добавляем поле "Группа" (Группа доступа) значение по умолчанию "Пользователь"           

# При удалении пользователя удаляются оставленные им обявления
    def delete(self, *args, **kwargs):
        for bb in self.bb_set.all():
            bb.delete()
        super().delete(*args, **kwargs)

    class Meta(AbstractUser.Meta):
        pass









"""
ТЕСТОВЫЙ ВАРИАНТ МОДЕЛИ ПОЛЬЗОВАТЕЛЯ (ДЛЯ ОБРАЗЦА - ПО ОКОНЧАНИЮ УДАЛИТЬ)
class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True,
                                       verbose_name='Прошел активацию?')
    send_messages = models.BooleanField(default=True,
                  verbose_name='Слать оповещения о новых комментариях?')

# При удалении пользователя удаляются оставленные им обявления
    def delete(self, *args, **kwargs):
        for bb in self.bb_set.all():
            bb.delete()
        super().delete(*args, **kwargs)

    class Meta(AbstractUser.Meta):
        pass
"""



# Класс модели Rubric в которой хранятся надрубрики и подрубрики
class Rubric(models.Model):
    name = models.CharField(max_length=20, db_index=True, unique=True,
                            verbose_name='Название')
    order = models.SmallIntegerField(default=0, db_index=True,
                                     verbose_name='Порядок')
    super_rubric = models.ForeignKey('SuperRubric', on_delete=models.PROTECT,
                   null=True, blank=True, verbose_name='Надрубрика')
    # Мы не задаём никаких параметров самой модели - поскольку пользователи не будут работать с ней непосредственно
    # здесь это лишнее.

# Диспетчер записей SuperRubriс
class SuperRubricManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=True)

# Класс Модели SuperRubriс
class SuperRubric(Rubric):
    objects = SuperRubricManager()
    
# Для того чтобы получить "красивый" вывод информации. Используем метод  __str__ . В этом методе указываем какая именно информация будет выводится 
    def __str__(self):  # когда мы будем выводить этот объект
        return self.name   # 
    # Можно отформатировать строку и написать следующее
    # return f'Имя:  {self.name}'

    class Meta:
        proxy = True
        ordering = ('order', 'name')
        verbose_name = 'Надрубрика'
        verbose_name_plural = 'Надрубрики'


# Диспетчер записей SubRubric (Подрубрики)
class SubRubricManager(models.Manager):
    def get_queryset(self):
       return super().get_queryset().filter(super_rubric__isnull=False)

# Модель подрубрик SubRubric 
class SubRubric(Rubric):
    
    SuperRubricManager
    objects = SubRubricManager()
    #objects = SuperRubricManager()
    
    def __str__(self):
         return '%s - %s' % (self.super_rubric.name, self.name)
       

    class Meta:
        proxy = True
        ordering = ('super_rubric__order', 'super_rubric__name', 'order',
                    'name')
        verbose_name = 'Подрубрика'
        verbose_name_plural = 'Подрубрики'


# Модель хранящая публикации
class Bb(models.Model):
    
    
    
    SCHEDULE_CHOICE = (
    ('FE', 'Полная занятость'),
    ('FS', 'Гибкий график'),
    ('SW', 'Сменный график'),
    ('FT', 'Скользящий график'),
    ('BD', 'Разрывной график'),
    ('SM', 'Вахтовый метод'),
    ('AN', 'Другое'),
    )
    
    
    EDUCATION_CHOICE = (
    ('SO', 'Среднее'),
    ('SPO', 'Среднее-профессиональное (СПО)'),
    ('VO', 'Высшее (ВО)'),
    )


    rubric = models.ForeignKey(SubRubric, on_delete=models.PROTECT,verbose_name='Категория')
    title = models.CharField(max_length=100, verbose_name='Должность')
    content = models.TextField(verbose_name='Описание')  #  (Описание) О вакансии / О себе
    image = models.ImageField(blank=True, upload_to=get_timestamp_path,
                              verbose_name='Изображение')
                              
    schedule = models.CharField(max_length=40, choices = SCHEDULE_CHOICE, default='Полная занятость',  verbose_name='График работы')
    experience = models.CharField(max_length=100, default='Не указан', verbose_name='Опыт работы')
    education = models.CharField(max_length=40, default='Среднее-профессиональное', choices = EDUCATION_CHOICE, verbose_name='Образование')
    empoloyment_area = models.CharField(max_length=150, default='Не указан', verbose_name='Район трудоустройства')
    salary_from = models.IntegerField(default='0', verbose_name='Зарплата от')                         
    salary_up_to = models.IntegerField(default='0', verbose_name='Зарплата до') 
    telephone = models.CharField(max_length=40, default='Не указан', verbose_name='Телефон')
    #addit_info = models.TextField(verbose_name='Дополнительная информация')  #  
    account = models.CharField(max_length=40, default='Не указан??????', verbose_name='Тип учётной записи')
    name_contact = models.CharField(max_length=100, default='Не указано', verbose_name='ФИО соискателя')
    organization = models.CharField(max_length=100, default='Не указано', verbose_name='Название организации')
    email = models.EmailField(default='example@mail.ru' ,verbose_name='E-mail')  
    author = models.ForeignKey(AdvUser, on_delete=models.CASCADE,
                               verbose_name='Автор публикации')
    is_active = models.BooleanField(default=True, db_index=True,
                                    verbose_name='Выводить в списке?')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True,
                                      verbose_name='Опубликовано')


    """
    В переопределённом методе delete() перед удалением текущей записи мы перебираем и
    вызовом метода delete() удаляем все связанные дополнительные иллюстрации. При вызове метода delete()
    возникает сигнал post_delete, обрабатываемый приложением django_cleanup, которое в ответ удалит все файлы,
    хранящиеся в удалённой записи.
    """
    def delete(self, *args, **kwargs):
        for ai in self.additionalimage_set.all():
            ai.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Публикации' 
        verbose_name = 'Публикация'
        ordering = ['-created_at'] # Сортировка по полю (-) меняет порядок сортировки



"""
ТЕСТОВЫЙ ВАРИАНТ МОДЕЛИ ХРАНЯЩЕЙ ПУБЛИКАЦИИ  (ДЛЯ ОБРАЗЦА - ПО ОКОНЧАНИЮ УДАЛИТЬ)
class Bb(models.Model):
    rubric = models.ForeignKey(SubRubric, on_delete=models.PROTECT,
                                          verbose_name='Рубрика')
    title = models.CharField(max_length=40, verbose_name='Товар')
    content = models.TextField(verbose_name='Описание')
    price = models.FloatField(default=0, verbose_name='Цена')
    contacts = models.TextField(verbose_name='Контакты')
    image = models.ImageField(blank=True, upload_to=get_timestamp_path,
                              verbose_name='Изображение')
    author = models.ForeignKey(AdvUser, on_delete=models.CASCADE,
                               verbose_name='Автор объявления')
    is_active = models.BooleanField(default=True, db_index=True,
                                    verbose_name='Выводить в списке?')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True,
                                      verbose_name='Опубликовано')

"""
"""
    В переопределённом методе delete() перед удалением текущей записи мы перебираем и
    вызовом метода delete() удаляем все связанные дополнительные иллюстрации. При вызове метода delete()
    возникает сигнал post_delete, обрабатываемый приложением django_cleanup, которое в ответ удалит все файлы,
    хранящиеся в удалённой записи.
"""
"""
    def delete(self, *args, **kwargs):
        for ai in self.additionalimage_set.all():
            ai.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Объявления'
        verbose_name = 'Объявление'
        ordering = ['-created_at']

"""





# Модель дополнительных иллюстраций в объявлении
class AdditionalImage(models.Model):
    bb = models.ForeignKey(Bb, on_delete=models.CASCADE,
                           verbose_name='Объявление')
    image = models.ImageField(upload_to=get_timestamp_path,
                              verbose_name='Изображение')

    class Meta:
        verbose_name_plural = 'Дополнительные иллюстрации'
        verbose_name = 'Дополнительная иллюстрация'


# Модель комментариев
class Comment(models.Model):
    bb = models.ForeignKey(Bb, on_delete=models.CASCADE,
                               verbose_name='Объявление')
    author = models.CharField(max_length=30, verbose_name='Автор')
    content = models.TextField(verbose_name='Содержание')
    is_active = models.BooleanField(default=True, db_index=True,
                                    verbose_name='Выводить на экран?')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True,
                                      verbose_name='Опубликован')

    class Meta:
        verbose_name_plural = 'Комментарии'
        verbose_name = 'Комментарий'
        ordering = ['created_at']


def post_save_dispatcher(sender, **kwargs):
    author = kwargs['instance'].bb.author
    if kwargs['created'] and author.send_messages:
        send_new_comment_notification(kwargs['instance'])

post_save.connect(post_save_dispatcher, sender=Comment)
