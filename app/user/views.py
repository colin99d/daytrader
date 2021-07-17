from .serializers import UserSerializer, UserSerializerWithToken
from rest_framework.authtoken.views import ObtainAuthToken
from trader.serializers import AlgorithmSerializer
from rest_framework.authtoken.models import Token
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from trader.models import Algorithm
from django.urls import reverse


@api_view(['GET'])
def current_user(request):
    """Determine the current user by their token, and return their data"""
    
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['GET'])
def update_user_algo(request):
    """Change the user's chosen algorithm"""
    algoId = request.GET.get('algo', '')
    algo = Algorithm.objects.get(pk=algoId)
    setattr(request.user,"selected_algo",algo)
    request.user.save()
    return Response(UserSerializer(request.user).data)

@api_view(['GET'])
def update_user_email(request):
    """Toggle whether the user gets emails"""
    email = request.user.daily_emails
    new_status = False if email else True
    setattr(request.user,"daily_emails",new_status)
    request.user.save()
    return Response(UserSerializer(request.user).data)


class UserList(APIView):
    """Create a new user. It's called 'UserList' because normally we'd have a get
    method here too, for retrieving a list of all User objects."""

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                       context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'username': user.username,
            'email': user.email,
            'id': user.id,
            'selected_algo': AlgorithmSerializer(user.selected_algo).data,
            'daily_emails': user.daily_emails
        })


def change_password(request, token):
    if request.method == "GET":
        args = {"token":token}
        return render(request, 'change_password.html',args)