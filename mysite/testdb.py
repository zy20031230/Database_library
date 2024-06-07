from django.http import HttpResponse
from demo.models import Test,Book
def testdb(request):
    test1 = Test(name='runoob')
    test1.save()
    return HttpResponse("<p>数据添加成功！</p>")
def booktest(request):
    book = Book.objects.create(
        abstract='数据库前端实践',
        author='张三',
        bookname='编程入门',
        book_type='编程',
        ISBN='1234567890',
        num=10
    )
    book.save()
    return HttpResponse("<p>数据添加成功！</p>")