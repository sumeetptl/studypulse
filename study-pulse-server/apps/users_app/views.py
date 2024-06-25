# Local Packages
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from .utils import Util
from .renderers import UserRenderer
from .models import User
from .serializers import UserProfileSerializer, UserRegistrationSerializer, \
    UserLoginSerializer, ChangePasswordSerializer, \
    SendPasswordResetEmailSerializer, ResetPasswordSerializer, \
    EmailVerificationSerializer

# Django

# Django Rest Framework


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegisterationView(APIView):
    renderer_classes = [UserRenderer]
    serializer_class = UserRegistrationSerializer

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(request.data)
            token = get_tokens_for_user(user)
            current_site = get_current_site(request).domain
            relative_link = reverse('email-verify')
            absurl = 'http://'+current_site+relative_link + \
                "?token="+str(token.get('access'))
            email_body = 'Hi '+user.name + \
                ' Use the link below to verify your email \n' + absurl
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Verify your email'}
            Util.send_email(data)
            return Response({"msg": "Please check your email"},
                            status=status.HTTP_201_CREATED)
            # verification_email(user.email,user.name)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    renderer_classes = [UserRenderer]
    serializer_class = UserLoginSerializer

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            try:
                user = User.objects.get(email=email)
                if password != user.password:
                    token = get_tokens_for_user(user)
                    return Response({"token": token, "msg": "User Found"},
                                    status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"msg": "User Doesn't Exist"},
                                status=status.HTTP_200_OK)
        else:
            return Response({'errors': {'non_field_errors':
                                        ["Email or password is not valid"]}},
                            status.HTTP_404_NOT_FOUND)
        # return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get(self, request, format=None):
        print("Request", request.user)
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserChangePassword(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def post(self, request, format=None):
        serializer = ChangePasswordSerializer(
            data=request.data, context={'user': request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({"msg": "Password Changed Succesfully"},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]
    serializer_class = SendPasswordResetEmailSerializer

    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({"msg": "Password Reset Email Sent Succesfully"},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    renderer_classes = [UserRenderer]
    serializer_class = ResetPasswordSerializer

    def post(self, request, uid, token, format=None):
        serializer = ResetPasswordSerializer(data=request.data, context={
                                             'uid': uid, 'token': token})
        if serializer.is_valid(raise_exception=True):
            return Response({"msg": "Password Reset Succesfully"},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmail(APIView):
    serializer_class = EmailVerificationSerializer

    @extend_schema(
        parameters=[
            EmailVerificationSerializer,
            # serializer fields are converted to parameters
        ],
        # more customizations
    )
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = AccessToken(token)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': e.__str__()},
                            status=status.HTTP_401_UNAUTHORIZED)
