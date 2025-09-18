from django.http import JsonResponse
from rest_framework import generics
from .models import User
from .serializers import UserSerializer

def hello(request):
    return JsonResponse({"message":"accounts working!"})


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer