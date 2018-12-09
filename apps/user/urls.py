"""dailyfreshh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from apps.user import views
from  django.contrib.auth.decorators import  login_required
urlpatterns = [
    url(r'register$',views.RegisterView.as_view(),name='register'),#注册用户
    url(r'^active/(?P<token>.*)$',views.ActiveView.as_view(),name='activeView'),#激活用户
    url(r'^$',login_required(views.UserInfoView.as_view()),name='user'),#用户中心-信息页
    url(r'^login',views.LoginView.as_view(),name='login'),#用户登录
    url(r'^logout',views.LoginOut.as_view(),name='logout'),#登出
    url(r'^order$',views.UserOrderView.as_view(),name='order'),#用户中心-订单页
    url(r'^address$',login_required(views.AddressView.as_view()),name='address'),#用户中心-地址页



]
