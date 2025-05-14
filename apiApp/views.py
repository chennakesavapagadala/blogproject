from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView

from django.http import Http404
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


from postApp.models import Post
from commentApp.models import Comment
from .serializers import PostSerializer, CommentSerializer, RegisterSerializer

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters



class RegisterView(APIView):
    
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
        
    def get(self, request, pk=None):
        if pk:
            user = self.get_object(pk)
            serializer = RegisterSerializer(user)
            return Response(serializer.data)
        
        users = User.objects.all()
        serializer = RegisterSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
         
    def put(self, request, pk):
        employee = self.get_object(pk)
        serializer = RegisterSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        employee = self.get_object(pk)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    permission_classes = [AllowAny]
        

class PostView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]
    pagination_class = PageNumberPagination
    filterset_fields = ['author', 'title']
    search_fields = ['title'] # ['title'] for like start with name in a title
    ordering_fields = ['id']
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]



class CommentView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]
    










