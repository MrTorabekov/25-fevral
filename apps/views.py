from django.contrib.auth.hashers import make_password
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics
from .models import Wishlist
from .serializers import WishlistSerializer
from apps.admin import Address, Brand, Category, Product
from apps.serializers import RegisterSerializer, LoginSerializer, UserSerializer, AddressSerializer, BrandSerializer, \
    CategorySerializer, ProductSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


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
    @extend_schema(
        summary="User Registration",
        description="Register a new user with username, email, password, and role.",
        request=RegisterSerializer,  # Specify request body serializer
        responses={
            201: OpenApiParameter(name="Tokens", description="JWT access and refresh tokens"),
            400: OpenApiParameter(name="Errors", description="Validation errors")
        },
        tags=["User Registration"]
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(password=make_password(serializer.validated_data['password']))
            # Generate JWT tokens

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                "refresh": str(refresh),
                "access": access_token,
            }, status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserUpdateView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]  # Faqat autentifikatsiyalangan user

    @extend_schema(
        request=UserSerializer,
        responses={200: "User updated successfully"}
    )
    def put(self, request, pk):
        if request.user.id != pk:
            return Response(
                {"detail": "Siz faqat o'z profilingizni yangilashingiz mumkin."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = UserSerializer(instance=request.user, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryAPI(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories)
        return Response(serializer.data)


class ProductAPI(APIView):
    parser_classes = (MultiPartParser, FormParser)

    @extend_schema(
        request=ProductSerializer,
        responses={200: "Product create successfully"}
    )
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddressListCreateAPIView(APIView):
    """
    GET - Address ro'yxatini olish
    POST - Yangi Address qo'shish
    """

    def get(self, request):
        addresses = Address.objects.all()
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddressDetailAPIView(APIView):
    """
    GET - Bitta Address ma'lumotlarini olish
    PUT - Address ma'lumotlarini yangilash
    DELETE - Addressni o'chirish
    """

    def get_object(self, pk):
        try:
            return Address.objects.get(pk=pk)
        except Address.DoesNotExist:
            return None

    def get(self, request, pk):
        address = self.get_object(pk)
        if address is None:
            return Response({"error": "Address not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = AddressSerializer(address)
        return Response(serializer.data)

    def put(self, request, pk):
        address = self.get_object(pk)
        if address is None:
            return Response({"error": "Address not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = AddressSerializer(address, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        address = self.get_object(pk)
        if address is None:
            return Response({"error": "Address not found"}, status=status.HTTP_404_NOT_FOUND)
        address.delete()
        return Response({"message": "Address deleted"}, status=status.HTTP_204_NO_CONTENT)


class BrandAPI(APIView):
    def get(self, request):
        brands = Brand.objects.all()
        serializer = BrandSerializer(brands, many=True)
        return Response(serializer.data)


class WishlistListCreateView(generics.ListCreateAPIView):
    queryset = Wishlist.objects.all()  # Hamma wishlistlar chiqadi
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]

