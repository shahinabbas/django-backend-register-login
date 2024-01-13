from django.contrib.auth.models import User
from rest_framework import generics, status
from accounts import serializers
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView


class Register(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                content = {
                    'message': 'User Registered Successfully',
                    'user': serializer.data,
                }
                return Response(content, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if username and password:
            print(username, password)
            user = authenticate(request, username=username, password=password)
            print(user)
            if user:
                login(request, user)
                refresh = RefreshToken.for_user(user)
                serializer = serializers.RegisterSerializer(user)
                return Response({
                    'Message': 'Login Successful',
                    'user': serializer.data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Both username and password are required'}, status=status.HTTP_400_BAD_REQUEST)
