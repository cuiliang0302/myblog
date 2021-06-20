import json
import random


import requests
from django.contrib.auth.models import User
from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from social_django.models import UserSocialAuth
from django.core.paginator import Paginator
from django.db.models import Q
from django.forms import model_to_dict
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.utils import timezone
from PIL import Image
from account.forms import *
from account.models import UserInfo, ArticleViewHistory, CommentMessage, LeaveMessage, SectionMessage, \
    SectionViewHistory
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.decorators.csrf import csrf_exempt

from blog.models import Article, Category, Tag, Note, Section, Catalogue
from management.models import Carousel, Link, ImagesConfig
from PIL import Image as ImagePIL, ImageFont, ImageDraw

# 设置邮箱、用户名都可以登录
from management.tools import sendEmail


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            print(e)
            return None


# 登录注册页
def loginRegister(request):
    if request.method == "POST":
        type = request.POST.get('type')
        if type == "登录":
            login_form = LoginForm(request.POST)
            # 创建一个对象，获得post方法提交的数据
            if login_form.is_valid():
                # 验证传入的数据是否合法
                login_data = login_form.cleaned_data
                # 引入字典数据类型，存储用户名和密码
                user = authenticate(username=login_data['user'], password=login_data['password'])
                # 验证账号密码是否正确，正确返回user对象，错误返回null
                if user:
                    # 调用django默认的login方法，实现用户登录
                    login(request, user)
                    # 登录后跳转的页面
                    next_url = request.GET.get("next")
                    if next_url:
                        print(next_url)
                        return HttpResponseRedirect(next_url)
                    else:
                        return HttpResponseRedirect('/')
                else:
                    message = '用户名或密码错误！'
                    hashkey = CaptchaStore.generate_key()
                    image_url = captcha_image_url(hashkey)
                    login_form = LoginForm()
                    register_form = RegisterForm()
                    print(message)
                    return render(request, "account/loginRegister.html", locals())
            else:
                message = '验证码错误！'
                hashkey = CaptchaStore.generate_key()
                image_url = captcha_image_url(hashkey)
                login_form = LoginForm()
                register_form = RegisterForm()
                print(message)
                return render(request, "account/loginRegister.html", locals())
        elif type == "注册":
            register_form = RegisterForm(request.POST)
            # 创建一个对象，获得post方法提交的数据
            if register_form.is_valid():
                register_data = register_form.cleaned_data
                # 校验邮件验证码
                try:
                    session_code = request.session['email_code']
                except KeyError:
                    data = {
                        "code": 0,
                        "msg": "邮件验证码已过期！"
                    }
                    return JsonResponse(data)
                if register_data['email_code'] != session_code:
                    data = {
                        "code": 0,
                        "msg": "邮件验证码错误！"
                    }
                    return JsonResponse(data)
                # 校验通过，创建用户
                username = register_data['username']
                password = register_data['password1']
                email = register_data['email']
                new_user = User.objects.create()
                new_user.username = username
                new_user.set_password(password)
                new_user.email = email
                new_user.save()
                # 创建用户信息表记录
                UserInfo.objects.create(user_id=new_user.id)
                # 创建完用户自动登录
                user = authenticate(username=username, password=password)
                # 调用django默认的login方法，实现用户登录
                login(request, user)
                data = {
                    "code": 1,
                    "msg": "注册成功，自动跳转至首页并登陆！"
                }
                return JsonResponse(data)
            else:
                ErrorDict = register_form.errors
                print(ErrorDict)
                data = {
                    "code": 0,
                    "msg": "请求数据异常！"
                }
                return JsonResponse(data)

    else:
        hashkey = CaptchaStore.generate_key()
        image_url = captcha_image_url(hashkey)
        login_form = LoginForm()
        register_form = RegisterForm()
        return render(request, 'account/loginRegister.html', locals())


# 忘记密码
def forgetPassword(request):
    if request.method == "POST":
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            forget_data = forget_form.cleaned_data
            email = forget_data['email']
            password = forget_data['password1']
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            data = {
                "code": 1,
                "msg": "密码重置成功！"
            }
            return JsonResponse(data)
        else:
            ErrorDict = forget_form.errors
            print(ErrorDict)
            data = {
                "code": 0,
                "msg": "请求数据异常！"
            }
            return JsonResponse(data)

    else:
        forget_form = ForgetForm()
        return render(request, 'account/forgetPassword.html', locals())


# 个人中心模块
@login_required()
def account(request):
    try:
        userinfo = UserInfo.objects.get(user_id=request.user.id)
    except Exception as e:
        print(e)
        userinfo = None
    return render(request, 'layui-mini/base.html', locals())


# 第三方用户头像下载至本地
def downloadPhoto(url):
    # url='http://thirdqq.qlogo.cn/g?b=oidb&k=TGX7Iu5wFlTiasg1VOiaeYMA&s=40&t=1598856813'
    filename = "%s.%s" % (timezone.now().strftime('%Y_%m_%d_%H_%M_%S_%f'), "jpg")
    filepath = 'media/photo/' + filename
    db_path = 'photo/' + filename
    html = requests.get(url)
    with open(filepath, 'wb') as file:
        file.write(html.content)
    file.close()
    return db_path


