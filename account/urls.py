from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = "account"

urlpatterns = [
    path('loginRegister/', views.loginRegister, name='loginRegister'),
    # 登录注册页
    path('logout/', auth_views.LogoutView.as_view(template_name='account/logout.html'), name='logout'),
    # 注销
    path('forgetPassword/', views.forgetPassword, name='forgetPassword'),
    # 忘记密码

    path('', views.account, name='account'),
    # 个人中心模块
    path('personalCenter/', views.personalCenter, name='personalCenter'),
    # 个人中心首页
    path('changeInformation/', views.changeInformation, name='changeInformation'),
    # 修改信息
    path('changePassword/', views.changePassword, name='changePassword'),
    # 修改密码
    path('changeEmail/', views.changeEmail, name='changeEmail'),
    # 修改邮箱
    path('historyBrowse/', views.historyBrowse, name='historyBrowse'),
    # 浏览记录
    path('historyLike/', views.historyLike, name='historyLike'),
    # 收藏记录
    path('historyComment/', views.historyComment, name='historyComment'),
    # 评论记录
    path('historyLeave/', views.historyLeave, name='historyLeave'),
    # 留言记录

    path('tableData', views.tableData, name='tableData'),
    # ajax动态表格数据
    path('tableSearch', views.tableSearch, name='tableSearch'),
    # ajax动态表格搜索
    path('tableForm', views.tableForm, name='tableForm'),
    # ajax动态表格表单

    path('registerCheck', views.registerCheck, name='registerCheck'),
    # ajax用户注册信息验证
    path('imageUpload/', views.imageUpload, name='imageUpload'),
    # ajax图片上传接口(头像 文章封面)
    path('commentUpload/', views.commentUpload, name='commentUpload'),
    # ajax评论图片上传
    path('markdownUpload/', views.markdownUpload, name='markdownUpload'),
    # ajax markdown图片上传
    path('emailCode/', views.emailCode, name='emailCode'),
    # ajax获取邮件验证码
    path('checkEmailCode/', views.checkEmailCode, name='checkEmailCode'),
    # ajax校验邮件验证码
    path('bindEmail/', views.bindEmail, name='bindEmail'),
    # ajax绑定邮箱
]
