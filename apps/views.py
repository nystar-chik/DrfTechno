from django.shortcuts import render
from rest_framework.views import APIView
from apps.models import Product, Category, Characteristics
from apps.serializer import ProductSerializer, CategorySerializer, CharacteristicsSerializer, ProductCreateUpdateSerializer
from rest_framework.response import Response
from rest_framework import status
from apps.paginator import ProductPaginator
from rest_framework import generics, viewsets 
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from apps import mixins
from rest_framework.decorators import action


class ProductViewSet(mixins.ProProductViewSet):
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = ProductPaginator
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['title', 'category']
    search_fields = ['title']
    ordering_fields = ['price']

    serializer_classes = {
        'list': ProductSerializer,
        'create': ProductCreateUpdateSerializer,
        'update': ProductCreateUpdateSerializer,
    }

    permission_classes_by_action = {
        'list': [IsAuthenticated],
        'retrieve': [AllowAny],
        'create': [IsAuthenticated],
        'update': [IsAuthenticated],    
        'delete': [IsAdminUser]
    }   

    @action(detail=False, methods=['get'])
    def sum(self, request):
        products = self.get_queryset()
        total = 0
        for i in products:
            total += i.price

        return Response({'count': len(products), 'sum' : total})
    
    @action(detail=False, methods=['get'], serializer_class=ProductSerializer)
    def expensive(self, request):
        products = Product.objects.order_by('-price').first()
        serializer = self.get_serializer(products)
        return Response({'the most expensive product' : serializer.data})
    
    @action(detail=False, methods=['get'], serializer_class=ProductSerializer)
    def cheap(self, request):
        products = Product.objects.order_by('price').first()
        serializer = self.get_serializer(products)
        return Response({'the most expensive product' : serializer.data})

    @action(detail=False, methods=['get'], serializer_class=ProductSerializer)
    def my_products(self, request):
        product = Product.objects.filter(user=request.user)

        serializer = self.get_serializer(product, many=True)

        return Response(serializer.data)


    
                

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CharacteristicsViewSet(viewsets.ModelViewSet):
    queryset = Characteristics.objects.all()
    serializer_class = CharacteristicsSerializer

# class ProductViewSet(viewsets.ViewSet):
#     def list(self, request):
#         products = Product.objects.all()
#         paginator = ProductPaginator()
#         page = paginator.paginate_queryset(products, request)
#         serializer = ProductSerializer(page, many=True)
#         return paginator.get_paginated_response(serializer.data)
    
#     def retrieve(self, request, pk):
#         products = Product.objects.all()
#         product = get_object_or_404(products, pk=pk)
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
    
#     def create(self, request):
#         serializer = ProductSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#         return Response(serializer.data)

#     def update(self, request, pk):
#         product = Product.objects.get(pk=pk)
#         serializer = ProductSerializer(product, data=request.data)
#         if serializer.is_valid():
#             serializer.save()      
#         return Response(serializer.data)
    
#     def partial_update(self, request, pk):
#         product = Product.objects.get(pk = pk)
#         serializer = ProductSerializer(product, data = request.data, partial = True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status.HTTP_200_OK)
#         return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
#     def destroy(self, request, pk):
#         product = Product.objects.get(pk=pk)
#         product.delete()
#         return Response({'message':'Product was deleted'}, status=status.HTTP_204_NO_CONTENT)
    

# class CategoryViewSet(viewsets.ViewSet):
#     def list(self, request):
#         categorys = Category.objects.all()
#         paginator = ProductPaginator()
#         page = paginator.paginate_queryset(categorys, request)
#         serializer = CategorySerializer(page, many=True)
#         return paginator.get_paginated_response(serializer.data)
    
#     def retrieve(self, request, pk):
#         categorys = Category.objects.all()
#         product = get_object_or_404(categorys, pk=pk)
#         serializer = CategorySerializer(product)
#         return Response(serializer.data)
    
#     def create(self, request):
#         serializer = CategorySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#         return Response(serializer.data)

#     def update(self, request, pk):
#         categorys = Category.objects.get(pk=pk)
#         serializer = CategorySerializer(categorys, data=request.data)
#         if serializer.is_valid():
#             serializer.save()      
#         return Response(serializer.data)
    
#     def partial_update(self, request, pk):
#         categorys = Category.objects.get(pk = pk)
#         serializer = CategorySerializer(categorys, data = request.data, partial = True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status.HTTP_200_OK)
#         return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
#     def destroy(self, request, pk):
#         product = Category.objects.get(pk=pk)
#         product.delete()
#         return Response({'message':'Category was deleted'}, status=status.HTTP_204_NO_CONTENT)