# 个人中心首页
@login_required()
@xframe_options_exempt
def personalCenter(request):
    try:
        userinfo = UserInfo.objects.get(user_id=request.user.id)
        # print("注册用户登录")
    except Exception as e:
        # 第三方用户
        print(e)
        "第三方用户第一次登录"
        social_user = UserSocialAuth.objects.get(user_id=request.user.id)
        if social_user.provider == 'github':
            # print("github登录")
            UserInfo.objects.create(user_id=request.user.id)
            user = User.objects.get(id=request.user.id)
        else:
            # print("qq 微博登录")
            username = social_user.extra_data['username'].replace(" ", "")
            photo_url = social_user.extra_data['profile_image_url']
            username = social_user.extra_data['username'].replace(" ", "")
            photo_url = social_user.extra_data['profile_image_url']
            sex = social_user.extra_data['gender']
            # print(sex)
            if sex == '女' or sex == 'f':
                sex_id = 2
            else:
                sex_id = 1
            user_info = UserInfo()
            user_info.user_id = request.user.id
            user_info.photo = downloadPhoto(photo_url)
            user_info.sex = sex_id
            user_info.save()
            new_user = User.objects.get(id=request.user.id)
            new_user.username = username
            new_user.save()
            user = new_user
    article_view = ArticleViewHistory.objects.filter(user=request.user).count()
    article_like = ArticleViewHistory.objects.filter(user=request.user).filter(is_like=1).count()
    article_comment = CommentMessage.objects.filter(user=request.user).count()
    section_view = SectionViewHistory.objects.filter(user=request.user).count()
    section_like = SectionViewHistory.objects.filter(user=request.user).filter(is_like=1).count()
    section_comment = SectionMessage.objects.filter(user=request.user).count()
    leave_count = LeaveMessage.objects.filter(user=request.user).count()
    return render(request, 'layui-mini/account/index.html', locals())


# 修改密码
@login_required()
@xframe_options_exempt
def changePassword(request):
    if request.method == "POST":
        change_password_form = ChangePasswordForm(request.POST)
        if change_password_form.is_valid():
            change_password_data = change_password_form.cleaned_data
            old_password = change_password_data['password_old']
            new_password = change_password_data['password1']
            user = authenticate(username=request.user.username, password=old_password)
            # 验证账号密码是否正确，正确返回user对象，错误返回null
            if user:
                user.set_password(new_password)
                user.save()
                return HttpResponseRedirect(reverse('account:logout'))
            else:
                message = "原始密码错误！"
        else:
            message = "表单数据异常！"
        change_password_form = ChangePasswordForm()
        return render(request, 'layui-mini/account/changePassword.html', locals())
    else:
        change_password_form = ChangePasswordForm()
        return render(request, 'layui-mini/account/changePassword.html', locals())


# 修改邮箱
@login_required()
@xframe_options_exempt
def changeEmail(request):
    if request.method == "POST":
        change_email_form = ChangeEmailForm(request.POST)
        if change_email_form.is_valid():
            change_email_data = change_email_form.cleaned_data
            password = change_email_data['password']
            email = change_email_data['email']
            email_code = change_email_data['email_code']
            user = authenticate(username=request.user.username, password=password)
            # 验证账号密码是否正确，正确返回user对象，错误返回null
            if user:
                # 校验邮件验证码
                try:
                    session_code = request.session['email_code']
                except KeyError:
                    message = '验证码过期！'

                if email_code != request.session['email_code']:
                    message = '验证码错误！'
                else:
                    # 验证通过，修改邮箱号
                    user = request.user
                    user.email = email
                    user.save()
                    return HttpResponseRedirect(reverse('account:personalCenter'))
                change_email_form = ChangeEmailForm()
                return render(request, 'layui-mini/account/changeEmail.html', locals())
            else:
                message = "密码错误！"
            change_email_form = ChangeEmailForm()
            return render(request, 'layui-mini/account/changeEmail.html', locals())
        else:
            message = change_email_form.errors
        change_email_form = ChangeEmailForm()
        return render(request, 'layui-mini/account/changeEmail.html', locals())
    else:
        change_email_form = ChangeEmailForm()
        return render(request, 'layui-mini/account/changeEmail.html', locals())


# 修改信息
@login_required()
@xframe_options_exempt
def changeInformation(request):
    userinfo = UserInfo.objects.get(user_id=request.user.id)
    user = User.objects.get(username=request.user)
    if request.method == "POST":
        user_form = UserForm(request.POST)
        userinfo_form = UserInfoForm(request.POST)
        user = User.objects.get(id=request.user.id)
        user.username = request.POST.get("username")
        user.save()
        if userinfo_form.is_valid():
            userinfo_data = userinfo_form.cleaned_data
            userinfo = UserInfo.objects.get(user=request.user.id)
            userinfo.sex = userinfo_data['sex']
            userinfo.phone = userinfo_data['phone']
            userinfo.web = userinfo_data['web']
            userinfo.aboutme = userinfo_data['aboutme']
            photo_url = request.POST.get('photo')
            print(photo_url)
            userinfo.photo = photo_url[photo_url.find('/media/') + 7:]
            userinfo.save()
            data = {
                "code": 1,
                "msg": "修改成功！"
            }
        else:
            data = {
                "code": 0,
                "msg": "修改失败！"
            }
        return JsonResponse(data)
    else:
        username = user.username
        email = user.email
        user_form = UserForm({'username': username, 'email': email})
        sex = userinfo.sex
        phone = userinfo.phone
        web = userinfo.web
        aboutme = userinfo.aboutme
        userinfo_form = UserInfoForm({'sex': sex, 'phone': phone, 'web': web, 'aboutme': aboutme})
        return render(request, 'layui-mini/account/changeInformation.html', locals())


