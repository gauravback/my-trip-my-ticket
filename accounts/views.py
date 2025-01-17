from rest_framework.response import Response
from .models import User
from .serializers import RegistrationSerializer,UserSerializer
from rest_framework import status
from rest_framework.views import APIView
import uuid
from .helper import send_password_reset_email
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from .serializers import EditProfileSerializer
from .token import MyTokenObtainPairSerializer
from rest_framework_simplejwt.exceptions import InvalidToken

class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success':'registration successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error':'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        token = str(uuid.uuid4())
        url = f"{settings.FRONTEND_URL}/reset/{token}"
        user.pwd_reset_token = token
        user.save()
        email_sent = send_password_reset_email(user.email,url)
        if not email_sent:
            return Response({'error':'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'success':'An email has been sent to your email address'}, status=status.HTTP_200_OK)


class ResetPasswordView(APIView):
    def post(self, request,token):
        try:
            user = User.objects.get(pwd_reset_token=token)
        except User.DoesNotExist:
            return Response({'error':'Token is invalid or expired'}, status=status.HTTP_404_NOT_FOUND)
        
        password = request.data['password']
        password2 = request.data['password2']
        
        if password != password2:
            return Response({'error':'Passwords do not match'},status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(password)
        user.save()
        return Response({'success':'Your password has been changed'}, status=status.HTTP_200_OK)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = User.objects.get(email=request.user)
        current_password = request.data['current_password']
        new_password = request.data['new_password']
        confirm_password = request.data['confirm_password']

        if not user.check_password(current_password):
            return Response({'error':'Incorrect password'}, status=status.HTTP_400_BAD_REQUEST)
        if new_password != confirm_password:
            return Response({'error':'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()
        return Response({'success':'Your password has been changed'}, status=status.HTTP_200_OK)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user,many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        serializer = EditProfileSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CheckTokenValidityView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            return Response({'message': 'Token is valid.'})
        except InvalidToken:
            return Response({'message': 'Token is not valid.'}, status=status.HTTP_400_BAD_REQUEST)