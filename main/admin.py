from django.contrib import admin
import datetime

from .models import AdvUser
from .utilities import send_activation_notification
from .models import SuperRubric, SubRubric
from .forms import SubRubricForm


#
# Регистрация действия, которое разошлёт пользователям письма 
# # с предписаниями выполнить активацию
def send_activation_notifications(modeladmin, request, queryset):
    for rec in queryset:
        if not rec.is_activated:
            send_activation_notification(rec)  # Вызывается для не выполнивших активациюЫЫ
    modeladmin.message_user(request, 'Письма с требованиями отправлены')
send_activation_notifications.short_description = \
    'Отправка писем с требованиями активации'
    
# Фильтрация пользователей выполнивших активацию    
class NonactivatedFilter(admin.SimpleListFilter):
    title = 'Прошли активацию?'
    parameter_name = 'actstage'
    
    def lookups(self, request, model_admin):
        return(
            ('activated', 'Прошли'),
            ('threedays', 'Не прошли более 3 дней'),
            ('week', 'Не прошли более недели'),
        )

    def queryset(self, request, queryset):
        val = self.value()
        if val == 'activated':
            return queryset.filter(is_active=True, is_activated=True)
        elif val == 'threedays':
            d = datetime.date.today() - datetime.timedelta(days=3)
            return queryset.filter(is_active=False, is_activated=False, date_joined_date_It=d)
        
class AdvUserAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_activated', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = (NonactivatedFilter,)
    fields = (('username', 'email'),('first_name', 'last_name'),
              ('send_messages', 'is_active', 'is_activated'),
              ('is_staff', 'is_superuser'), 
              'groups', 'user_permissions',
              ('last_login', 'date_joined'))
    realdony_fields = ('last_login', 'date_joined')
    actions = (send_activation_notifications,)  

# Редактор рубрик
class SubRubricInline(admin.TabularInline):
    model = SubRubric
    
# Встроенный редактор рубрик
class SuperRubricAdmin(admin.ModelAdmin):
    exclude = ('super_rubric',)
    inlines = (SubRubricInline,)
    
    
class SubRubricAdmin(admin.ModelAdmin):
    form = SubRubricForm    
    

admin.site.register(AdvUser, AdvUserAdmin, SuperRubric, SuperRubricAdmin, SubRubric, SubRubricAdmin)  
#admin.site.register(AdvUser, AdvUserAdmin) # Удалить если не потребуется
# admin.site.register(SuperRubric, SuperRubricAdmin)   # Удалить если не потребуется
    
# Register your models here.
