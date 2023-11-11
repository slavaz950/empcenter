from .models import SubRubric, SuperRubric  # Добавил SuperRubric

def empcenter_context_processor(request):
    context = {}
    
    context['super_rubrics'] = SuperRubric.objects.all() # Добавил строку (переменная для Надрубрик)
    context['rubrics'] = SubRubric.objects.all() # Строка была задана изначально (переменная для Подрубрик)
    
    context['keyword'] = ''
    context['all'] = ''
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            context['keyword'] = '?keyword=' + keyword
            context['all'] = context['keyword']
    if 'page' in request.GET:
        page = request.GET['page']
        if page != '1':
            if context['all']:
                context['all'] += '&page=' + page
            else:
                context['all'] = '?page=' + page
    return context