from django.shortcuts import render, redirect, reverse,HttpResponse
from apps.user.models import *
from django.views.generic import View
from celery_tasks import tasks
import re
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from django.conf import settings
from django.contrib.auth import authenticate,login,logout
from  django.contrib.auth.decorators import  login_required
from django.utils.decorators import  method_decorator
from util import miminx
# Create your views here.

class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        # 接受数据
        username = request.POST.get('user_name')
        pwd = request.POST.get('pwd')
        cpwd = request.POST.get('cpwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')
        # 进行数据校验
        if not all([username, pwd, email]):
            # 数据不完整
            return render(request, 'register.html', {'errmsg': '数据不完整'})
        # 校验邮箱
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '邮箱格式不一致'})
        if allow != 'on':
            return render(request, 'register.html', {'errmsg': '请同意协议'})
        # 进行业务处理：进行用户注册
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # 用户名不存在
            user = None
        if user:
            # 用户名已存在
            return render(request, 'register.html', {'errmsg': '用户名已存在'})
        user = User.objects.create_user(username, email, pwd)
        user.is_active = 0
        user.save()
        # 发送激活邮件，包含激活链接：/user/active/3
        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {'confirm': user.id}
        res = serializer.dumps( info )
        res=res.decode('utf-8')
        #发邮件
        tasks.send_register_active_email(email, username, res)
        # 激活链接中需要包含用户的身份信息
        return redirect(reverse('goods:index'))
        # 返回应答


class ActiveView(View):
    '''用户激活'''

    def get(self, request, token):
        '''进行用户激活'''
        # 进行解密，获取要激活用户信息
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            res = serializer.loads(token)
            user_id=res['confirm']
            #根据id获取用户信息
            user = User.objects.filter(id=user_id).first()
            user.is_active =1
            user.save()
            #跳转登录页面
            return redirect(reverse('user:login'))
        except SignatureExpired as e:
            #激活链接已过期
            return HttpResponse('激活已过期')

class  LoginView(View):
    '''登录'''
    def  get(self,request):
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')

            check ='checked'
        else:
            username = ''
            check = ''

        return render(request,'login.html',{'username':username,'checked':check })
    def  post(self,request):
        '''登录校验'''
        #接收数据
        username = request.POST.get('username')
        password = request.POST.get('pwd')

        #校验数据
        if not all([username,password]):
            return  render(request,'login.html',{'errmsg':'数据不完整'})
        #业务处理：登录校验
        user = authenticate(username=username,password=password)
        if user :
            if user.is_active:
                #用户已激活
                #记录用户登录状态
                login(request,user)
                #登录后跳转到原先页面
                next_url=request.GET.get('next',reverse('goods:index'))
                #跳转到首页
                response=redirect(next_url)
                #判断是否需要记住用户民
                remember =request.POST.get('remember')
                if remember =='on':
                    #记住用户名
                    response.set_cookie('username',username,max_age=7*24*3600)


                else:
                    response.delete_cookie('username')
                #跳到首页
                return response
            else:
                return render(request, 'login.html', {'errmsg': '账户未激活'})
        else:
            return render(request, 'login.html', {'errmsg': '账户不存在'})
        #返回应答
#/user
class LoginOut(View):
    '''用户登出界面1'''
    def  get(self,request):
        logout(request)
        return  redirect(reverse('goods:index'))
class UserInfoView(View):
    '''用户中心-信息页'''


    def  get(self,request):
        '''显示'''
        # page = 'user'

        return render(request,'user_center_info.html',{'page':'user'})
# /user/order

class UserOrderView(miminx.LoginRequairMixin,View):
    '''用户中心-订单页'''


    def  get(self,request):
        '''显示'''
        # page = 'order'
        return render(request,'user_center_order.html',{'page':'order'})
# /user/address

class AddressView(View):
    '''用户中心-地址页'''


    def  get(self,request):
        '''显示'''
        # page = 'address'
        return render(request,'user_center_site.html',{'page':'address'})