# 浏览记录
@login_required()
@xframe_options_exempt
def historyBrowse(request):
    return render(request, 'layui-mini/account/historyBrowse.html', locals())


# 收藏记录
@login_required()
@xframe_options_exempt
def historyLike(request):
    return render(request, 'layui-mini/account/historyLike.html', locals())


# 评论记录
@login_required()
@xframe_options_exempt
def historyComment(request):
    return render(request, 'layui-mini/account/historyComment.html', locals())


# 留言记录
@login_required()
@xframe_options_exempt
def historyLeave(request):
    return render(request, 'layui-mini/account/historyLeave.html', locals())


# ajax动态数据表格接口
def tableData(request):
    page_index = request.GET.get('page')
    page_limit = request.GET.get('limit')
    page_type = request.GET.get('type')
    user_id = request.user.id
    # 浏览记录
    if page_type == 'browse':
        table_data = ArticleViewHistory.objects.filter(user=user_id)
        lis = []
        for history in table_data:
            data = {}
            data["id"] = history.id
            data["article_id"] = history.article.id
            data["title"] = history.article.title
            data['category'] = history.article.category.name
            data['category_id'] = history.article.category_id
            data['time'] = history.time.strftime("%Y-%m-%d %H:%M:%S")
            tags = history.article.tags.all()
            tags_dict = {}
            for tag in tags:
                tags_dict[tag.id] = tag.name
            data['tags'] = tags_dict
            lis.append(data)
    # 收藏记录
    elif page_type == 'like':
        table_data = ArticleViewHistory.objects.filter(user=user_id).filter(is_like=True)
        lis = []
        for history in table_data:
            data = {}
            data["id"] = history.id
            data["article_id"] = history.article.id
            data["title"] = history.article.title
            data['category'] = history.article.category.name
            data['category_id'] = history.article.category_id
            data['time'] = history.time.strftime("%Y-%m-%d %H:%M:%S")
            tags = history.article.tags.all()
            tags_dict = {}
            for tag in tags:
                tags_dict[tag.id] = tag.name
            data['tags'] = tags_dict
            lis.append(data)
    # 评论记录
    elif page_type == 'comment':
        table_data = CommentMessage.objects.filter(user=user_id)
        lis = []
        for history in table_data:
            data = {}
            data["id"] = history.id
            data["article_id"] = history.article.id
            data["title"] = history.article.title
            data['category'] = history.article.category.name
            data['category_id'] = history.article.category_id
            data['time'] = history.time.strftime("%Y-%m-%d %H:%M:%S")
            data['like'] = history.like
            data['content'] = history.content
            lis.append(data)
    # 留言记录
    elif page_type == 'leave':
        table_data = LeaveMessage.objects.filter(user=user_id)
        lis = []
        for history in table_data:
            data = {}
            data["id"] = history.id
            data['time'] = history.time.strftime("%Y-%m-%d %H:%M:%S")
            data['like'] = history.like
            data['content'] = history.content
            lis.append(data)
    # 文章列表
    elif page_type == 'article_list':
        table_data = Article.objects.all()
        lis = []
        for article in table_data:
            data = {}
            data["id"] = article.id
            data["title"] = article.title
            data["cover"] = article.img.url
            data['created_time'] = article.created_time.strftime("%Y-%m-%d %H:%M:%S")
            data['is_release'] = article.is_release
            data['is_recommend'] = article.is_recommend
            data['category'] = article.category.name
            data['category_id'] = article.category_id
            tags = article.tags.all()
            tags_dict = {}
            for tag in tags:
                tags_dict[tag.id] = tag.name
            data['tags'] = tags_dict
            lis.append(data)
    # 文章分类
    elif page_type == 'article_category':
        table_data = Category.objects.all()
        lis = []
        for category in table_data:
            data = {}
            data["id"] = category.id
            data["name"] = category.name
            data["article_count"] = Article.objects.filter(category_id=category.id).count()
            lis.append(data)
    # 文章标签
    elif page_type == 'article_tag':
        table_data = Tag.objects.all()
        lis = []
        for tag in table_data:
            data = {}
            data["id"] = tag.id
            data["name"] = tag.name
            data["article_count"] = Article.objects.filter(tags=tag.id).count()
            lis.append(data)
    # 文章评论
    elif page_type == 'article_comment':
        table_data = CommentMessage.objects.all()
        lis = []
        for history in table_data:
            data = {}
            data["id"] = history.id
            data["article_id"] = history.article.id
            data["title"] = history.article.title
            data['time'] = history.time.strftime("%Y-%m-%d %H:%M:%S")
            data['user'] = history.user.username
            data['content'] = history.content
            if history.level == 0:
                data['type'] = "评论"
            else:
                data['type'] = "回复"
            lis.append(data)
    # 留言
    elif page_type == 'leave_message':
        table_data = LeaveMessage.objects.all()
        lis = []
        for history in table_data:
            data = {}
            data["id"] = history.id
            data['time'] = history.time.strftime("%Y-%m-%d %H:%M:%S")
            data['user'] = history.user.username
            data['content'] = history.content
            if history.level == 0:
                data['type'] = "留言"
            else:
                data['type'] = "回复"
            lis.append(data)
    # 轮播图管理
    elif page_type == 'carousel':
        table_data = Carousel.objects.all()
        lis = []
        for carousel in table_data:
            data = {}
            data["id"] = carousel.id
            data["info"] = carousel.info
            data["url"] = carousel.url
            data["img"] = carousel.img.url
            data["is_show"] = carousel.is_show
            lis.append(data)
    # 友情链接管理
    elif page_type == 'link':
        table_data = Link.objects.all()
        lis = []
        for link in table_data:
            data = {}
            data["id"] = link.id
            data["logo"] = link.logo.url
            data["name"] = link.name
            data["url"] = link.url
            data["describe"] = link.describe
            data["type"] = link.type
            lis.append(data)
    # 用户管理
    elif page_type == 'user':
        table_data = UserInfo.objects.all()
        lis = []
        for user_info in table_data:
            data = {}
            data["id"] = user_info.user.id
            data["username"] = user_info.user.username
            data["email"] = user_info.user.email
            data["is_active"] = user_info.user.is_active
            data["last_login"] = user_info.user.last_login.strftime("%Y-%m-%d")
            data["date_joined"] = user_info.user.date_joined.strftime("%Y-%m-%d")
            data["photo"] = user_info.photo.url
            data["sex"] = user_info.sex
            try:
                data["source"] = UserSocialAuth.objects.get(user_id=user_info.user.id).provider
            except Exception as e:
                print(e)
                data["source"] = "邮箱注册"
            lis.append(data)
    # 笔记名称
    elif page_type == 'note_name':
        table_data = Note.objects.all()
        lis = []
        for note in table_data:
            data = {}
            data["id"] = note.id
            data["name"] = note.name
            data["section_count"] = Section.objects.filter(note_id=note.id).count()
            lis.append(data)
    # 笔记列表
    elif page_type == 'section_list':
        table_data = Section.objects.all()
        lis = []
        for section in table_data:
            data = {}
            data["id"] = section.id
            data["title"] = section.title
            data['created_time'] = section.created_time.strftime("%Y-%m-%d %H:%M:%S")
            data['note'] = section.note.name
            data['note_id'] = section.note_id
            catalogue = Catalogue.objects.filter(section=section.id)
            father = Catalogue.objects.get(id=catalogue[0].father)
            data['father'] = father.name
            data['is_release'] = section.is_release
            lis.append(data)
    # 笔记评论
    elif page_type == 'section_comment':
        table_data = SectionMessage.objects.all()
        lis = []
        for history in table_data:
            data = {}
            data["id"] = history.id
            data["section_id"] = history.section.id
            data["title"] = history.section.title
            data['time'] = history.time.strftime("%Y-%m-%d %H:%M:%S")
            data['user'] = history.user.username
            data['content'] = history.content
            if history.level == 0:
                data['type'] = "评论"
            else:
                data['type'] = "回复"
            lis.append(data)
    # 分页器进行分配
    try:
        paginator = Paginator(lis, page_limit)
        # 前端传来页数的数据
        data = paginator.page(page_index)
        # 放在一个列表里
        articles_info = [x for x in data]
        result = {"code": 0,
                  "msg": "分页正常",
                  "count": table_data.count(),
                  "data": articles_info}
    except Exception as e:
        print(e)
        result = {"code": 1,
                  "msg": "查询数据为空！"
                  }
    return JsonResponse(result)


