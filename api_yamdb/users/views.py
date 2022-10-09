from rest_framework.filters import SearchFilter
from .serializers import (SignupSerializer, TokenSerializer,
                          UserAdminSerializer,
                          UserNotAdminSerializer)
from .permissions import IsAdmin
from .models import User
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions, viewsets
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import action


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserAdminSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username',)

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(permissions.IsAuthenticated,),
        url_path='me'
    )
    def me(self, request):
        serializer = UserAdminSerializer(request.user)
        if request.method == 'PATCH':

            if request.user.is_admin:
                serializer = UserAdminSerializer(
                    request.user,
                    data=request.data,
                    partial=True
                )
            else:
                serializer = UserNotAdminSerializer(
                    request.user,
                    data=request.data,
                    partial=True
                )

            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def signup(request):
    password = User.objects.make_random_password()
    serializer = SignupSerializer(
        data=request.data, context={'password': password})
    if serializer.is_valid():
        new_user = serializer.save()
        send_mail(
            'Регистрация на сервисе api_yamdb',
            'Поздравляем с регистрацией!'
            f'Ваш код подтверждения: {password}',
            'auth@yamdb.com',
            [new_user.email, ],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def token(request):
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid():
        user = get_object_or_404(
            User, 
            username=serializer.validated_data["username"]
        )
        if user.check_password(serializer.validated_data["confirmation_code"]):
            token = AccessToken.for_user(user)
            return Response(
                {"token": f"{token}"},
                status=status.HTTP_200_OK
            )
        return Response(
            {"message": "Ошибка доступа"},
            status=status.HTTP_400_BAD_REQUEST
        )
    return Response({'message': 'Ошибка в данных', 'errors': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST)
