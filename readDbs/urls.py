from django.urls import path
from .views import index, book_list_view, product_list_view, album_list_view
# from .views import index, book_list_view, product_list_view
# from .views import index, book_list_view, album_list_view

urlpatterns = [
    path('', index, name='index'),
    # path('<int:book_id>/', views.book_detail, name='book_detail') # version1
    # path('<slug:slug>/', views.book_detail, name='book_detail'), # version with slug
    path('booklist', book_list_view, name='book_list_url'),
    path('productlist', product_list_view, name='product_list_url'),
    path('albumlist', album_list_view, name='album_list_url'),
]