# ajax动态表格搜索
def tableSearch(request):
    global title_search, category_search
    search_type = request.GET.get("type")
    # 搜索浏览记录
    if search_type == "browse":
        title = request.GET.get("title")
        category = request.GET.get("category")
        time = request.GET.get("time")
        q1 = Q()
        q1.connector = 'AND'
        if title:
            q1.children.append(('article__title__icontains', title))
        if category:
            q1.children.append(('category__name__icontains', category))
        if time != "undefined":
            start_date = time.split()[0]
            end_date = time.split()[2]
            start_time = start_date + " 00:00:01"
            end_time = end_date + " 23:59:59"
            q1.children.append(('time__range', [start_time, end_time]))
        table_data = ArticleViewHistory.objects.filter(q1)
        table_body = []
        for history in table_data:
            data = {}
            data["aritcle_id"] = history.article.id
            data["title"] = history.article.title
            data['time'] = history.time.strftime("%Y-%m-%d %H:%M:%S")
            data['category'] = history.article.category.name
            data['category_id'] = history.article.category_id
            tags = history.article.tags.all()
            tags_dict = {}
            for tag in tags:
                tags_dict[tag.id] = tag.name
            data['tags'] = tags_dict
            table_body.append(data)
    # 搜索收藏记录
    elif search_type == "like":
        title = request.GET.get("title")
        category = request.GET.get("category")
        time = request.GET.get("time")
        q1 = Q()
        q1.connector = 'AND'
        if title:
            q1.children.append(('article__title__icontains', title))
        if category:
            q1.children.append(('category__name__icontains', category))
        if time != "undefined":
            start_date = time.split()[0]
            end_date = time.split()[2]
            start_time = start_date + " 00:00:01"
            end_time = end_date + " 23:59:59"
            q1.children.append(('time__range', [start_time, end_time]))
        table_data = ArticleViewHistory.objects.filter(q1).filter(is_like=True)
        table_body = []
        for history in table_data:
            data = {}
            data["aritcle_id"] = history.article.id
            data["title"] = history.article.title
            data['time'] = history.time.strftime("%Y-%m-%d %H:%M:%S")
            data['category'] = history.article.category.name
            data['category_id'] = history.article.category_id
            tags = history.article.tags.all()
            tags_dict = {}
            for tag in tags:
                tags_dict[tag.id] = tag.name
            data['tags'] = tags_dict
            table_body.append(data)
    # 搜索评论记录
    elif search_type == "comment":
        title = request.GET.get("title")
        content = request.GET.get("content")
        time = request.GET.get("time")
        print(title, content, time)
        q1 = Q()
        q1.connector = 'AND'
        if title:
            q1.children.append(('article__title__icontains', title))
        if content:
            q1.children.append(('content__icontains', content))
        if time != "undefined":
            start_date = time.split()[0]
            end_date = time.split()[2]
            start_time = start_date + " 00:00:01"
            end_time = end_date + " 23:59:59"
            q1.children.append(('time__range', [start_time, end_time]))
        table_data = CommentMessage.objects.filter(q1).filter(user=request.user)
        table_body = []
        for history in table_data:
            data = {}
            data['aritcle_id'] = history.article.id
            data['title'] = history.article.title
            data['category'] = history.article.category.name
            data['category_id'] = history.article.category_id
            data['time'] = history.time.strftime("%Y-%m-%d %H:%M:%S")
            data['like'] = history.like
            data['content'] = history.content
            data['content_id'] = history.id
            table_body.append(data)
        print(table_body)
    # 搜索留言记录
    elif search_type == "leave":
        content = request.GET.get("content")
        time = request.GET.get("time")
        print(content, time)
        q1 = Q()
        q1.connector = 'AND'
        if content:
            q1.children.append(('content__icontains', content))
        if time != "undefined":
            start_date = time.split()[0]
            end_date = time.split()[2]
            start_time = start_date + " 00:00:01"
            end_time = end_date + " 23:59:59"
            q1.children.append(('time__range', [start_time, end_time]))
        table_data = LeaveMessage.objects.filter(q1).filter(user=request.user)
        table_body = []
        for history in table_data:
            data = {}
            data['time'] = history.time.strftime("%Y-%m-%d %H:%M:%S")
            data['like'] = history.like
            data['content'] = history.content
            data['content_id'] = history.id
            table_body.append(data)
        print(table_body)
    # 搜索文章分类：
    elif search_type == "category_name":
        category = request.GET.get("category")
        # 模糊查询，不区分大小写
        table_data = Category.objects.filter(name__icontains=category)
        table_body = []
        for category in table_data:
            info = {"id": category.id, "name": category.name}
            table_body.append(info)
    # 搜索文章标签：
    elif search_type == "tag_name":
        tag = request.GET.get("tag")
        # 模糊查询，不区分大小写
        table_data = Tag.objects.filter(name__icontains=tag)
        table_body = []
        for tag in table_data:
            info = {"id": tag.id, "name": tag.name}
            table_body.append(info)
    # 搜索文章列表
    elif search_type == "article":
        title = request.GET.get("title")
        category = request.GET.get("category")
        created_time = request.GET.get("created_time")
        q1 = Q()
        q1.connector = 'AND'
        if title:
            q1.children.append(('title__icontains', title))
        if category:
            q1.children.append(('category__name__icontains', category))
        if created_time != "undefined":
            start_date = created_time.split()[0]
            end_date = created_time.split()[2]
            start_time = start_date + " 00:00:01"
            end_time = end_date + " 23:59:59"
            q1.children.append(('created_time__range', [start_time, end_time]))
        table_data = Article.objects.filter(q1)
        print(table_data)
        table_body = []
        for article in table_data:
            data = {}
            data["id"] = article.id
            data["title"] = article.title
            data['created_time'] = article.created_time.strftime("%Y-%m-%d %H:%M:%S")
            data['is_release'] = article.is_release
            data["cover"] = article.img.url
            data['is_recommend'] = article.is_recommend
            data['category'] = article.category.name
            data['category_id'] = article.category_id
            tags = article.tags.all()
            tags_dict = {}
            for tag in tags:
                tags_dict[tag.id] = tag.name
            data['tags'] = tags_dict
            table_body.append(data)
    # 搜索文章评论
    elif search_type == "article_comment":
        title = request.GET.get("title")
        content = request.GET.get("content")
        time = request.GET.get("time")
        print(title, content, time)
        q1 = Q()
        q1.connector = 'AND'
        if title:
            q1.children.append(('article__title__icontains', title))
        if content:
            q1.children.append(('content__icontains', content))
        if time != "undefined":
            start_date = time.split()[0]
            end_date = time.split()[2]
            start_time = start_date + " 00:00:01"
            end_time = end_date + " 23:59:59"
            q1.children.append(('time__range', [start_time, end_time]))
        table_data = CommentMessage.objects.filter(q1)
        table_body = []
        for history in table_data:
            data = {}
            data["id"] = history.id
            data["article_id"] = history.article.id
            data["title"] = history.article.title
            data['time'] = history.time.strftime("%Y-%m-%d %H:%M:%S")
            data['user'] = history.user.username
            data['content'] = history.content
            table_body.append(data)
        print(table_body)
    # 搜索笔记名称：
    elif search_type == "note_name":
        note = request.GET.get("note")
        # 模糊查询，不区分大小写
        table_data = Note.objects.filter(name__icontains=note)
        table_body = []
        for note in table_data:
            section_count = Section.objects.filter(note_id=note.id).count()
            info = {"id": note.id, "name": note.name, "section_count": section_count}
            table_body.append(info)
        print(table_body)
    # 搜索笔记列表
    elif search_type == "section_list":
        title = request.GET.get("title")
        note = request.GET.get("note")
        created_time = request.GET.get("created_time")
        q1 = Q()
        q1.connector = 'AND'
        if title:
            q1.children.append(('title__icontains', title))
        if note:
            q1.children.append(('note__name__icontains', note))
        if created_time != "undefined":
            start_date = created_time.split()[0]
            end_date = created_time.split()[2]
            start_time = start_date + " 00:00:01"
            end_time = end_date + " 23:59:59"
            q1.children.append(('created_time__range', [start_time, end_time]))
        print(q1)
        table_data = Section.objects.filter(q1)
        print(table_data)
        table_body = []
        for section in table_data:
            data = {}
            data["id"] = section.id
            data["title"] = section.title
            data['created_time'] = section.created_time.strftime("%Y-%m-%d %H:%M:%S")
            data['note'] = section.note.name
            data['note_id'] = section.note_id
            catalogue = Catalogue.objects.filter(section=section.id)
            father = Catalogue.objects.get(id=catalogue[0].father)
            data['father'] = father.name
            table_body.append(data)
    # 搜索笔记评论
    elif search_type == "section_comment":
        section = request.GET.get("section")
        content = request.GET.get("content")
        time = request.GET.get("time")
        print(section, content, time)
        q1 = Q()
        q1.connector = 'AND'
        if section:
            q1.children.append(('article__section__icontains', section))
        if content:
            q1.children.append(('content__icontains', content))
        if time != "undefined":
            start_date = time.split()[0]
            end_date = time.split()[2]
            start_time = start_date + " 00:00:01"
            end_time = end_date + " 23:59:59"
            q1.children.append(('time__range', [start_time, end_time]))
        table_data = SectionMessage.objects.filter(q1)
        table_body = []
        for history in table_data:
            data = {}
            data["id"] = history.id
            data["section_id"] = history.section.id
            data["title"] = history.section.title
            data['time'] = history.time.strftime("%Y-%m-%d %H:%M:%S")
            data['user'] = history.user.username
            data['content'] = history.content
            if history.level == 0:
                data['type'] = "评论"
            else:
                data['type'] = "回复"
            table_body.append(data)
        print(table_body)
    # 搜索轮播图
    elif search_type == "carousel":
        title = request.GET.get("title")
        url = request.GET.get("url")
        print(title, url)
        q1 = Q()
        q1.connector = 'AND'
        if title:
            q1.children.append(('info__icontains', title))
        if url:
            q1.children.append(('url__icontains', url))
        table_data = Carousel.objects.filter(q1)
        table_body = []
        for carousel in table_data:
            data = {}
            data["id"] = carousel.id
            data["info"] = carousel.info
            data["url"] = carousel.url
            data["img"] = carousel.img.url
            data["is_show"] = carousel.is_show
            table_body.append(data)
        print(table_body)
    # 搜索轮播图
    elif search_type == "link":
        name = request.GET.get("name")
        url = request.GET.get("url")
        print(name, url)
        q1 = Q()
        q1.connector = 'AND'
        if name:
            q1.children.append(('name__icontains', name))
        if url:
            q1.children.append(('url__icontains', url))
        table_data = Link.objects.filter(q1)
        table_body = []
        for link in table_data:
            data = {}
            data["id"] = link.id
            data["logo"] = link.logo.url
            data["name"] = link.name
            data["url"] = link.url
            data["describe"] = link.describe
            data["type"] = link.type
            table_body.append(data)
        print(table_body)
    # 搜索用户
    elif search_type == "user":
        username = request.GET.get("username")
        email = request.GET.get("email")
        print(username, email)
        q1 = Q()
        q1.connector = 'AND'
        if username:
            q1.children.append(('user__username__icontains', username))
        if email:
            q1.children.append(('user__email__icontains', email))
        table_data = UserInfo.objects.filter(q1)
        table_body = []
        for user_info in table_data:
            data = {}
            data["id"] = user_info.user.id
            data["username"] = user_info.user.username
            data["email"] = user_info.user.email
            data["is_active"] = user_info.user.is_active
            data["last_login"] = user_info.user.last_login.strftime("%Y-%m-%d")
            data["date_joined"] = user_info.user.date_joined.strftime("%Y-%m-%d")
            data["photo"] = user_info.photo.url
            data["sex"] = user_info.sex
            table_body.append(data)
        print(table_body)
    # 放在一个列表里
    result_data = [x for x in table_body]
    if len(table_body) == 0:
        result = {"code": 1,
                  "msg": "查询记录为空！",
                  "count": 0,
                  "data": result_data}
    else:
        result = {"code": 0,
                  "count": len(table_body),
                  "data": result_data}

    return JsonResponse(result)