# class CharacteristickViewSet(viewsets.ViewSet):
#     def list(self, request):
#         categorys = Characteristics.objects.all()
#         paginator = ProductPaginator()
#         page = paginator.paginate_queryset(categorys, request)
#         serializer = CharacteristicsSerializer(page, many=True)
#         return paginator.get_paginated_response(serializer.data)
    
#     def retrieve(self, request, pk):
#         categorys = Characteristics.objects.all()
#         product = get_object_or_404(categorys, pk=pk)
#         serializer = CharacteristicsSerializer(product)
#         return Response(serializer.data)
    
#     def create(self, request):
#         serializer =CharacteristicsSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#         return Response(serializer.data)

#     def update(self, request, pk):
#         categorys = Characteristics.objects.get(pk=pk)
#         serializer = CharacteristicsSerializer(categorys, data=request.data)
#         if serializer.is_valid():
#             serializer.save()      
#         return Response(serializer.data)
    
#     def partial_update(self, request, pk):
#         categorys = Characteristics.objects.get(pk = pk)
#         serializer = CharacteristicsSerializer(categorys, data = request.data, partial = True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status.HTTP_200_OK)
#         return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
#     def destroy(self, request, pk):
#         product = Characteristics.objects.get(pk=pk)
#         product.delete()
#         return Response({'message':'Category was deleted'}, status=status.HTTP_204_NO_CONTENT)




# class ProductGenerics(generics.ListCreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     pagination_class = ProductPaginator
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['title', 'category']

# class ProductdetailGenerics(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     pagination_class = ProductPaginator



# class CategoryGenerics(generics.ListCreateAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     pagination_class = ProductPaginator

# class CategorydetailGenerics(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     pagination_class = ProductPaginator



# class CharacteristicGenerics(generics.ListCreateAPIView):
#     queryset = Characteristics.objects.all()
#     serializer_class = CharacteristicsSerializer
#     pagination_class = ProductPaginator

# class CharacteristicdetailGenerics(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Characteristics.objects.all()
#     serializer_class = CharacteristicsSerializer
#     pagination_class = ProductPaginator


# class ProductAPIView(APIView):
#     def get(self, request):
#         product = Product.objects.all()
#         paginator = ProductPaginator()
#         page = paginator.paginate_queryset(product, request)
#         serializer = ProductSerializer(page, many=True)
#         return paginator.get_paginated_response(serializer.data)

#     def post(self, request):
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=201)
    

# class ProductDetailAPIView(APIView):
#     def get(self, request, id):
#         product = Product.objects.get(id=id)
#         serializer = ProductSerializer(product)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     def put(self, request, id): 
#         product = Product.objects.get(id=id)
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
#     def patch(self, request, id): 
#         product = Product.objects.get(id=id)
#         serializer = ProductSerializer(product, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
#     def delete(self, request, id):
#         product = Product.objects.get(id=id)
#         product.delete()
#         return Response(status=status.HTTP_202_ACCEPTED)

    
# class CategoryAPIView(APIView):
#     def get(self, request):
#         product = Category.objects.all()
#         paginator = ProductPaginator()
#         page = paginator.paginate_queryset(product, request)
#         serializer = CategorySerializer(page, many=True)
#         return paginator.get_paginated_response(serializer.data)

#     def post(self, request):
#         serializer = CategorySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#         return Response(serializer.data, status=201)


# class CategoryDetailAPIView(APIView):
#     def get(self, request, id):
#         product = Category.objects.get(id=id)
#         serializer = CategorySerializer(product)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     def put(self, request, id): 
#         product = Category.objects.get(id=id)
#         serializer = CategorySerializer(product, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
#         return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

#     def patch(self, request, id): 
#         product = Category.objects.get(id=id)
#         serializer = CategorySerializer(product, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
#         return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self, request, id):
#         product = Category.objects.get(id=id)
#         product.delete()
#         return Response(status=status.HTTP_202_ACCEPTED)



# class CharacteristicsAPIView(APIView):
#     def get(self, request):
#         product = Characteristics.objects.all()
#         serializer = CharacteristicsSerializer(product, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = CharacteristicsSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#         return Response(serializer.data, status=201)
    


# class CharacteristicsDetailAPIView(APIView):
#     def get(self, request, id):
#         product = Characteristics.objects.get(id=id)
#         serializer = CharacteristicsSerializer(product)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     def put(self, request, id): 
#         product = Characteristics.objects.get(id=id)
#         serializer = CharacteristicsSerializer(product, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
#         return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

#     def patch(self, request, id): 
#         product = Characteristics.objects.get(id=id)
#         serializer = CharacteristicsSerializer(product, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
#         return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self, request, id):
#         product = Characteristics.objects.get(id=id)
#         product.delete()
#         return Response(status=status.HTTP_202_ACCEPTED)
