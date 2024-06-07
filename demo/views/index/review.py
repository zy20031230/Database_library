from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.hashers import make_password, check_password  # 用户密码管理
from django.utils import timezone  # django带时区管理的时间类
from demo.models import User,Book,Review

def add_review(request,book_id):
    print(f'{book_id}---')

    if request.session.get('user_type') != 'student':
        return redirect('demo:login')
    user_id = request.session.get('user_id') # 从user中获取user_name 对应的id
    user_id = User.objects.get(user_id=user_id).id
    # 查看user是否对其发表评论
    if Review.objects.filter(user_id=user_id,book_id=book_id).exists():
        oldreview = Review.objects.get(user_id=user_id,book_id=book_id)
        # oldreview.comment = request.POST.get('comment')
        rating = int(request.POST.get('rating'))
        if rating <1 or rating > 5:
            return HttpResponse('rating should be between 1 and 5')
        oldreview.rating = rating
        oldreview.comment = request.POST.get('comment')
        oldreview.save()
        return HttpResponse("你已经修改了你的评论")
    else:
        rating = int(request.POST.get('rating'))
        if rating <1 or rating > 5:
            return HttpResponse('rating should be between 1 and 5')
        review = Review(user_id=user_id,book_id=book_id,rating=rating,comment=request.POST.get('comment'))
        review.save()
        return HttpResponse('评论成功')
    # return redirect('demo:login')
    return HttpResponse('tobedone1')
    # pass
def delete_review(request,book_id):
    if request.session.get('user_type') != 'student':
        return redirect('demo:login')
    user_id = request.session.get('user_id') # 从user中获取user_name 对应的id
    user_id = User.objects.get(user_id=user_id).id
    if Review.objects.filter(user_id=user_id,book_id=book_id).exists():
        review = Review.objects.get(user_id=user_id,book_id=book_id)
        review.delete()
        return HttpResponse('删除成功')
    else:
        return HttpResponse('你还没有评论')

    # pass