# ajax 动态表格表单
def tableForm(request):
    form_type = request.POST.get('type')
    edit_id = request.POST.get('id')
    edit_value = request.POST.get('value')
    # 修改用户启用禁用状态
    if form_type == 'user_active':
        user = User.objects.get(id=edit_id)
        if edit_value == 'true':
            user.is_active = 1
        else:
            user.is_active = 0
        try:
            user.save()
            data = {
                "code": 1,
                "msg": "修改成功！"
            }
        except Exception as e:
            print(e)
            data = {
                "code": 0,
                "msg": "修改失败！"
            }
        return JsonResponse(data)
    # 修改文章是否发布
    elif form_type == 'article_release':
        article = Article.objects.get(id=edit_id)
        if edit_value == 'true':
            article.is_release = 1
        else:
            article.is_release = 0
        try:
            article.save()
            data = {
                "code": 1,
                "msg": "修改成功！"
            }
        except Exception as e:
            print(e)
            data = {
                "code": 0,
                "msg": "修改失败！"
            }
        return JsonResponse(data)
    # 修改文章是否推荐
    elif form_type == 'article_recommend':
        article = Article.objects.get(id=edit_id)
        if edit_value == 'true':
            article.is_recommend = 1
        else:
            article.is_recommend = 0
        try:
            article.save()
            data = {
                "code": 1,
                "msg": "修改成功！"
            }
        except Exception as e:
            print(e)
            data = {
                "code": 0,
                "msg": "修改失败！"
            }
        return JsonResponse(data)
    # 修改轮播图是否显示
    elif form_type == 'carousel_show':
        carousel = Carousel.objects.get(id=edit_id)
        if edit_value == 'true':
            carousel.is_show = 1
        else:
            carousel.is_show = 0
        try:
            carousel.save()
            data = {
                "code": 1,
                "msg": "修改成功！"
            }
        except Exception as e:
            print(e)
            data = {
                "code": 0,
                "msg": "修改失败！"
            }
        return JsonResponse(data)
    # 修改友情链接类型
    elif form_type == 'link_type':
        link = Link.objects.get(id=edit_id)
        if edit_value == 'true':
            link.type = 2
        else:
            link.type = 1
        try:
            link.save()
            data = {
                "code": 1,
                "msg": "修改成功！"
            }
        except Exception as e:
            print(e)
            data = {
                "code": 0,
                "msg": "修改失败！"
            }
        return JsonResponse(data)
    # 修改笔记内容是否发布
    elif form_type == 'section_release':
        section = Section.objects.get(id=edit_id)
        if edit_value == 'true':
            section.is_release = 1
        else:
            section.is_release = 0
        try:
            section.save()
            data = {
                "code": 1,
                "msg": "修改成功！"
            }
        except Exception as e:
            print(e)
            data = {
                "code": 0,
                "msg": "修改失败！"
            }
        return JsonResponse(data)
    else:
        data = {
            "code": 0,
            "msg": "修改失败！"
        }
        return JsonResponse(data)


