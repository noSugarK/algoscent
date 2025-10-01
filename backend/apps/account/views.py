from datetime import timedelta

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.throttling import UserRateThrottle
from django.contrib.auth import login, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.http import JsonResponse
from django.views import View

import os
from apps.users.models import USER
from apps.account.serializers import UserDetailSerializer, PasswordResetSerializer
from apps.account.utils import decrypt_with_private_key


class LoginThrottle(UserRateThrottle):
    rate = '5/min'
    scope = 'login'

class GetPublicKeyView(View):
    def get(self, request):
        key_path = os.path.join(os.path.dirname(__file__), '../account/keys', 'public_key.pem')
        with open(key_path, 'r') as f:
            public_key = f.read()
        return JsonResponse({'public_key': public_key})

class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        encrypted_username = request.data.get('username')
        encrypted_password = request.data.get('password')
        remember_me = request.data.get('remember_me', False)

        if not encrypted_username or not encrypted_password:
            return Response({'detail': '缺少参数'}, status=400)

        try:
            # 🔐 解密
            username = decrypt_with_private_key(encrypted_username)
            password = decrypt_with_private_key(encrypted_password)
        except Exception as e:
            return Response({'detail': '解密失败'}, status=400)

        # 此时 username 和 password 是明文
        # 使用 Django 默认认证
        user = authenticate(username=username, password=password)
        if not user:
            return Response({'detail': '用户名或密码错误'}, status=401)

        login(request, user)

        refresh = RefreshToken.for_user(user)
        # 设置 access token 过期时间
        refresh.access_token.set_exp(lifetime=timedelta(hours=1 if not remember_me else 7*24))

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserDetailSerializer(user).data
        })

class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"detail": "无效令牌"}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetUsernameCheckView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    def post(self, request):
        username = request.data.get('username')
        if not username:
            return Response({"username": "用户名是必填项"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = USER.objects.get(username=username, is_active=True)
            return Response({"valid": True}, status=status.HTTP_200_OK)
        except USER.DoesNotExist:
            return Response({"valid": False}, status=status.HTTP_200_OK)


class PasswordResetEmailCheckView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        
        if not username or not email:
            return Response({"detail": "用户名和邮箱都是必填项"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = USER.objects.get(username=username, email=email, is_active=True)
            return Response({"valid": True}, status=status.HTTP_200_OK)
        except USER.DoesNotExist:
            return Response({"valid": False}, status=status.HTTP_200_OK)


class PasswordResetView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        user = USER.objects.get(email=email, is_active=True)

        # 生成重置链接
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_url = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"

        # 发送邮件
        send_mail(
            subject="重置您的密码",
            message=f"点击链接重置密码: {reset_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

        return Response({"message": "密码重置邮件已发送"}, status=status.HTTP_200_OK)

def force_text(s):
    if isinstance(s, bytes):
        return s.decode('utf-8')
    return str(s)

class PasswordResetValidateView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    def post(self, request):
        uid = request.data.get('uid')
        token = request.data.get('token')

        if not uid or not token:
            return Response({'valid': False}, status=200)

        try:
            uid_pk = force_text(urlsafe_base64_decode(uid))
            user = USER.objects.get(pk=uid_pk)
        except (USER.DoesNotExist, ValueError):
            return Response({'valid': False}, status=200)

        if default_token_generator.check_token(user, token):
            return Response({'valid': True}, status=200)
        else:
            return Response({'valid': False}, status=200)

class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    def post(self, request):
        uid = request.data.get('uid')
        token = request.data.get('token')
        new_password = request.data.get('new_password')

        if not uid or not token or not new_password:
            return Response({'message': '参数缺失'}, status=400)

        try:
            uid_pk = force_text(urlsafe_base64_decode(uid))
            user = USER.objects.get(pk=uid_pk)
        except (USER.DoesNotExist, ValueError):
            return Response({'message': '链接无效'}, status=400)

        if not default_token_generator.check_token(user, token):
            return Response({'message': '链接已过期或无效'}, status=400)

        # 设置新密码
        user.set_password(new_password)
        user.save()

        return Response({'message': '密码已重置，请使用新密码登录'})