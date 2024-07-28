from django.urls import path
from products.api import (
    ItemListView,
    CreateItem,
)

urlpatterns = [
    path('item/', ItemListView.as_view(), name='product-list'),
    path('item/create/' ,CreateItem.as_view() , name = 'product-create'),
    path('item/<int:pk>/', CreateItem.as_view(), name='item-detail'),
    path('item/<int:pk>/delete/', CreateItem.as_view(), name='item-detail'),
    
    # path('<pk>/', ItemDetailView.as_view(), name='product-detail'),
]