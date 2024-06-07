from django.shortcuts import render
from ...models import Book  # 假设你的书籍模型的名字是 Book

from django.db import connection
from rest_framework.decorators import api_view, authentication_classes

# from myapp import utils
# from myapp.handler import APIResponse
# from myapp.models import Classification, Book, Tag, User
# from myapp.serializers import BookSerializer, ClassificationSerializer, ListBookSerializer, DetailBookSerializer
# from myapp.utils import dict_fetchall
from django.http import HttpResponse
from django.db.models import Q
# def book_view(request):
#     search = request.GET.get('search', '')
#     books = Book.objects.filter(bookname__icontains=search)
#     return render(request, 'book.html', {'books': books})

def show(request):
    books = Book.objects.all()
    return render(request, 'book.html', {'books': books})

def book_search(request):
    search = request.GET.get('searchQuery')
    books = Book.objects.filter(Q(bookname__icontains=search)|Q(author__icontains=search)|Q(ISBN__icontains=search)|Q(book_type__icontains=search))
    # books = Book.objects.all()
    # print("hllllllllllll")
    # if 
    if books:
        return render(request, 'book_search.html', {'books': books})
    # return render(request, 'book_search.html', {'books': books})
    else :
        return HttpResponse("No such book")
    # return HttpResponse("fuckyou")

# def book_search_view(request):
#     search = request.GET.get('search', '')
#     books = Book.objects.filter(bookname__icontains=search)
#     return render(request, 'book_search.html', {'books': books})
