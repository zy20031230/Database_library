from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ...models import Book, User, Reservation,BorrowingRecord,UserViolation
from datetime import datetime, timedelta
from django.utils import timezone
# Create your views here.
# demo/views.py
from django.http import HttpResponse
# @login_required
# def 
def vio_type(request):
    status = request.session.get('user_status')
    print(status)
    status_dict = {0:'正常',1:'预定和借阅书超过3',2:'借阅超时'}
    return HttpResponse(status_dict[status])
def pre_check(request):
    if request.session.get('user_id') :
        reserve_num = 0
        user_id = request.session.get('user_id')
        user_id = User.objects.get(user_id=user_id).id
        today = timezone.now()
        if Reservation.objects.filter(user_id=user_id).exists():
            reservation_ = Reservation.objects.filter(user_id=user_id)
            for reservation in reservation_:
                reservation_date = reservation.reservation_date
                if today - reservation_date > timedelta(days=5):
                    book = reservation.book
                    book.num += 1
                    book.save()
                    reservation.delete()
                else:
                    reserve_num += 1

        # 查看当前用户的借阅历史
        borrowing_num = 0
        if BorrowingRecord.objects.filter(user_id=user_id,return_date__isnull=True).exists():
            Borrow_books = BorrowingRecord.objects.filter(user_id=user_id,return_date__isnull=True)
            delete_list = []
            for book in Borrow_books:
                borrowing_num += 1
                if today - book.due_date > timedelta(days=1):
                    request.session['user_status'] = 2
        all_num = reserve_num + borrowing_num
        if all_num > 3:
            request.session['user_status'] = 1
        



def index(request):
    books = Book.objects.all().prefetch_related('review_set')
    context = {'books': books}
    request.session['user_status'] = 0 # 默认是正常状态
    # 用户信息初始化
    # 查询自己的预定记录
    if request.session.get('user_type') == 'student':
        pre_check(request)
    return render(request,'index.html',context)
def load_in(request):
    return render(request,'load.html')

from django import forms

class BookSearchForm(forms.Form):
    q = forms.CharField(label='Search for', max_length=100, required=False)

def book_list(request):
    form = BookSearchForm()
    query = request.GET.get('q')
    if query:
        books = Book.objects.filter(bookname__icontains=query) | Book.objects.filter(author__icontains=query)
    else:
        books = Book.objects.all()
    return render(request, 'book_list.html', {'form': form, 'books': books})