# ajax用户注册验证
def registerCheck(request):
    username = request.GET.get('username')
    if username is not None:
        if User.objects.filter(username=username).exists():
            data = {
                "code": 0,
                "msg": "用户名已存在"
            }
        else:
            data = {
                "code": 1,
                "msg": "用户名可以使用"
            }
        return JsonResponse(data)
    email = request.GET.get('email')
    if email is not None:
        if User.objects.filter(email=email).exists():
            data = {
                "code": 0,
                "msg": "邮箱已注册"
            }
        else:
            data = {
                "code": 1,
                "msg": "邮箱可以使用"
            }
        return JsonResponse(data)


# ajax获取邮件验证码
def emailCode(request):
    if request.method == "GET":
        email = request.GET["email"]
        action = request.GET["action"]
        if action == "注册新用户":
            username = "新用户"
        elif action == "重置密码":
            username = str(User.objects.get(email=email))
        elif action == "更换邮箱" or action == "绑定邮箱":
            username = str(request.GET["username"])
        email_code = ""
        for i in range(6):
            email_code = email_code + str(random.randint(0, 9))
        request.session['email_code'] = email_code
        # 过期时间 单位s
        request.session.set_expiry(180)
        action = request.GET["action"]
        if sendEmail(email, username, action, email_code):
            data = {
                "code": 1,
                "msg": "验证码已发送"
            }
        else:
            data = {
                "code": 0,
                "msg": "验证码发送失败"
            }
    return JsonResponse(data)


