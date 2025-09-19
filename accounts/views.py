from django.http import JsonResponse
from rest_framework import generics, permissions
from .models import User
from .serializers import UserSerializer

def hello(request):

    return JsonResponse({"message":"accounts working!"})


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
