from main.models import SubRubric

# Обработчик контекста
def empcenter_context_processor(request):
    context = {}
    context['rubrics'] = SubRubric.objects.all()
    return context