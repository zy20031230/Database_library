from django.shortcuts import render
from models import Book  # 假设你的书籍模型的名字是 Book

Book.objects.create(
    abstract='数据库前端实践',
    author='张三',
    bookname='编程入门',
    book_type='编程',
    ISBN='1234567890',
    num=10
)