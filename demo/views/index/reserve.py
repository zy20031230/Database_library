from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.hashers import make_password, check_password  # 用户密码管理
from django.utils import timezone  # django带时区管理的时间类
from demo.models import User,Book,Review, UserViolation,Reservation,BorrowingRecord
from datetime import datetime, timedelta
from demo.views.index.hello_world import vio_type, pre_check
from django.db.models import Case, When, Value, IntegerField

def person_init(request):
    # print('hll')
    # print(request.session.get('user_id'))
    if not request.session.get('user_type'):
        return redirect('demo:login')
    pre_check(request)
    context = {}
    user_id = request.session.get('user_id')
    user_id = User.objects.get(user_id=user_id).id
    # 获得user_id 正在预定的书籍
    reserve_books = Reservation.objects.filter(user_id=user_id)
    context['reserve_books'] = reserve_books
    # 或者借书情况，同时没还的书排在最上面,还了的书按照归还时间排序
    borrow_books = BorrowingRecord.objects.filter(user_id=user_id).annotate(
        if_return = Case(
            When(return_date__isnull=True,then=0),
            default=1,
            output_field=IntegerField()
        )
    ).order_by('if_return','return_date')
    context['borrow_books'] = borrow_books

    # 查看是否有违规记录
    vio_books = UserViolation.objects.filter(user_id=user_id)
    context['vio_books'] = vio_books
    

    return render(request,'Person.html',context=context)
    # if reserve_books.exists():
        # 从BOOK中获取书籍的信息
        



    # return HttpResponse(f'{request.session.get("user_id")}')
    # return render(request,'Person.html')
    # if request.session.get('user_type') == 'student':
        # return redirect('demo:login')
            
        # pre_check(request)
def reserve_cancel(request,book_id):
    user_id = request.session.get('user_id')
    user_id = User.objects.get(user_id=user_id).id

    # 查询
    reserve_book = Reservation.objects.get(user_id=user_id,book_id=book_id)
    book_ = reserve_book.book
    book_.num += 1
    book_.save()
    reserve_book.delete()
    return HttpResponse('取消预定成功')

def borrow_book(request,book_id):

    user_id = request.session.get('user_id')
    user_id = User.objects.get(user_id=user_id).id
    # 查询
    reserve_book = Reservation.objects.get(user_id=user_id,book_id=book_id)
    borrow_ = BorrowingRecord(user_id=user_id,book_id=book_id,borrow_date=timezone.now(),due_date=timezone.now()+timedelta(days=30))
    borrow_.save()
    reserve_book.delete()
    return HttpResponse('借阅成功')

def return_book(request,book_id):
    user_id = request.session.get('user_id')
    user_id = User.objects.get(user_id=user_id).id
    now_time = timezone.now()
    # 查询
    borrow_book = BorrowingRecord.objects.get(user_id=user_id,book_id=book_id,return_date__isnull=True)
    borrow_book.return_date = now_time
    # borrow_book.save()
    # 查看是否超时
    if borrow_book.due_date < now_time:
        # 超时
        user_vio = UserViolation(user_id=user_id,book_id=book_id,borrow_date=borrow_book.borrow_date,due_date=borrow_book.due_date,return_date=now_time,violation_description="超时归还,请咨询管理员罚款情况")
        user_vio.save()
    borrow_book.save()
    # 增加书库数量
    book_ = Book.objects.get(id=book_id)
    book_.num += 1
    book_.save()
    return HttpResponse('归还成功')



def logout(request):
    if request.session.get('user_type',None):
        request.session.flush()
    return redirect('demo:login')

def reserve_book(request,book_id):
    if request.session.get('user_type') != 'student':
        return redirect('demo:login')
    user_id = request.session.get('user_id') # 从user中获取user_name 对应的id
    user_id = User.objects.get(user_id=user_id).id
    # 查询
    pre_check(request)
    status = request.session.get('user_status')
    # reserve_book_num_check(request)
    if status and status != 0:
        return vio_type(request)
    # 查看书库，这本书的数量是否大于0
    book = Book.objects.get(id=book_id)
    if book.num <= 0:
        return HttpResponse('这本书已经被预定完了')
    # 查看自己是否预定了这本书
    if Reservation.objects.filter(user_id=user_id,book_id=book_id).exists():
        return HttpResponse('你已经预定了这本书')
    # 查看自己是否借阅了这本书
    if BorrowingRecord.objects.filter(user_id=user_id,book=book_id,return_date__isnull=True).exists():
        return HttpResponse('你已经借阅了这本书')
    # 处理预定
    reservation = Reservation(user_id=user_id,book_id=book_id,status=0)
    reservation.save()
    book.num -= 1
    book.save()
    return HttpResponse('预定成功')
    
    
        
