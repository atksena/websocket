from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class ExampleView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


class RegisterView(APIView):
    authentication_classes = []

    def post(self, request):
        data = request.data

        username = data.get('username')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password != confirm_password:
            return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password)

        return Response({'success': 'User created successfully'}, status=status.HTTP_201_CREATED)