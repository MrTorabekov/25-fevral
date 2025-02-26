from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiParameter, extend_schema, OpenApiResponse
from rest_framework import status, generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from apps.admin import Address, Brand, Category
from apps.models import Review, Product, Supplier, Order, Wishlist, ProductImage, Comment, CartItem, Deal
from apps.serializers import RegisterSerializer, LoginSerializer, UserSerializer, AddressSerializer, BrandSerializer, \
    CategorySerializer, ProductSerializer, ProductImageSerializer, ReviewSerializer, SupplierSerializer, \
    OrderSerializer, WishlistSerializer, CommentSerializer, CartItemSerializer, DealSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginApiView(APIView):
    @extend_schema(
            summary='User Login',
            description='Login using email and password to obtain JWT tokens',
            request=LoginSerializer,
            responses={
                200: OpenApiParameter(name='Tokens', description='JWT access and refresh tokens'),
                400: OpenApiParameter(name='Errors', description='Invalid credentials or validation errors')
            },
            tags=['User Authentication']
    )
    def post(self, request):
        serializer = LoginSerializer(data = request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            user = User.objects.get(email = email)
            if user.check_password(password):
                if not user.is_active :
                    return Response({'detail': 'User is anactive'}, status=status.HTTP_400_BAD_REQUEST)
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                return Response({
                    'refresh': str(refresh),
                    'access': access_token
                }, status=status.HTTP_200_OK)
        else:
            return Response({"detail": 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)

class RegisterApiView(APIView):
    @extend_schema(
        summary='User Register',
        description='Register using email and password to obtain JWT tokens',
        request=RegisterSerializer,
        responses={
            201: OpenApiResponse(description="JWT access and refresh tokens"),
            400: OpenApiResponse(description="Invalid credentials or validation errors"),
        },
        tags=['User Authentication']
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            print("Validated data:", serializer.validated_data)  # 🔍 DEBUG
            if 'password' not in serializer.validated_data:
                return Response({"error": "Password field is missing"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = serializer.save()
                user.set_password(serializer.validated_data['password'])
                user.save()

                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'user': RegisterSerializer(user).data
                    }, status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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

class CategoryAPI(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

class ProductAPI(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)  # Har xil formatlarni qo‘llab-quvvatlash

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        print("Received data:", request.data)  # Debug uchun
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=ProductSerializer,
        responses={200: "Product deleted successfully"}
    )
    def delete(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            # ❗ Faqat mahsulot egasi o‘chirishi mumkin
            if product.user != request.user:
                return Response({"error": "You do not have permission to delete this product"},
                                status=status.HTTP_403_FORBIDDEN)
            product.delete()
            return Response({"message": "Product deleted"}, status=status.HTTP_204_NO_CONTENT)

        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

class ProductUpdateAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]


    @extend_schema(
        summary="Product Update",
        description="Product update data",
        request=ProductSerializer,  # Specify request body fields
        responses={
            200: OpenApiParameter(name="Update", description="Product update data"),
            400: OpenApiParameter(name="Errors", description="Invalid credentials or validation errors"),
        },
        tags=["Product Update"]
    )
    def put(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=400)

class ProductImageAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get(self, request):
        products = ProductImage.objects.all()
        serializer = ProductImageSerializer(products, many=True)
        return Response(serializer.data)

class ReviewAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary='Review',
        description='Enter Review',
        request=ReviewSerializer,
    )

    def post(self, request, *args, **kwargs):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SuplierCreateAPIView(APIView):
    def get(self, request):
        suppliers = Supplier.objects.all()
        serializer = SupplierSerializer(suppliers, many=True)
        return Response(serializer.data)

    @extend_schema(
            summary='Supplier',
            description='Enter supplier',
            request=SupplierSerializer
    )

    def post(self, request):
        serializer = SupplierSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SuplierDetailAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        try:
            supplier = Supplier.objects.get(user=request.user, pk=pk)
        except Supplier.DoesNotExist:
            return Response({'error': 'Supplier not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = SupplierSerializer(supplier)
        return Response(serializer.data)

    def delete(self, request, pk):
        try:
            supplier = Supplier.objects.get(user=request.user, pk=pk)
            if supplier.user != request.user:
                return Response({"error": "You do not have permission to delete this supplier"},)
            supplier.delete()
            return Response({"message": "Supplier deleted"}, status=status.HTTP_204_NO_CONTENT)
        except Supplier.DoesNotExist:
            return Response({"error": "Supplier not found"}, status=status.HTTP_404_NOT_FOUND)

class OrderListView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary='Order',
        description='Enter Orders',
        request=OrderSerializer
    )

    def post(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, pk):
        try:
            order = Order.objects.get(user=request.user, pk=pk)
            if order.user != request.user:
                return Response({"error": "You do not have permission to delete this order"},)
            order.delete()
            return Response({"message": "Order deleted"}, status=status.HTTP_204_NO_CONTENT)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

class WishlistListCreateView(generics.ListCreateAPIView):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]

class CommentListAPIView(APIView):

    def get(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary='Comment',
        description='Enter Comment',
        request=CommentSerializer
    )
    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDetailView(APIView):

    def get_object(self, pk):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            return None

    def delete(self, request, pk):
        comment = self.get_object(pk)
        if comment is None:
            return Response({"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)
        comment.delete()
        return Response({"message": "Comment deleted"}, status=status.HTTP_204_NO_CONTENT)

class CartItemListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart_items = CartItem.objects.filter(user=request.user)
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CartItemDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk, user):
        return get_object_or_404(CartItem, pk=pk, user=user)

    def get(self, request, pk):
        cart_item = self.get_object(pk, request.user)
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)

    def put(self, request, pk):
        cart_item = self.get_object(pk, request.user)
        serializer = CartItemSerializer(cart_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        cart_item = self.get_object(pk, request.user)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class DealAPIView(APIView):

    def get(self, request):
        deal = Deal.objects.all()
        serializer = DealSerializer(deal, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary='Deal',
        description="Enter Deal",
        request=DealSerializer
    )


    def post(self, request):
        serializer = DealSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)