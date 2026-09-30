from django.urls import path, include
from apps.views import ProductViewSet, CategoryViewSet, CharacteristicsViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('products', ProductViewSet)
router.register('category', CategoryViewSet)
router.register('characteristics', CharacteristicsViewSet)

print(router.urls)



urlpatterns = [
    path('', include(router.urls)),
    # path('', include(router.urls)),
    # path('', include(router.urls))
    # path('products/', views.ProductViewSet.as_view({'get':'list', 'post':'create'})),
    # path('products/<int:pk>/', views.ProductViewSet.as_view({'get':'retrieve', 'put': 'update', 'patch':'partial_update', 'delete':'destroy'})),
    # path('api/v1/category/', views.CategoryViewSet.as_view({'get':'list', 'post':'create'})),
    # path('api/v1/category/<int:pk>/', views.CategoryViewSet.as_view({'get':'retrieve', 'put': 'update', 'patch':'partial_update', 'delete':'destroy'})),
    # path('api/v1/characteristics/', views.CharacteristickViewSet.as_view({'get':'list', 'post':'create'})),
    # path('api/v1/characteristics/<int:pk>/', views.CharacteristickViewSet.as_view({'get':'retrieve', 'put': 'update', 'patch':'partial_update', 'delete':'destroy'})),
]