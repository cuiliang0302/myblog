import datetime
import json
import os
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q, Max
from django.forms import model_to_dict
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.utils import timezone

from blog.forms import searchForm
from blog.models import *
from account.models import UserInfo, ArticleViewHistory, LeaveMessage, CommentMessage, SectionViewHistory, \
    SectionMessage
from management.models import About, Info, Carousel, Link, WebsiteConfig, ImagesConfig
from myblog.settings import BASE_DIR, BAIDU_START_DATE, SITE_MAP_PATH
from management.tools import BaiduApi, SiteMap
from django.db.models import Max, Min
from django.core.cache import cache


# 全局调用函数
def global_variable(request):
    # 登录用户信息头像
    try:
        userinfo = UserInfo.objects.get(user_id=request.user.id)
    except Exception as e:
        print(e)
        userinfo = None
    # 所有分类
    categorys = Category.objects.all()
    # 学习笔记
    notes = Note.objects.all()
    # 搜索表单
    search_form = searchForm()
    # 网站信息
    site = WebsiteConfig.objects.get(id=1)
    # 默认图片
    img = ImagesConfig.objects.get(id=1)
    return locals()


# 侧边栏内容
def aside():
    # 博主信息
    info = Info.objects.get(id=1)
    # 所有标签
    tags = Tag.objects.all()
    # 推荐阅读
    recommend = Article.objects.all().filter(is_recommend=True).filter(is_release=True).order_by('-created_time')[:6]
    # 阅读排行
    viewTop = Article.objects.all().filter(is_release=True).order_by('-view')[:9]
    # 点赞排行
    likeTop = Article.objects.all().filter(is_release=True).order_by('-like')[:9]
    # 收藏排行
    collectionTop = Article.objects.all().filter(is_release=True).order_by('-collection')[:9]
    # 评论排行
    commentTop = Article.objects.all().filter(is_release=True).order_by('-comment')[:9]
    # 数据统计
    if cache.get("data_count"):
        # print("有数据，直接用")
        data_count = cache.get("data_count")
    else:
        # print("过期了，重新取")
        data_count = {}
        # 运行时间
        now_data = str(timezone.now().strftime('%Y-%m-%d'))
        d1 = datetime.datetime.strptime(BAIDU_START_DATE, '%Y%m%d')
        d2 = datetime.datetime.strptime(now_data, '%Y-%m-%d')
        data_count['day'] = (d2 - d1).days
        # 流量统计
        api = BaiduApi()
        count = api.countAll()
        data_count['pv'] = count['pv']
        data_count['uv'] = count['uv']
        data_count['ip'] = count['ip']
        # 文章总数
        data_count['article'] = Article.objects.filter(is_release=True).count()
        # 笔记总数
        data_count['section'] = Section.objects.filter(is_release=True).count()
        # 分类数
        data_count['category'] = Category.objects.count()
        # 标签数
        data_count['tag'] = Tag.objects.count()
        cache.set("data_count", data_count, timeout=3600)
        data_count = cache.get("data_count")
    return locals()


