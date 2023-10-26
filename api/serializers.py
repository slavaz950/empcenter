from rest_framework import serializers
from main.models import Bb
from main.models import Comment

# Сериализатор формирующий список объявлений
class BbSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bb
        fields = ('id', 'title', 'content', 'price', 'created_at')
        """
        Ради компактности выводится только:
        Ключ, Название, Описание, Цена, ВременНая отметка создания публикации
        """
        
# Сериализатор выдающий сведения о публикации
class BbDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bb
        fields = ('id', 'title', 'content', 'price', 'created_at', 'contacts', 'image')
        """
        В состав сведений о выбранной публикации помимо других полей включены:
        контакты и интернет-адрес основной иллюстрации
        """
 # Сериализатор который отправляет список комментариев и добавляет новый комментарий
class CommentSerializer(serializers.ModelSerializer) :
    class Meta:
        model = Comment
        fields = ('bb', 'author', 'content', 'created_at')       
