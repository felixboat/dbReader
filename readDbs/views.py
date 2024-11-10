from django.shortcuts import render

# from .chinook_models import Album
from .models import Book, ChinookAlbum, NorthwindProducts
from django.db.models import Avg, Max, Min
# from .northwind_models import Products


# Create your views here.
def index(request):
    context = {}
    return render(request, 'readDbs/index.html', context)

def book_list_view(request):
    books = Book.objects.all().order_by('-rating')
    num_books = books.count()
    agg_rating = books.aggregate(Avg("rating"), Max('rating'), Min('rating'))
    context = {
        'books': books,
        'num_books': num_books,
        'agg_rating': agg_rating,
    }
    return render(request, 'readDbs/books.html', context)

def product_list_view(request):
    products = NorthwindProducts.objects.using('northwind').all()
    num_prod = products.count()
    context = {
        'products': products,
        'num_prod': num_prod,
    }
    return render(request, 'readDbs/products.html', context)

def album_list_view(request):
    albums = ChinookAlbum.objects.using('chinook').all()
    num_albums = albums.count()
    context = {
        'albums': albums,
        'num_albums': num_albums,
    }
    return render(request, 'readDbs/albums.html', context)
