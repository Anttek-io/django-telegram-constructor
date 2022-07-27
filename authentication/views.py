import pytz
from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from authentication.models import CustomUser, Token
from core.settings import TOKEN_TTL


@api_view(['POST'])
def login_view(request):
    _username = request.POST.get('username')
    _password = request.POST.get('password')
    if None in (_username, _password):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    _user_exists = CustomUser.objects.filter(username=_username).exists()
    if not _user_exists:
        return Response(status=status.HTTP_404_NOT_FOUND)
    _user = authenticate(request, username=_username, password=_password)
    if _user is None:
        return Response(status=status.HTTP_403_FORBIDDEN)
    utc_now = timezone.now()
    utc_now = utc_now.replace(tzinfo=pytz.utc)
    Token.objects.filter(user=_user, last_use__lt=utc_now - TOKEN_TTL).delete()
    token, created = Token.objects.get_or_create(user=_user)
    return Response({'token': token.key,
                     'user': {'id': token.user_id,
                              'username': token.user.username}})


@api_view(['POST'])
def logout_view(request):
    if request.user.is_anonymous:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    _user = request.user
    _user.auth_token.delete()
    return Response(status=status.HTTP_200_OK)
