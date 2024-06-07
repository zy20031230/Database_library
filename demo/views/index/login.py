from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password  # 用户密码管理
from django.utils import timezone  # django带时区管理的时间类
from demo.models import User,Book
from demo.forms import UserForm
def login_view(request):  # 读者、管理员用户登录
# 前端本质上是在同一个图的不同图chen中操作
    context = dict()
    context["msg"] = "error"
    print("hll-----------------------------")
    # return render(request, 'load.html', context=context)
    if request.method == 'GET':
        context["username"] = username = request.GET.get("username")
        password = request.GET.get("password")
        if not username:
            context["msg"] = "请输入邮箱、读者id或图书管理员工号"
            return render(request, 'load.html', context=context)
        context["userid"] = username
        if not password:
            context["msg"] = "密码不能为空"
            return render(request, 'load.html', context=context)
        
        if 'root' in username:
            return HttpResponseRedirect('tobedone')
        else: # 读者登录
            result = User.objects.filter(user_id=username)
            print(type(password))
            print(check_password(password, result[0].password))
            if result.exists() and check_password(password, result[0].password):
                context["books"] = Book.objects.all()
                request.session['user_id'] = result[0].user_id
                request.session['username'] = result[0].name
                request.session['user_type'] = 'student'
                return redirect('demo:home')
            else:
                context["msg"] = "用户名或密码错误"
                return render(request, 'load.html', context=context)

        
def register(request):
    # return HttpResponseRedirect('tobedone')
    context = {}
    if request.method == 'GET':
        return render(request, 'register.html', context=context)
    elif request.method == 'POST':
        # pass
        user_id = request.POST.get("userid")
        # print(user_id)
        # 检查是否有重复的user_id
        username = request.POST.get("username")
        nickname = request.POST.get("nickname")
        password = request.POST.get("password")
        # relation_phone = request.POST.get("relation_phone")
        contact = request.POST.get("contact")
        confirm_password = request.POST.get("confirm_password")
        # 提交时，还能保持这些信息不变
        context["userid"] = user_id
        context["username"] = username
        context["nickname"] = nickname
        context["contact"] = contact
        context["password"] = password
        # 检查上述信息是否为空
        if not user_id or not username or not nickname or not password or not contact:
            context["msg"] = "请填写完整信息"
            return render(request, 'register.html', context=context)
                
        if User.objects.filter(user_id=user_id):
            context["msg"] = "该用户id已存在"
            return render(request, 'register.html', context=context)
        # 昵称
        if User.objects.filter(name=nickname):
            context["msg"] = "该昵称已存在"
            return render(request, 'register.html', context=context)
        if 'PB' not in user_id:
            context["msg"] = "请输入正确的用户id,包含PB"
            return render(request, 'register.html', context=context)
        if password != confirm_password:
            context["msg"] = "两次密码不一致"
            return render(request, 'register.html', context=context)
        new_user = User(
            user_id=user_id,
            load_name=username,
            name=nickname,
            password=make_password(password),
            relation_phone=contact
        )
        # 保存注册的用户信息
        new_user.save()
        context["msg"] = "注册成功:"+"可通过学号登入"
        return render(request, 'load.html', context=context)

def User_profile(request):
    if not request.session.get('user_type'):
        return redirect('demo:login')
    user_id = request.session.get('user_id')
    user_id = User.objects.get(user_id=user_id).id
    User_ = User.objects.get(id=user_id)
    
        
