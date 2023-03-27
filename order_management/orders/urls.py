from django.urls import path
from . import views
from .views import OrdersListView,OrdersDetailView,OrdersCreateView,OrdersUpdateView,OrdersDeleteView

urlpatterns = [
    path('', OrdersListView.as_view(), name='orders-home'),
    path('orders/<int:pk>/', OrdersDetailView.as_view(), name='orders-detail'),
    path('orders/<int:pk>/update/', OrdersUpdateView.as_view(), name='orders-update'),
    path('favourite_add/<int:id>/', views.favourite_add, name='favourite-add'),
    path('orders/<int:pk>/delete/', OrdersDeleteView.as_view(), name='orders-delete'),
    path('order/new/', OrdersCreateView.as_view(), name='order-create'),
    path('favourite_list/', views.favourite_list, name='favourite-list'),
    path('about/', views.about, name='orders-about'),
    path ('tags/<slug:tags_slug>/', views.TagIndex.as_view(),name='posts_by_tag'),
    path('tag_search/', views.search_tag, name='tag-search'),
]