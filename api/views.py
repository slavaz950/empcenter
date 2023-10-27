"""

from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import RetrieveAPIView

from main.models import Bb, Comment
from .serializers import BbSerializer, BbDetailSerializer, CommentSerializer 

#from .serializers import BbDetailSerializer
#from rest_framework.decorators import permission_classes
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.permissions import IsAuthenticatedOrReadOnly
#from main.models import Comment
#from .serializers import CommentSerializer

@api_view(['GET'])
# Контроллер выдающий список публикаций
def bbs(request):
    if request.method == 'GET':
        bbs = Bb.objects.filter(is_active=True) [:10]
        serializer = BbSerializer(bbs, many=True)
        return Response(serializer.data)
    
# Контроллер выдающий сведения о выбранной публикации
class BbDetailView(RetrieveAPIView):
    queryset = Bb.objects.filter(is_active=True)
    serializer_class = BbDetailSerializer
    
# Контроллер выдающий список комментариев
@api_view(['GET', 'POST'])
# Позволяем всем просматривать комментарии (даже если пользователь незарегистрирован)
@permission_classes((IsAuthenticatedOrReadOnly,)) 
def comments(request, pk):
    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            comments = Comment.objects.filter(is_active=True, bb=pk)
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)

    
 # Контроллер выдающий сведения о  

# Create your views here.



"""



from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import RetrieveAPIView
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from main.models import Bb, Comment
from .serializers import BbSerializer, BbDetailSerializer, CommentSerializer

@api_view(['GET'])
def bbs(request):
    if request.method == 'GET':
        bbs = Bb.objects.filter(is_active=True)[:10]
        serializer = BbSerializer(bbs, many=True)
        return Response(serializer.data)

class BbDetailView(RetrieveAPIView):
    queryset = Bb.objects.filter(is_active=True)
    serializer_class = BbDetailSerializer

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def comments(request, pk):
    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    else:
        comments = Comment.objects.filter(is_active=True, bb=pk)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
