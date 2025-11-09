from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserTelegram
from .permissions import IsOwner
from .serializers import RegisterSerializer, UserSerializer, UserTelegramSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """
    APIView для регистрации нового пользователя.
    Позволяет создавать аккаунт, предоставляет публичный доступ.
    """

    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для просмотра информации о пользователях"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Определяет результирующий список пользователей для текущего пользователя"""

        user = self.request.user
        if user.is_staff or user.is_superuser:
            return User.objects.all()
        return User.objects.filter(pk=user.pk)


class UserDetailView(generics.RetrieveUpdateAPIView):
    """
    APIView для получения и обновления профиля текущего пользователя.
    Доступ разрешен только авторизованным пользователям.
    """

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Возвращает объект — текущий пользователь"""

        return self.request.user


class DeactivateUserView(APIView):
    """
    APIView для деактивации профиля пользователя.
    Метод DELETE снимает флаг активности и возвращает статус 204.
    """

    permission_classes = [IsAuthenticated]

    def delete(self, request):
        """Деактивирует текущего пользователя"""

        user = request.user
        user.is_active = False
        user.save()
        return Response(
            {"detail": "Пользователь деактивирован"}, status=status.HTTP_204_NO_CONTENT
        )


class UserTelegramViewSet(viewsets.ModelViewSet):
    """ViewSet для управления Telegram-профилем пользователя"""

    serializer_class = UserTelegramSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        """Возвращает Telegram-профиль только для текущего пользователя"""

        user = self.request.user
        return UserTelegram.objects.filter(user=user)

    def perform_create(self, serializer):
        """Связывает профиль Telegram c текущим пользователем при создании"""

        serializer.save(user=self.request.user)
