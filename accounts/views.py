from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers import ChangePasswordSerializer, UserSerializer


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

class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes=[permissions.IsAuthenticated]

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({'old_password':['wrong password.']}, status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(serializer.validated_data['new_password'])
            user.save()

            return Response({'detail':'Password updated successfully'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    # def post(self, request, *args, **kwargs):
    #     serializer = ChangePasswordSerializer(data=request.data)

    #     if serializer.is_valid():
    #         user = request.user

    #         if not user.check_password(serializer.validated_data['old_password']):
    #             return Response({'old_password':'wrong password'}, status=status.HTTP_400_BAD_REQUEST)

    #         user.set_password(serializer.validated_data['new_password'])
    #         user.save()

    #         update_session_auth_hash(request, user)

    #         return Response({'detail':'Password updated successfully'}, status=status.HTTP_200_OK)

    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class PasswordResetRequestAPI(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        email = request.data.get('email', '').strip()
        if not email:
            return Response({'email': ['This field is required.']}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Do not reveal whether the email exists
            return Response({'detail': 'If the email exists, a reset link has been sent.'}, status=status.HTTP_200_OK)

        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        # Optionally send email; for dev you can inspect uid/token in response
        reset_link = f"{request.build_absolute_uri('/accounts/reset/')}{uidb64}/{token}/"
        try:
            send_mail(
                subject='Password reset',
                message=f'Reset your password: {reset_link}',
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', None),
                recipient_list=[email],
                fail_silently=True,
            )
        except Exception:
            pass

        return Response({'detail': 'If the email exists, a reset link has been sent.', 'uidb64': uidb64, 'token': token}, status=status.HTTP_200_OK)


class PasswordResetConfirmAPI(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def get(self, request, uidb64, token, *args, **kwargs):
        return Response({'detail': 'Use POST with new_password.'}, status=200)

    def post(self, request, uidb64, token, *args, **kwargs):
        new_password = request.data.get('new_password')
        if not new_password:
            return Response({'new_password': ['This field is required.']}, status=status.HTTP_400_BAD_REQUEST)

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except Exception:
            return Response({'detail': 'Invalid link.'}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({'detail': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({'detail': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)