# ajax 检查邮件验证码
def checkEmailCode(request):
    if request.method == "POST":
        # 校验邮件验证码
        request_code = request.POST.get('email_code')
        try:
            session_code = request.session['email_code']
        except KeyError:
            data = {
                "code": 0,
                "msg": "邮件验证码已过期！"
            }
            return JsonResponse(data)
        if request_code != session_code:
            data = {
                "code": 0,
                "msg": "邮件验证码错误！"
            }
            return JsonResponse(data)
        # 校验通过
        else:
            data = {
                "code": 1,
                "msg": "邮件验证码校验通过！"
            }
            return JsonResponse(data)


# ajax图片上传接口
def imageUpload(request):
    if request.method == "POST":
        file = request.FILES.get('file')
        type = request.POST.get('type')
        filename = "%s.%s" % (timezone.now().strftime('%Y_%m_%d_%H_%M_%S_%f'), file.name.split('.')[-1])
        filepath = 'media/' + type + '/' + filename
        if type == 'cover':
            # 文章封面
            img_height = 300
            img_width = 200
        elif type == 'photo':
            # 用户头像
            img_height = 150
            img_width = 150
        elif type == 'carousel':
            # 轮播图
            img_height = 910
            img_width = 520
        elif type == 'link':
            # 友情链接
            img_height = 100
            img_width = 100
        else:
            img_height = None
            img_width = None
        if imgSave(file, filename, filepath, img_height, img_width):
            data = {
                "msg": "上传成功",
                "src": filepath,
                "code": "1",
            }
        else:
            data = {
                "msg": "上传失败",
                "code": "0",
            }
        return JsonResponse(data)


