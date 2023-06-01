from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User

class ExampleView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


class RegisterView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = request.data

        username = data.get('username')
        password = data.get('password')
        confirm_password = data.get('confirmPassword')

        if password != confirm_password:
            return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create(username=username)
        user.set_password(password)
        user.save()

        return Response({'success': 'User created successfully'}, status=status.HTTP_201_CREATED)