# 首页
def index(request):
    aside_dict = aside()
    count = Article.objects.all().filter(is_release=True).count()
    page_count = (count // 5) + 1
    carousels = Carousel.objects.all()
    return render(request, 'blog/index.html', locals())


# 首页流加载
def indexPage(request):
    page_index = request.GET.get('page')
    # 前台传来的一页显示多少条数据
    page_limit = request.GET.get('limit')
    articles_all = Article.objects.all().filter(is_release=True)
    # 处理成LayUi官方文档的格式
    lis = []
    for article in articles_all:
        data = model_to_dict(article)
        data['category'] = article.category.name
        data['img'] = article.img.name
        data['created_time'] = article.created_time.strftime("%Y-%m-%d %H:%M:%S")
        data.pop('tags')
        data.pop('body')
        data['category_id'] = article.category_id
        lis.append(data)
    # 分页器进行分配
    try:
        paginator = Paginator(lis, page_limit)
        # 前端传来页数的数据
        data = paginator.page(page_index)
        # 放在一个列表里
        articles_info = [x for x in data]
        result = {"code": 1,
                  "msg": "分页正常",
                  "count": articles_all.count(),
                  "data": articles_info}
    except Exception as e:
        print(e)
        result = {"code": 0,
                  "msg": "分页调用异常！"
                  }
    return JsonResponse(result)


# 文章分类列表
def category(request, category_id):
    articles_all = Article.objects.filter(category_id=category_id).filter(is_release=True)
    count = articles_all.count()
    category_name = Category.objects.get(id=category_id)
    return render(request, 'blog/categoryList.html',
                  {"count": count, "category_name": category_name, "category_id": category_id, "aside_dict": aside()})


# ajax文章分类分页
def categoryPage(request):
    category_id = request.GET.get('category_id')
    # 前台传来的页数
    page_index = request.GET.get('page')
    # 前台传来的一页显示多少条数据
    page_limit = request.GET.get('limit')
    articles_all = Article.objects.filter(category_id=category_id).filter(is_release=True)
    # 处理成LayUi官方文档的格式
    lis = []
    for article in articles_all:
        data = model_to_dict(article)
        data['category'] = article.category.name
        data['img'] = article.img.name
        data['created_time'] = article.created_time.strftime("%Y-%m-%d %H:%M:%S")
        data.pop('tags')
        data.pop('body')
        data['category_id'] = article.category_id
        lis.append(data)
    # 分页器进行分配
    try:
        paginator = Paginator(lis, page_limit)
        # 前端传来页数的数据
        data = paginator.page(page_index)
        # 放在一个列表里
        articles_info = [x for x in data]
        result = {"code": 1,
                  "msg": "分页正常",
                  "count": articles_all.count(),
                  "data": articles_info}
    except Exception as e:
        print(e)
        result = {"code": 0,
                  "msg": "分页调用异常！"
                  }
    return JsonResponse(result)


# 文章标签列表
def tag(request, tag_id):
    tag_obj = Tag.objects.get(id=tag_id)
    count = tag_obj.article_set.all().count()
    return render(request, 'blog/tagList.html',
                  {"count": count, "tag_name": tag_obj, "tag_id": tag_id, "aside_dict": aside()})


# 学习笔记
def note(request, note_id):
    aside_dict = aside()
    note = Note.objects.get(id=note_id)
    first_catalogue = Catalogue.objects.filter(note=note.id).filter(level=1)
    num = ["零", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十", "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八"]
    catalogue_list = []
    for i in first_catalogue:
        catalogue_dict = {}
        catalogue_dict["title"] = num[i.order] + "、\t" + i.name
        catalogue_dict["spread"] = 'true'
        children_list = []
        catalogue_dict["children"] = children_list
        second_catalogue = Catalogue.objects.filter(note=note.id).filter(father=i.id)
        for j in second_catalogue:
            children_dict = {}
            children_dict["title"] = str(j.order) + ".\t" + j.section.title
            children_dict["href"] = '/blog/section-' + str(j.section.id)
            children_list.append(children_dict)
        catalogue_list.append(catalogue_dict)
    return render(request, 'blog/note.html', locals())


# 标签列表分页
def tagPage(request):
    tag_id = request.GET.get('tag_id')
    # 前台传来的页数
    page_index = request.GET.get('page')
    # 前台传来的一页显示多少条数据
    page_limit = request.GET.get('limit')
    article_list = []
    tag_obj = Tag.objects.get(id=tag_id)
    article_obj = tag_obj.article_set.all().values()
    for article in article_obj:
        category_name = Category.objects.get(id=article['category_id'])
        article["category"] = category_name
        article_list.append(article)
    lis = []
    for article in article_list:
        article['category'] = Category.objects.get(id=article['category_id']).name
        article['img'] = Article.objects.get(id=article['id']).img.name
        article['created_time'] = article['created_time'].strftime("%Y-%m-%d %H:%M:%S")
        article.pop('body')
        lis.append(article)
    try:
        paginator = Paginator(lis, page_limit)
        # 前端传来页数的数据
        data = paginator.page(page_index)
        # 放在一个列表里
        articles_info = [x for x in data]
        result = {"code": 1,
                  "msg": "分页正常",
                  "count": len(article_list),
                  "data": articles_info}
    except Exception as e:
        print(e)
        result = {"code": 0,
                  "msg": "分页调用异常！"
                  }
    return JsonResponse(result)


# 查找博文根评论的所有子回复
def comment_record(article, root_id, record):
    for comment in CommentMessage.objects.filter(root_id=root_id):
        comment_dict = model_to_dict(comment)
        comment_dict['photo'] = CommentMessage.objects.get(id=comment.id).user.userinfo.photo.name
        comment_dict['web'] = CommentMessage.objects.get(id=comment.id).user.userinfo.web
        comment_dict['username'] = CommentMessage.objects.get(id=comment.id).user.username
        comment_dict['time'] = CommentMessage.objects.get(id=comment.id).time.strftime("%Y-%m-%d %H:%M:%S")
        reply_id = CommentMessage.objects.get(id=comment.id).reply_id
        comment_dict['reply_name'] = CommentMessage.objects.get(id=reply_id).user.username
        comment_dict['reply_web'] = CommentMessage.objects.get(id=reply_id).user.userinfo.web
        record.append(comment_dict)
    return record


# 文章内容页
def show(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    # 阅读量+1
    article.view = article.view + 1
    article.save()
    article_like = 0
    # 用户已登录
    if request.user.id:
        # 添加阅读记录(第一次：添加，已有记录：更新时间)
        history = ArticleViewHistory.objects.filter(article_id=article_id).filter(user_id=request.user)
        if history:
            change_history = history[0]
            change_history.time = timezone.now()
            change_history.save()
        else:
            new_history = ArticleViewHistory()
            new_history.article = article
            new_history.category = article.category
            new_history.user = request.user
            new_history.save()
        # 判断是否已收藏文章
        user_list = ArticleViewHistory.objects.filter(article_id=article_id)
        for i in user_list:
            if request.user == i.user and i.is_like == 1:
                article_like = 1
                break
    # 下一篇，找出id大于当前文章id的文章,升序排序后取第一个，即为下一篇
    next_article = Article.objects.filter(id__gt=article_id).filter(is_release=True).order_by("id")[:1]
    if len(next_article) == 0:
        next_article = 0
    else:
        for next in next_article:
            next_article = next
    # 上一篇，找出id小于当前文章id的文章，降序排序后取第一个，即为上一篇
    last_article = Article.objects.filter(id__lt=article_id).filter(is_release=True).order_by("-id")[:1]
    if len(last_article) == 0:
        last_article = 0
    else:
        for last in last_article:
            last_article = last
    # 评论列表
    # 全部评论
    all_comment = []
    for info in CommentMessage.objects.filter(article=article):
        # 根评论
        if info.reply_id is None:
            # 单条记录
            record = []
            info_dict = model_to_dict(info)
            info_dict['username'] = CommentMessage.objects.get(id=info.id).user.username
            info_dict['reply_id'] = 'None'
            info_dict['root_id'] = 'None'
            info_dict['reply_name'] = 'None'
            info_dict['photo'] = CommentMessage.objects.get(id=info.id).user.userinfo.photo.name
            info_dict['web'] = CommentMessage.objects.get(id=info.id).user.userinfo.web
            info_dict['time'] = CommentMessage.objects.get(id=info.id).time.strftime("%Y-%m-%d %H:%M:%S")
            record.append(info_dict)
            # 根据根留言查找子回复
            record = comment_record(article, info.id, record)
            all_comment.append(record)
    # 热门评论
    hot_comment = CommentMessage.objects.filter(article=article).filter(level=0).order_by('-like')
    # 我的评论
    user_id = request.user.id
    if user_id:
        my_comment = CommentMessage.objects.filter(article=article).filter(level=0).filter(user_id=user_id)
    else:
        my_comment = None
    # 评论统计
    count = CommentMessage.objects.filter(article=article).count()
    # 猜你喜欢
    guess1 = Article.objects.filter(is_release=True).filter(tags=article.tags.all()[0]).order_by('?')[:2]
    guess2 = Article.objects.filter(is_release=True).filter(tags=article.tags.all()[1]).order_by('?')[:2]
    return render(request, 'blog/show.html',
                  {"article": article, "articke_like": article_like, "next_article": next_article,
                   "last_article": last_article, "all_comment": all_comment, "hot_comment": hot_comment,
                   "my_comment": my_comment, "count": count, "aside_dict": aside(), "guess1": guess1, "guess2": guess2})


# 查找笔记根评论的所有子回复
def note_record(article, root_id, record):
    for comment in SectionMessage.objects.filter(root_id=root_id):
        comment_dict = model_to_dict(comment)
        comment_dict['photo'] = SectionMessage.objects.get(id=comment.id).user.userinfo.photo.name
        comment_dict['web'] = SectionMessage.objects.get(id=comment.id).user.userinfo.web
        comment_dict['username'] = SectionMessage.objects.get(id=comment.id).user.username
        comment_dict['time'] = SectionMessage.objects.get(id=comment.id).time.strftime("%Y-%m-%d %H:%M:%S")
        reply_id = SectionMessage.objects.get(id=comment.id).reply_id
        comment_dict['reply_name'] = SectionMessage.objects.get(id=reply_id).user.username
        comment_dict['reply_web'] = SectionMessage.objects.get(id=reply_id).user.userinfo.web
        record.append(comment_dict)
    return record


# 笔记内容页
def section(request, content_id):
    section = get_object_or_404(Section, id=content_id)
    # 阅读量+1
    section.view = section.view + 1
    section.save()
    note = Note.objects.get(id=section.note_id)
    # 上下篇笔记
    second = Catalogue.objects.get(section=section.id)
    second_min = Catalogue.objects.filter(father=second.father).aggregate(Min('order'))["order__min"]
    second_max = Catalogue.objects.filter(father=second.father).aggregate(Max('order'))["order__max"]
    first = Catalogue.objects.get(id=second.father)
    first_min = Catalogue.objects.filter(note=note).filter(level=1).aggregate(Min('order'))["order__min"]
    first_max = Catalogue.objects.filter(note=note).filter(level=1).aggregate(Max('order'))["order__max"]
    if second.order == second_min:
        if first.order == first_min:
            # 第一篇文章
            last_content = None
        else:
            # 上一篇找上一章最后一篇
            last_father = Catalogue.objects.filter(note=note).filter(level=1).filter(order=first.order - 1)
            last_second_max = Catalogue.objects.filter(father=last_father[0].id).aggregate(Max('order'))["order__max"]
            last_content = Catalogue.objects.filter(father=last_father[0].id).filter(order=last_second_max)[0]
        next_content = Catalogue.objects.filter(father=first.id).filter(order=second.order + 1)[0]
    elif second.order == second_max:
        if first.order == first_max:
            # 最后一篇文章
            next_content = None
        else:
            # 下一篇找上一章第一篇
            next_father = Catalogue.objects.filter(note=note).filter(level=1).filter(order=first.order + 1)
            next_second_min = Catalogue.objects.filter(father=next_father[0].id).aggregate(Min('order'))["order__min"]
            next_content = Catalogue.objects.filter(father=next_father[0].id).filter(order=next_second_min)[0]
        last_content = Catalogue.objects.filter(father=first.id).filter(order=second.order - 1)[0]
    else:
        last_content = Catalogue.objects.filter(father=first.id).filter(order=second.order - 1)[0]
        next_content = Catalogue.objects.filter(father=first.id).filter(order=second.order + 1)[0]
    # 笔记目录
    first_catalogue = Catalogue.objects.filter(note=note.id).filter(level=1)
    num = ["零", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十", "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八"]
    catalogue_list = []
    for i in first_catalogue:
        catalogue_dict = {}
        catalogue_dict["title"] = num[i.order] + "、\t" + i.name
        if i.id == first.id:
            catalogue_dict["spread"] = 'true'
        children_list = []
        catalogue_dict["children"] = children_list
        second_catalogue = Catalogue.objects.filter(note=note.id).filter(father=i.id)
        for j in second_catalogue:
            children_dict = {}
            children_dict["id"] = str(j.section.id)
            children_dict["title"] = str(j.order) + ".\t" + j.section.title
            children_dict["href"] = '/blog/section-' + str(j.section.id)
            children_list.append(children_dict)
        catalogue_list.append(catalogue_dict)
    # 用户已登录
    article_like = '0'
    if request.user.id:
        # 添加阅读记录(第一次：添加，已有记录：更新时间)
        history = SectionViewHistory.objects.filter(section_id=section.id).filter(user_id=request.user)
        if history:
            change_history = history[0]
            change_history.time = timezone.now()
            change_history.save()
        else:
            new_history = SectionViewHistory()
            new_history.section = section
            new_history.note = section.note
            new_history.user = request.user
            new_history.save()
        # 判断是否已收藏文章
        user_list = SectionViewHistory.objects.filter(section_id=section.id)
        for i in user_list:
            if request.user == i.user and i.is_like == 1:
                article_like = 1
                break
        # 评论列表
        # 全部评论
        content_count = SectionMessage.objects.filter(section=section).count()
        all_comment = []
        for info in SectionMessage.objects.filter(section=section):
            # 根评论
            if info.reply_id is None:
                # 单条记录
                record = []
                info_dict = model_to_dict(info)
                info_dict['username'] = SectionMessage.objects.get(id=info.id).user.username
                info_dict['reply_id'] = 'None'
                info_dict['root_id'] = 'None'
                info_dict['reply_name'] = 'None'
                info_dict['photo'] = SectionMessage.objects.get(id=info.id).user.userinfo.photo.name
                info_dict['web'] = SectionMessage.objects.get(id=info.id).user.userinfo.web
                info_dict['time'] = SectionMessage.objects.get(id=info.id).time.strftime("%Y-%m-%d %H:%M:%S")
                record.append(info_dict)
                # 根据根留言查找子回复
                record = note_record(section, info.id, record)
                all_comment.append(record)
        # 热门评论
        hot_comment = SectionMessage.objects.filter(section=section).filter(level=0).order_by('-like')
        # 我的评论
        user_id = request.user.id
        if user_id:
            my_comment = SectionMessage.objects.filter(section=section).filter(level=0).filter(user_id=user_id)
        else:
            my_comment = None
    # 评论统计
    comment_count = SectionMessage.objects.filter(section=section).count()
    return render(request, 'blog/section.html', locals())


# 时间轴
def timeAxis(request):
    date_list_all = []  # 建立一个列表用来存放所有日期
    date_obj = Article.objects.filter(is_release=True).values('created_time')
    for date in date_obj:
        date = date['created_time'].strftime('%Y年%m月')
        date_list_all.append(date)
    date_list_count = []
    # 日期去重
    for i in date_list_all:
        date_list_count.append(date_list_all.count(i))
    date_list_sum = zip(date_list_all, date_list_count)
    date_list = []
    for (i, j) in date_list_sum:
        if (i, j) not in date_list:
            date_list.append((i, j))

    return render(request, 'blog/timeAxis.html', {"date_list": date_list, "aside_dict": aside()})


# 查找根留言的所有子回复
def build_record(root_id, record):
    for comment in LeaveMessage.objects.filter(root_id=root_id):
        comment_dict = model_to_dict(comment)
        comment_dict['photo'] = LeaveMessage.objects.get(id=comment.id).user.userinfo.photo.name
        comment_dict['web'] = LeaveMessage.objects.get(id=comment.id).user.userinfo.web
        comment_dict['username'] = LeaveMessage.objects.get(id=comment.id).user.username
        comment_dict['time'] = LeaveMessage.objects.get(id=comment.id).time.strftime("%Y-%m-%d %H:%M:%S")
        reply_id = LeaveMessage.objects.get(id=comment.id).reply_id
        comment_dict['reply_name'] = LeaveMessage.objects.get(id=reply_id).user.username
        comment_dict['reply_web'] = LeaveMessage.objects.get(id=reply_id).user.userinfo.web
        record.append(comment_dict)
    return record


# 留言板
def messageBoard(request):
    # 全部留言
    all_message = []
    for info in LeaveMessage.objects.all():
        # 根留言
        if info.reply_id is None:
            # 单条记录
            record = []
            info_dict = model_to_dict(info)
            info_dict['username'] = LeaveMessage.objects.get(id=info.id).user.username
            info_dict['reply_id'] = 'None'
            info_dict['root_id'] = 'None'
            info_dict['reply_name'] = 'None'
            info_dict['photo'] = LeaveMessage.objects.get(id=info.id).user.userinfo.photo.name
            info_dict['web'] = LeaveMessage.objects.get(id=info.id).user.userinfo.web
            info_dict['time'] = LeaveMessage.objects.get(id=info.id).time.strftime("%Y-%m-%d %H:%M:%S")
            record.append(info_dict)
            # 根据根留言查找子回复
            record = build_record(info.id, record)
            all_message.append(record)
    # 热门留言
    hot_message = LeaveMessage.objects.filter(level=0).order_by('-like')
    # 我的留言
    user_id = request.user.id
    if user_id:
        my_message = LeaveMessage.objects.filter(level=0).filter(user_id=user_id)
    else:
        my_message = None
    # 留言统计
    count = LeaveMessage.objects.all().count()
    return render(request, 'blog/messageBoard.html',
                  {"all_message": all_message, "hot_message": hot_message, "my_message": my_message,
                   "count": count, "aside_dict": aside()})


# ajax发布留言
def postMessage(request):
    content = request.GET.get("content")
    username = request.GET.get("username")
    level = request.GET.get("level")
    if content and username:
        reply_id = request.GET.get("reply_id")
        root_id = request.GET.get("root_id")
        message = LeaveMessage()
        message.content = content
        message.user = User.objects.get(username=username)
        message.level = level
        message.reply_id = reply_id
        message.root_id = root_id
        message.save()
        result = {"code": 1, "msg": "留言成功!"}
    else:
        result = {"code": 0, "msg": "留言失败!"}
    return JsonResponse(result)


# ajax点赞留言
def likeMessage(request):
    message_id = request.GET.get("like_id")
    if message_id:
        message = LeaveMessage.objects.get(id=message_id)
        message.like = message.like + 1
        message.save()
        result = {"code": 1, "msg": "点赞成功!"}
    else:
        result = {"code": 0, "msg": "点赞失败!"}
    return JsonResponse(result)


# ajax删除留言
def delMessage(request):
    message_id = request.GET.get("del_id")
    delid_arr = request.GET.get("delidArr")
    if message_id:
        message = LeaveMessage.objects.get(id=message_id)
        reply = LeaveMessage.objects.filter(reply_id=message_id)
        # 根留言且没有回复，可以删除
        if message.level == 0 and len(reply) == 0:
            LeaveMessage.objects.get(id=message_id).delete()
        else:
            message.content = "该内容已被用户删除"
            message.save()
        result = {"code": 1, "msg": "删除成功!"}
    elif delid_arr:
        article_list = delid_arr.split(',')
        for i in article_list:
            message = LeaveMessage.objects.get(id=i)
            reply = LeaveMessage.objects.filter(reply_id=i)
            # 根留言且没有回复，可以删除
            if message.level == 0 and len(reply) == 0:
                LeaveMessage.objects.get(id=i).delete()
            else:
                message.content = "该内容已被用户删除"
                message.save()
        result = {"code": 1, "msg": "删除成功!"}
    else:
        result = {"code": 0, "msg": "删除失败!"}
    return JsonResponse(result)


# 关于
def about(request):
    aside_dict = aside()
    about_content = About.objects.get(id=1)
    return render(request, 'blog/about.html', locals())


# 友情链接
def link(request):
    hots = Link.objects.filter(type=2)[:4]
    links = Link.objects.filter(type=1)[:12]
    return render(request, 'blog/link.html', locals())


# 搜索
def search(request):
    aside_dict = aside()
    key = request.GET.get('key')
    search_form = searchForm(request.GET)
    if search_form.is_valid():
        search_data = search_form.cleaned_data
        articles = Article.objects.filter(is_release=1).filter(
            Q(title__icontains=search_data['key']) | Q(body__icontains=search_data['key']))
        if articles.count() == 0:
            message = '未搜索到匹配内容，请重新输入关键字！'
    else:
        message = '输入内容不合法！'
    return render(request, 'blog/search.html', locals())


# ajax文章点赞
def articleLike(request):
    type = request.GET.get("type")
    if type == 'blog':
        article = Article.objects.get(id=request.GET.get("article_id"))
        article.like = article.like + 1
        article.save()
        result = {"code": 1, "msg": "感谢点赞!"}
    elif type == 'note':
        section = Section.objects.get(id=request.GET.get("section_id"))
        section.like = section.like + 1
        section.save()
        result = {"code": 1, "msg": "感谢点赞!"}
    else:
        result = {"code": 0, "msg": "点赞失败!"}
    return JsonResponse(result)


# ajax文章收藏
def articleCollection(request):
    type = request.GET.get("type")
    if type == 'blog':
        # 更新浏览记录表
        article_id = request.GET.get("article_id")
        history = ArticleViewHistory.objects.filter(article_id=article_id).filter(user_id=request.user)
        change_history = history[0]
        change_history.time = timezone.now()
        change_history.is_like = 1
        change_history.save()
        # 更新文章信息表
        article = Article.objects.get(id=article_id)
        article.collection = ArticleViewHistory.objects.filter(article_id=article_id).filter(is_like=1).count()
        article.save()
        result = {"code": 1, "msg": "感谢收藏!"}
    elif type == 'note':
        # 更新浏览记录表
        section_id = request.GET.get("section_id")
        history = SectionViewHistory.objects.filter(section_id=section_id).filter(user_id=request.user)
        change_history = history[0]
        change_history.time = timezone.now()
        change_history.is_like = 1
        change_history.save()
        # 更新文章信息表
        section = Section.objects.get(id=section_id)
        section.collection = SectionViewHistory.objects.filter(section_id=section_id).filter(is_like=1).count()
        section.save()
        result = {"code": 1, "msg": "感谢收藏!"}
    else:
        result = {"code": 0, "msg": "收藏失败!"}
    return JsonResponse(result)


# ajax取消收藏
def deleteCollection(request):
    type = request.GET.get("type")
    delid_arr = request.GET.get("delidArr")
    if type == 'blog':
        article_id = request.GET.get("article_id")
        if article_id:
            # 更新浏览记录表
            history = ArticleViewHistory.objects.filter(article_id=article_id).filter(user_id=request.user)
            change_history = history[0]
            change_history.time = timezone.now()
            change_history.is_like = 0
            change_history.save()
            result = {"code": 1, "msg": "已取消收藏!"}
        elif delid_arr:
            article_list = delid_arr.split(',')
            for i in article_list:
                change_history = ArticleViewHistory.objects.get(id=i)
                change_history.time = timezone.now()
                change_history.is_like = 0
                change_history.save()
            result = {"code": 1, "msg": "已取消收藏!"}
    elif type == 'note':
        section_id = request.GET.get("section_id")
        if section_id:
            # 更新浏览记录表
            history = SectionViewHistory.objects.filter(section_id=section_id).filter(user_id=request.user)
            change_history = history[0]
            change_history.time = timezone.now()
            change_history.is_like = 0
            change_history.save()
            result = {"code": 1, "msg": "已取消收藏!"}
        elif delid_arr:
            article_list = delid_arr.split(',')
            for i in article_list:
                change_history = ArticleViewHistory.objects.get(id=i)
                change_history.time = timezone.now()
                change_history.is_like = 0
                change_history.save()
            result = {"code": 1, "msg": "已取消收藏!"}
    else:
        result = {"code": 0, "msg": "操作失败!"}
    return JsonResponse(result)


# ajax时间轴文章列表
def timeArticle(request):
    year = request.GET.get("year")
    month = request.GET.get("month")
    if year and month:
        article_list = Article.objects.filter(created_time__year=year).filter(created_time__month=month).order_by(
            '-created_time')
        lis = []
        for article in article_list:
            data = dict()
            data['id'] = article.id
            data['title'] = article.title
            data_joined = article.created_time.strftime("%Y-%m-%d %H:%M")
            data['created_time'] = data_joined
            lis.append(data)
        result = {"code": 1, "data": lis}

    else:
        result = {"code": 0, "msg": "查询失败!"}
    return JsonResponse(result)


# ajax发表评论
def postComment(request):
    content = request.POST.get("content")
    username = request.POST.get("username")
    level = request.POST.get("level")
    type = request.POST.get("type")
    reply_id = request.POST.get("reply_id")
    root_id = request.POST.get("root_id")
    if type == 'blog':
        article_id = request.POST.get("article_id")
        message = CommentMessage()
        message.article = Article.objects.get(id=article_id)
        message.content = content
        message.user = User.objects.get(username=username)
        message.level = level
        message.reply_id = reply_id
        message.root_id = root_id
        message.save()
        # 更新评论数
        article = Article.objects.get(id=article_id)
        article.comment = CommentMessage.objects.filter(article=article).count()
        article.save()
        result = {"code": 1, "msg": "评论成功!"}
    elif type == 'note':
        section_id = request.POST.get("section_id")
        message = SectionMessage()
        message.section = Section.objects.get(id=section_id)
        message.content = content
        message.user = User.objects.get(username=username)
        message.level = level
        message.reply_id = reply_id
        message.root_id = root_id
        message.save()
        # 更新评论数
        section = Section.objects.get(id=section_id)
        section.comment = SectionMessage.objects.filter(section=section).count()
        section.save()
        result = {"code": 1, "msg": "评论成功!"}
    else:
        result = {"code": 0, "msg": "评论失败!"}
    return JsonResponse(result)


# ajax点赞评论
def likeComment(request):
    message_id = request.GET.get("like_id")
    type = request.GET.get("type")
    if type == 'blog':
        message = CommentMessage.objects.get(id=message_id)
        message.like = message.like + 1
        message.save()
        result = {"code": 1, "msg": "点赞成功!"}
    elif type == 'note':
        message = SectionMessage.objects.get(id=message_id)
        message.like = message.like + 1
        message.save()
        result = {"code": 1, "msg": "点赞成功!"}
    else:
        result = {"code": 0, "msg": "点赞失败!"}
    return JsonResponse(result)


# ajax删除评论
def delComment(request):
    message_id = request.GET.get("del_id")
    delid_arr = request.GET.get("delidArr")
    type = request.GET.get("type")
    if type == 'blog':
        if message_id:
            message = CommentMessage.objects.get(id=message_id)
            reply = CommentMessage.objects.filter(reply_id=message_id)
            # 根留言且没有回复，可以删除
            if message.level == 0 and len(reply) == 0:
                CommentMessage.objects.get(id=message_id).delete()
            else:
                message.content = "该内容已被用户删除"
                message.save()
            result = {"code": 1, "msg": "删除成功!"}
        elif delid_arr:
            article_list = delid_arr.split(',')
            for i in article_list:
                message = CommentMessage.objects.get(id=i)
                reply = CommentMessage.objects.filter(reply_id=i)
                # 根留言且没有回复，可以删除
                if message.level == 0 and len(reply) == 0:
                    CommentMessage.objects.get(id=i).delete()
                else:
                    message.content = "该内容已被用户删除"
                    message.save()
            result = {"code": 1, "msg": "删除成功!"}
    elif type == "note":
        if message_id:
            message = SectionMessage.objects.get(id=message_id)
            reply = SectionMessage.objects.filter(reply_id=message_id)
            # 根留言且没有回复，可以删除
            if message.level == 0 and len(reply) == 0:
                SectionMessage.objects.get(id=message_id).delete()
            else:
                message.content = "该内容已被用户删除"
                message.save()
            result = {"code": 1, "msg": "删除成功!"}
        elif delid_arr:
            article_list = delid_arr.split(',')
            for i in article_list:
                message = SectionMessage.objects.get(id=i)
                reply = SectionMessage.objects.filter(reply_id=i)
                # 根留言且没有回复，可以删除
                if message.level == 0 and len(reply) == 0:
                    SectionMessage.objects.get(id=i).delete()
                else:
                    message.content = "该内容已被用户删除"
                    message.save()
            result = {"code": 1, "msg": "删除成功!"}
    else:
        result = {"code": 0, "msg": "删除失败!"}
    return JsonResponse(result)


# 初始化数据接口
def initApi(request):
    model = request.GET.get("type").strip('/')
    json_file = "init-" + model + ".json"
    path = "static/layui-mini/api/" + json_file
    open_path = os.path.join(BASE_DIR, *path.split('/'))
    with open(open_path, 'r', encoding='utf8')as f:
        json_data = json.load(f)
    f.close()
    return JsonResponse(json_data)


# sitemap文件生成
def siteMap(request):
    sitemap = SiteMap()
    sitemap.articleUrl()
    sitemap.categoryUrl()
    sitemap.tagUrl()
    sitemap.sectionUrl()
    sitemap.noteUrl()
    sitemap.otherUrl()
    with open(SITE_MAP_PATH, 'w') as file_object:
        for i in range(len(sitemap.url)):
            if i != len(sitemap.url) - 1:
                file_object.write(sitemap.url[i] + '\n')
            else:
                file_object.write(sitemap.url[i])
    file_object.close()
    return HttpResponse("sitemap生成成功")