# ajax 评论图片上传
def commentUpload(request):
    if request.method == "POST":
        dir = 'comment/'
        file = request.FILES.get('file')
        filename = "%s.%s" % (timezone.now().strftime('%Y_%m_%d_%H_%M_%S_%f'), file.name.split('.')[-1])
        filepath = 'media/' + dir + filename
        # 图片资源写入服务器
        img_height = None
        img_width = None
        code = imgSave(file, filename, filepath, img_height, img_width)
        if (code == 1):
            result = {
                "code": "0",
                "msg": "上传成功!",
                "data": {
                    "src": filepath,
                }
            }
            return JsonResponse(result)
        else:
            result = {
                "code": "1",
                "msg": "上传失败!",
                "data": {
                    "src": None,
                }
            }
        return JsonResponse(result)


# ajax markdown 图片上传
@csrf_exempt
@xframe_options_sameorigin
def markdownUpload(request):
    if request.method == "POST":
        dir = 'markdown/'
        file = request.FILES.get('editormd-image-file')
        filename = "%s.%s" % (timezone.now().strftime('%Y_%m_%d_%H_%M_%S_%f'), file.name.split('.')[-1])
        filepath = 'media/' + dir + filename
        # 图片资源写入服务器
        img_height = None
        img_width = None
        code = imgSave(file, filename, filepath, img_height, img_width)
        if (code == 1):
            result = {
                "success": 1,
                "message": "上传成功！",
                "url": filepath,
            }
            return JsonResponse(result)
        else:
            result = {
                "success": "0",
                "msg": "上传失败!",
                "src": None,
            }
        return JsonResponse(result)


# 图片保存
def imgSave(file, filename, filepath, width, height):
    """
    :param object file: 保存图片文件对象
    :param str  filename: 保存的文件名称
    :param str  filepath: 保存的文件完整地址（路径+文件名）
    :param str  width: 保存的文件高度
    :param str  height: 保存的文件宽度
    :return: 1 保存成功
    """
    tmp_path = 'media/tmp/' + filename
    try:
        if width and height:
            # 保存图片
            with open(tmp_path, 'wb+') as f:
                for chrunk in file.chunks():
                    f.write(chrunk)
            f.close()
            # 转换图片格式
            img = ImagePIL.open(tmp_path)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            # 修改分辨率
            resized_image = img.resize((width, height), Image.ANTIALIAS)
            # 保存本地
            resized_image.save(filepath)
        else:
            # 保存图片
            with open(filepath, 'wb+') as f:
                for chrunk in file.chunks():
                    f.write(chrunk)
            f.close()
        return 1
    except Exception as e:
        print(e)
        return 0


# ajax 绑定邮箱
def bindEmail(request):
    if request.method == "POST":
        email_code = request.POST.get("code")
        email = request.POST.get("email")
        try:
            session_code = request.session['email_code']
        except KeyError:
            result = {
                "code": 0,
                "msg": '验证码过期！',
            }
            return JsonResponse(result)
        if email_code != request.session['email_code']:
            result = {
                "code": 0,
                "msg": '验证码错误！'
            }
        else:
            # 验证通过，绑定邮箱号
            user = request.user
            user.email = email
            user.save()
            result = {
                "code": 1,
                "msg": '邮箱绑定成功！'
            }
        return JsonResponse(result)
