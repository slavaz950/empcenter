from django.db import models
from django.contrib.auth.models import AbstractUser

class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Прошёл активацию?')
    send_messages = models.BooleanField(default=True, verbose_name='Слать оповещения о новых комментариях?')
    
class Meta(AbstractUser.Meta): pass

   
   # Класс модели Rubric  в которой хранятся надрубрики и подрубрики
class Rubric(models.Model):
       name = models.CharField(max_length=20, db_index=True, unique=True, verbose_name='Название')
       order = models.SmallIntegerField(default=0, db_index=True, verbose_name='Порядок')
       super_rubric = models.ForeignKey('SuperRubric', on_delete=models.PROTECT, null=True, blank=True, verbose_name='Надрубрика')
 # Мы не задаём никаких параметров самой модели - поскольку пользователи не будут работать с ней непосредственно,
  # здесь это лишнее.
 
 
 # Диспетчер записей SuperRubric
class SuperRubricManager(models.Manager):
    def get_queryset(self):  # Метод (переопределённый) выбирает только записи 
        return super().get_queryset().filter(super_rubric__isnull=True) # с пустым полем super_rubric
    
 # Модель надрубрик SuperRubric
class SuperRubric(Rubric):
     objects = SuperRubricManager()  # Задаём диспетчер в качестве основного
     
     def __str__(self):   # Объявление метода, который генерирует строковое представление надрубрики (её название)
         return self.name
 #    
class Meta:
    proxy = True
    ordering = ('order', 'name')
    verbose_name = 'Надрубрика'
    verbose_name_plural = 'Надрубрики'  
    
    
 #  Диспетчер записей SubRubric (Подрубрики) 
class SubRubricManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=False)
 
 # Модель подрубрик SubRubric 
class SubRubric(Rubric):
    object = SubRubricManager()
    
    def __str__(self):
        return '%s - %s' % (self.super_rubric.name, self.name)
    #
    class Meta:
        proxy = True
        ordering = ('super_rubric__order', 'super_rubric__name', 'order', 'name')
        verbose_name = 'Подрубрика'
        verbose_name_plural = 'Подрубрики'
  
    
    
# Create your models here.
