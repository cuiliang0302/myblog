"""myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from blog import views
from django.views.static import serve
from myblog.settings import MEDIA_ROOT

urlpatterns = [
    re_path('media/(?P<path>.*)', serve, {'document_root': MEDIA_ROOT}, name='media_url'),
    # 媒体资源
    path('', views.index, name='index'),
    # 博客首页
    path('myblog_admin/', admin.site.urls),
    # admin管理页
    path('login/', include('social_django.urls', namespace='social')),
    # 第三方账户登录
    path('account/', include('account.urls', namespace='account')),
    # 个人中心
    path('blog/', include('blog.urls', namespace='blog')),
    # 博客前台
    path('management/', include('management.urls', namespace='management')),
    # 博客后台
    path('captcha', include('captcha.urls')),
    # 验证码
    path('sitemap/', views.siteMap, name='siteMap'),
    # 生成网站地图
]
