from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.serializers import RegisterSerializer, LoginSerializer


class LoginApiView(APIView):
    @extend_schema(
        summary="User Login",
        description="Login using email and password to obtain JWT tokens.",
        request=LoginSerializer,  # Specify request body fields
        responses={
            200: OpenApiParameter(name="Tokens", description="JWT access and refresh tokens"),
            400: OpenApiParameter(name="Errors", description="Invalid credentials or validation errors"),
        },
        tags=["User Authentication"]
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')

            user = User.objects.get(email=email)
            if user.check_password(password):
                if not user.is_active:
                    return Response({"detail": "User account is inactive."}, status=status.HTTP_400_BAD_REQUEST)

                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                return Response({
                    "refresh": str(refresh),
                    "access": access_token,
                }, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid password or email"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class RegisterApiView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(password=make_password(serializer.validated_data['password']))
            #Generate JWT tokens

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response(
                {
                    "refresh": str(refresh),
                    "access": access_token,
                    "user" : serializer.data
                },status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

User = get_user_model()
