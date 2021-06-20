import json
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.clickjacking import xframe_options_exempt

from account.models import ArticleViewHistory, CommentMessage, SectionViewHistory, SectionMessage
from account.views import imgSave
from blog.models import Category, Tag, Article, Note, Section, Catalogue
from management.models import About, WebsiteConfig, ImagesConfig, Info, Carousel, Link
from management.tools import AliyunSDK, BaiduApi


@login_required()
# 后台管理模块
def management(request):
    model = "management"
    return render(request, 'layui-mini/base.html', locals())


# 后台管理首页
@xframe_options_exempt
@login_required()
def dashboard(request):
    # 流量统计比较
    api = BaiduApi()
    count = api.countToday()
    today = count[0]
    compare = count[2]
    today_pv = today[1]
    today_uv = today[2]
    today_time = today[3]
    today_page = today[4]
    compare_pv = compare[1]
    compare_uv = compare[2]
    compare_time = compare[3]
    compare_page = compare[4]
    # 主机性能
    cpu = AliyunSDK("CPUUtilization")
    cpu_rate = round(cpu.metricInfo(), 2)
    memory = AliyunSDK("memory_usedutilization")
    memory_rate = round(memory.metricInfo(), 2)
    disk = AliyunSDK("diskusage_utilization")
    disk_rate = round(disk.metricInfo(), 2)
    load = AliyunSDK("load_15m")
    load_rate = round(load.metricInfo() * 100, 2)
    return render(request, 'layui-mini/management/index.html', locals())


# 文章列表
@xframe_options_exempt
@login_required()
def articleList(request):
    return render(request, 'layui-mini/management/articleList.html', locals())


# 文章分类
@xframe_options_exempt
@login_required()
def articleCategory(request):
    return render(request, 'layui-mini/management/articleCategory.html', locals())


# 文章标签
@xframe_options_exempt
@login_required()
def articleTag(request):
    return render(request, 'layui-mini/management/articleTag.html', locals())


# 文章评论
@xframe_options_exempt
@login_required()
def articleComment(request):
    return render(request, 'layui-mini/management/articleComment.html', locals())


# 笔记名称
@xframe_options_exempt
@login_required()
def sectionNote(request):
    return render(request, 'layui-mini/management/sectionNote.html', locals())


# 笔记评论
@xframe_options_exempt
@login_required()
def sectionComment(request):
    return render(request, 'layui-mini/management/sectionComment.html', locals())


# 笔记目录编排
@xframe_options_exempt
@login_required()
def sectionCatalog(request):
    note_all = Note.objects.all()
    return render(request, 'layui-mini/management/sectionCatalog.html', locals())


# 文章列表
@xframe_options_exempt
@login_required()
def sectionList(request):
    return render(request, 'layui-mini/management/sectionList.html', locals())


# 网站关于
@xframe_options_exempt
@login_required()
def websiteAbout(request):
    if request.method == "POST":
        try:
            about = About.objects.get(id=1)
            about.body = request.POST.get("content")
            about.save()
            result = {
                "code": "1",
                "msg": "修改成功!",
            }
        except Exception as e:
            print(e)
            result = {
                "code": "0",
                "msg": "修改失败!",
            }
        return JsonResponse(result)
    else:
        about = About.objects.get(id=1)
        body = about.body
        time = about.time
        return render(request, 'layui-mini/management/websiteAbout.html', locals())


# 网站配置
@xframe_options_exempt
@login_required()
def websiteConfig(request):
    if request.method == "POST":
        website = WebsiteConfig.objects.get(id=1)
        website.name = request.POST.get('sitename')
        website.domain = request.POST.get('domain')
        website.index_title = request.POST.get('title')
        website.keywords = request.POST.get('keywords')
        website.descript = request.POST.get('descript')
        website.copyright = request.POST.get('copyright')
        images = ImagesConfig.objects.get(id=1)
        images.foreground = request.POST.get('foreground')[6:]
        images.background = request.POST.get('background')[6:]
        images.icon = request.POST.get('icon')[6:]
        images.photo = request.POST.get('photo')[6:]
        images.cover = request.POST.get('cover')[6:]
        images.pay = request.POST.get('pay')[6:]
        try:
            website.save()
            images.save()
            result = {
                "code": "1",
                "msg": "修改成功！",
            }
        except Exception as e:
            print(e)
            result = {
                "code": "0",
                "msg": "修改成功！",
            }
        return JsonResponse(result)
    else:
        website = WebsiteConfig.objects.get(id=1)
        images = ImagesConfig.objects.get(id=1)
        return render(request, 'layui-mini/management/websiteConfig.html', locals())


# 博主信息
@xframe_options_exempt
@login_required()
def BloggerInfo(request):
    if request.method == 'POST':
        info = Info.objects.get(id=1)
        info.position = request.POST.get('position')
        info.company = request.POST.get('company')
        info.location = request.POST.get('location')
        info.email = request.POST.get('email')
        info.csdn = request.POST.get('csdn')
        info.github = request.POST.get('github')
        info.qq = request.POST.get('qq')[6:]
        info.weixin = request.POST.get('weixin')[6:]
        try:
            info.save()
            result = {
                "code": "1",
                "msg": "修改成功！",
            }
        except Exception as e:
            print(e)
            result = {
                "code": "0",
                "msg": "修改失败！",
            }
        return JsonResponse(result)
    else:
        info = Info.objects.get(id=1)
        return render(request, 'layui-mini/management/bloggerInfo.html', locals())


# 留言管理
@xframe_options_exempt
@login_required()
def websiteLeaveMessage(request):
    return render(request, 'layui-mini/management/websiteLeaveMessage.html', locals())


# 轮播图管理
@xframe_options_exempt
@login_required()
def websiteCarousel(request):
    return render(request, 'layui-mini/management/websiteCarousel.html', locals())


# 新增轮播图
@xframe_options_exempt
@login_required()
def carouselAdd(request):
    if request.method == 'POST':
        carousel = Carousel()
        carousel.info = request.POST.get('info')
        carousel.url = request.POST.get('url')
        carousel.img = request.POST.get('img')[6:]
        carousel.is_show = request.POST.get('is_show')
        try:
            carousel.save()
            result = {
                "code": "1",
                "msg": "添加成功！",
            }
        except Exception as e:
            print(e)
            result = {
                "code": "0",
                "msg": "添加失败！",
            }
        return JsonResponse(result)
    else:
        return render(request, 'layui-mini/management/carouselAdd.html', locals())


# 友情链接管理
@xframe_options_exempt
@login_required()
def websiteLink(request):
    return render(request, 'layui-mini/management/websiteLink.html', locals())


# 新增友情链接
@xframe_options_exempt
@login_required()
def linkAdd(request):
    if request.method == 'POST':
        link = Link()
        link.name = request.POST.get('name')
        link.url = request.POST.get('url')
        link.logo = request.POST.get('img')[6:]
        link.describe = request.POST.get('describe')
        link.type = request.POST.get('type')
        try:
            link.save()
            result = {
                "code": "1",
                "msg": "添加成功！",
            }
        except Exception as e:
            print(e)
            result = {
                "code": "0",
                "msg": "添加失败！",
            }
        return JsonResponse(result)
    else:
        return render(request, 'layui-mini/management/linkAdd.html', locals())


# 用户管理
@xframe_options_exempt
@login_required()
def managementUser(request):
    return render(request, 'layui-mini/management/managementUser.html', locals())


# ajax 文章封面图片上传
def coverUpload(request):
    if request.method == "POST":
        dir = 'cover/'
        file = request.FILES.get('file')
        filename = "%s.%s" % (timezone.now().strftime('%Y_%m_%d_%H_%M_%S_%f'), file.name.split('.')[-1])
        filepath = 'media/' + dir + filename
        # 图片资源写入服务器
        code = imgSave(file, filepath)
        if (code == 1):
            result = {
                "code": "1",
                "msg": "上传成功!",
                "src": filepath,
            }
            return JsonResponse(result)
        else:
            result = {
                "code": "0",
                "msg": "上传失败!",
                "src": None,
            }
        return JsonResponse(result)


# 新增文章
@xframe_options_exempt
@login_required()
def articleAdd(request):
    if request.method == "POST":
        title = request.POST.get("title")
        category_id = request.POST.get("category_id")
        excerpt = request.POST.get("excerpt")
        tags = request.POST.get("tags")
        cover_img = request.POST.get("cover_img")
        img = str(cover_img).split("media/")[1]
        content = request.POST.get("content")
        article_type = request.POST.get("type")
        recommended = request.POST.get("recommended")
        try:
            article = Article()
            article.title = title
            article.excerpt = excerpt
            article.img = img
            article.body = content
            article.author_id = request.user.id
            article.category_id = category_id
            article.is_recommend = recommended
            if article_type == 'release':
                article.is_release = 1
            elif article_type == 'save':
                article.is_release = 0
            article.save()
            article.tags.add(*list(Tag.objects.filter(id__in=tags.split(','))))
            result = {
                "code": "1",
                "msg": "提交成功！",
            }
        except Exception as e:
            print(e)
            result = {
                "code": "0",
                "msg": "提交失败！",
            }
        return JsonResponse(result)
    else:
        category_all = Category.objects.all()
        tag_all = Tag.objects.all()
        return render(request, 'layui-mini/management/articleAdd.html', locals())


# ajax删除文章
def articleDel(request):
    article_id = request.GET.get("del_id")
    article_arr = request.GET.get("delidArr")
    if article_id:
        Article.objects.get(id=article_id).delete()
        result = {"code": 1, "msg": "删除成功!"}
    elif article_arr:
        article_list = article_arr.split(',')
        for i in article_list:
            Article.objects.get(id=i).delete()
        result = {"code": 1, "msg": "删除成功!"}
    else:
        result = {"code": 0, "msg": "删除失败!"}
    return JsonResponse(result)


# ajax文章修改
@xframe_options_exempt
@login_required()
def articleEdit(request, article_id):
    if request.method == "POST":
        article_id = request.POST.get("id")
        title = request.POST.get("title")
        category_id = request.POST.get("category_id")
        excerpt = request.POST.get("excerpt")
        tags = request.POST.get("tags")
        cover_img = request.POST.get("cover_img")
        img = str(cover_img).split("media/")[1]
        content = request.POST.get("content")
        article_type = request.POST.get("type")
        recommended = request.POST.get("recommended")
        try:
            article = Article.objects.get(id=article_id)
            article.title = title
            article.excerpt = excerpt
            article.img = img
            article.body = content
            article.author_id = request.user.id
            article.category_id = category_id
            article.is_recommend = recommended
            if article_type == 'release':
                article.is_release = 1
            elif article_type == 'save':
                article.is_release = 0
            article.save()
            article.tags.clear()
            article.tags.add(*list(Tag.objects.filter(id__in=tags.split(','))))
            result = {
                "code": "1",
                "msg": "提交成功！",
            }
        except Exception as e:
            print(e)
            result = {
                "code": "0",
                "msg": "提交失败！",
            }
        return JsonResponse(result)
    else:
        article = Article.objects.get(id=article_id)
        category_all = Category.objects.all()
        tag_all = Tag.objects.all()
        tags = list(article.tags.values_list('id', flat=True))
        return render(request, 'layui-mini/management/articleEdit.html', locals())


# ajax删除文章分类
def categoryDel(request):
    category_id = request.GET.get("del_id")
    category_arr = request.GET.get("delidArr")
    if category_id:
        Category.objects.get(id=category_id).delete()
        result = {"code": 1, "msg": "删除成功!"}
    elif category_arr:
        category_list = category_arr.split(',')
        for i in category_list:
            Category.objects.get(id=i).delete()
        result = {"code": 1, "msg": "删除成功!"}
    else:
        result = {"code": 0, "msg": "删除失败!"}
    return JsonResponse(result)


# ajax修改文章分类
def categoryEdit(request):
    if request.method == "POST":
        category_id = request.POST.get("category_id")
        name = request.POST.get("name")
        try:
            category = Category.objects.get(id=category_id)
            category.name = name
            category.save()
            result = {
                "code": "1",
                "msg": "修改成功！",
            }
        except Exception as e:
            print(e)
            result = {
                "code": "0",
                "msg": "修改失败！",
            }
        return JsonResponse(result)


# ajax新增文章分类
def categoryAdd(request):
    if request.method == "POST":
        name = request.POST.get("name")
        try:
            category = Category()
            category.name = name
            category.save()
            result = {
                "code": "1",
                "msg": "添加成功！",
            }
        except Exception as e:
            print(e)
            result = {
                "code": "0",
                "msg": "添加失败！",
            }
        return JsonResponse(result)


# ajax添加文章标签
def tagAdd(request):
    if request.method == "POST":
        name = request.POST.get("name")
        try:
            tag = Tag()
            tag.name = name
            tag.save()
            result = {
                "code": "1",
                "msg": "添加成功！",
            }
        except Exception as e:
            print(e)
            result = {
                "code": "0",
                "msg": "添加失败！",
            }
        return JsonResponse(result)


# ajax 修改文章标签
def tagEdit(request):
    if request.method == "POST":
        tag_id = request.POST.get("tag_id")
        name = request.POST.get("name")
        try:
            tag = Tag.objects.get(id=tag_id)
            tag.name = name
            tag.save()
            result = {
                "code": "1",
                "msg": "修改成功！",
            }
        except Exception as e:
            print(e)
            result = {
                "code": "0",
                "msg": "修改失败！",
            }
        return JsonResponse(result)


# ajax删除标签
def tagDel(request):
    tag_id = request.GET.get("del_id")
    tag_arr = request.GET.get("delidArr")
    if tag_id:
        Tag.objects.get(id=tag_id).delete()
        result = {"code": 1, "msg": "删除成功!"}
    elif tag_arr:
        tag_list = tag_arr.split(',')
        for i in tag_list:
            Tag.objects.get(id=i).delete()
        result = {"code": 1, "msg": "删除成功!"}
    else:
        result = {"code": 0, "msg": "删除失败!"}
    return JsonResponse(result)


# ajax新增笔记名称
def noteAdd(request):
    if request.method == "POST":
        name = request.POST.get("name")
        try:
            note = Note()
            note.name = name
            note.save()
            result = {
                "code": "1",
                "msg": "添加成功！",
            }
        except Exception as e:
            print(e)
            result = {
                "code": "0",
                "msg": "添加失败！",
            }
        return JsonResponse(result)


# ajax删除笔记名
def noteDel(request):
    note_id = request.GET.get("del_id")
    note_arr = request.GET.get("delidArr")
    if note_id:
        Note.objects.get(id=note_id).delete()
        result = {"code": 1, "msg": "删除成功!"}
    elif note_arr:
        note_list = note_arr.split(',')
        for i in note_list:
            Note.objects.get(id=i).delete()
        result = {"code": 1, "msg": "删除成功!"}
    else:
        result = {"code": 0, "msg": "删除失败!"}
    return JsonResponse(result)


# ajax修改笔记名
def noteEdit(request):
    if request.method == "POST":
        note_id = request.POST.get("note_id")
        name = request.POST.get("name")
        try:
            note = Note.objects.get(id=note_id)
            note.name = name
            note.save()
            result = {
                "code": "1",
                "msg": "修改成功！",
            }
        except Exception as e:
            print(e)
            result = {
                "code": "0",
                "msg": "修改失败！",
            }
        return JsonResponse(result)


# ajax删除轮播图
def carouselDel(request):
    tag_id = request.GET.get("del_id")
    tag_arr = request.GET.get("delidArr")
    if tag_id:
        Carousel.objects.get(id=tag_id).delete()
        result = {"code": 1, "msg": "删除成功!"}
    elif tag_arr:
        tag_list = tag_arr.split(',')
        for i in tag_list:
            Carousel.objects.get(id=i).delete()
        result = {"code": 1, "msg": "删除成功!"}
    else:
        result = {"code": 0, "msg": "删除失败!"}
    return JsonResponse(result)


# ajax编辑轮播图
@xframe_options_exempt
@login_required()
def carouselEdit(request, carousel_id):
    if request.method == "POST":
        carousel = Carousel.objects.get(id=carousel_id)
        carousel.info = request.POST.get('info')
        carousel.url = request.POST.get('url')
        carousel.img = request.POST.get('img')[6:]
        carousel.is_show = request.POST.get('is_show')
        try:
            carousel.save()
            result = {
                "code": "1",
                "msg": "提交成功！",
            }
        except Exception as e:
            print(e)
            result = {
                "code": "0",
                "msg": "提交失败！",
            }
        return JsonResponse(result)
    else:
        carousel = Carousel.objects.get(id=carousel_id)
        return render(request, 'layui-mini/management/carouselEdit.html', locals())


# ajax友链删除
def linkDel(request):
    tag_id = request.GET.get("del_id")
    tag_arr = request.GET.get("delidArr")
    if tag_id:
        Link.objects.get(id=tag_id).delete()
        result = {"code": 1, "msg": "删除成功!"}
    elif tag_arr:
        tag_list = tag_arr.split(',')
        for i in tag_list:
            Link.objects.get(id=i).delete()
        result = {"code": 1, "msg": "删除成功!"}
    else:
        result = {"code": 0, "msg": "删除失败!"}
    return JsonResponse(result)


# ajax 编辑友链
@xframe_options_exempt
@login_required()
def linkEdit(request, link_id):
    if request.method == "POST":
        link = Link.objects.get(id=link_id)
        link.name = request.POST.get('name')
        link.url = request.POST.get('url')
        link.logo = request.POST.get('img')[6:]
        link.describe = request.POST.get('describe')
        link.type = request.POST.get('type')
        try:
            link.save()
            result = {
                "code": "1",
                "msg": "提交成功！",
            }
        except Exception as e:
            print(e)
            result = {
                "code": "0",
                "msg": "提交失败！",
            }
        return JsonResponse(result)
    else:
        link = Link.objects.get(id=link_id)
        return render(request, 'layui-mini/management/linkEdit.html', locals())


# ajax 删除用户
def userDel(request):
    tag_id = request.GET.get("del_id")
    tag_arr = request.GET.get("delidArr")
    if tag_id:
        User.objects.get(id=tag_id).delete()
        result = {"code": 1, "msg": "删除成功!"}
    elif tag_arr:
        tag_list = tag_arr.split(',')
        for i in tag_list:
            User.objects.get(id=i).delete()
        result = {"code": 1, "msg": "删除成功!"}
    else:
        result = {"code": 0, "msg": "删除失败!"}
    return JsonResponse(result)


# 新增笔记内容
@xframe_options_exempt
@login_required()
def sectionAdd(request):
    if request.method == "POST":
        title = request.POST.get("title")
        note_id = request.POST.get("note_id")
        father_id = request.POST.get("father_id")
        body = request.POST.get("body")
        type = request.POST.get("type")
        try:
            section = Section()
            section.title = title
            section.note_id = note_id
            section.body = body
            section.author_id = request.user.id
            if type == "release":
                section.is_release = 1
            else:
                section.is_release = 0
            section.save()
            catalogue = Catalogue()
            catalogue.note_id = note_id
            catalogue.father = father_id
            catalogue.name = title
            catalogue.section = Section.objects.get(id=section.id)
            catalogue.save()
            result = {
                "code": "1",
                "msg": "提交成功！",
            }
        except Exception as e:
            print(e)
            result = {
                "code": "0",
                "msg": "提交失败！",
            }
        return JsonResponse(result)
    else:
        note_all = Note.objects.all()
        return render(request, 'layui-mini/management/sectionAdd.html', locals())


# ajax删除笔记内容
def sectionDel(request):
    section_id = request.GET.get("del_id")
    section_arr = request.GET.get("delidArr")
    if section_id:
        Section.objects.get(id=section_id).delete()
        result = {"code": 1, "msg": "删除成功!"}
    elif section_arr:
        section_list = section_arr.split(',')
        for i in section_list:
            Section.objects.get(id=i).delete()
        result = {"code": 1, "msg": "删除成功!"}
    else:
        result = {"code": 0, "msg": "删除失败!"}
    return JsonResponse(result)


# ajax修改笔记内容
@xframe_options_exempt
@login_required()
def sectionEdit(request, section_id):
    if request.method == "POST":
        section_id = request.POST.get("id")
        title = request.POST.get("title")
        note_id = request.POST.get("note_id")
        father_id = request.POST.get("father_id")
        body = request.POST.get("content")
        section_type = request.POST.get("type")
        try:
            section = Section.objects.get(id=section_id)
            section.title = title
            section.body = body
            section.author_id = request.user.id
            section.note_id = note_id
            if section_type == 'release':
                section.is_release = 1
            elif section_type == 'save':
                section.is_release = 0
            section.save()
            catalogue = Catalogue.objects.filter(section=section.id)[0]
            catalogue.note_id = note_id
            catalogue.father = father_id
            catalogue.name = title
            catalogue.section = Section.objects.get(id=section.id)
            catalogue.save()
            result = {
                "code": "1",
                "msg": "提交成功！",
            }
        except Exception as e:
            print(e)
            result = {
                "code": "0",
                "msg": "提交失败！",
            }
        return JsonResponse(result)
    else:
        section = Section.objects.get(id=section_id)
        note_all = Note.objects.all()
        father_all = Catalogue.objects.filter(level=1)
        return render(request, 'layui-mini/management/sectionEdit.html', locals())


# ajax 修改目录结构
def catalogEdit(request):
    if request.method == 'POST':
        note_id = request.POST.get('note_id')
        catalog_data = request.POST.get('catalog_data')
        data_json = json.loads(catalog_data)
        try:
            if len(data_json) == Catalogue.objects.filter(note=note_id).filter(level=1).count():
                # 移动节点，未新增
                for i in range(len(data_json)):
                    father = Catalogue.objects.get(id=data_json[i]['id'])
                    father.name = data_json[i]['label']
                    father.save()
                    if 'children' in data_json[i].keys():
                        for j in range(len(data_json[i]['children'])):
                            children = Catalogue.objects.get(id=data_json[i]['children'][j]['id'])
                            children.order = j + 1
                            children.father = father.id
                            children.save()
            elif len(data_json) > Catalogue.objects.filter(note=note_id).filter(level=1).count():
                # 新增节点,有则改，无则加
                father_list = []
                father_all = Catalogue.objects.filter(note=note_id).filter(level=1)
                for i in father_all:
                    father_list.append(i.id)
                for i in range(len(data_json)):
                    if data_json[i]['id'] in father_list:
                        father = Catalogue.objects.get(id=data_json[i]['id'])
                        father.name = data_json[i]['label']
                        father.save()
                    else:
                        father = Catalogue()
                        father.note_id = note_id
                        father.name = data_json[i]['label']
                        father.order = i + 1
                        father.level = 1
                        father.father = None
                        father.section = None
                        father.save()
                        print(data_json[i])
                    if 'children' in data_json[i].keys():
                        for j in range(len(data_json[i]['children'])):
                            children = Catalogue.objects.get(id=data_json[i]['children'][j]['id'])
                            children.order = j + 1
                            children.father = father.id
                            children.save()
            else:
                # 删除节点,有则改，无则减
                father_list = []
                for i in range(len(data_json)):
                    father_list.append(data_json[i]['id'])
                father_all = Catalogue.objects.filter(note=note_id).filter(level=1)
                for i in father_all:
                    if i.id not in father_list:
                        father = Catalogue.objects.get(id=i.id)
                        father.delete()
                    else:
                        for j in data_json:
                            if i.id == j['id']:
                                father = Catalogue.objects.get(id=i.id)
                                father.name = j['label']
                                father.save()
            result = {
                "code": "1",
                "msg": "提交成功！",
            }
        except Exception as e:
            print(e)
            result = {
                "code": "0",
                "msg": "提交失败！",
            }
    else:
        note_id = request.GET.get("note_id")
        note = Note.objects.get(id=note_id)
        first_catalogue = Catalogue.objects.filter(note=note.id).filter(level=1)
        try:
            father_list = []
            for i in first_catalogue:
                father_dict = {}
                father_dict['id'] = i.id
                father_dict['name'] = i.name
                father_list.append(father_dict)
            catalogue_list = []
            for i in first_catalogue:
                catalogue_dict = {}
                catalogue_dict["id"] = i.id
                catalogue_dict["label"] = i.name
                catalogue_dict["isOpen"] = True
                children_list = []
                catalogue_dict["children"] = children_list
                second_catalogue = Catalogue.objects.filter(father=i.id)
                for j in second_catalogue:
                    children_dict = {}
                    children_dict["label"] = j.section.title
                    children_dict["id"] = j.id
                    children_list.append(children_dict)
                catalogue_list.append(catalogue_dict)
            result = {
                "father": father_list,
                "data": catalogue_list,
                "code": "1",
                "msg": "加载成功！",
            }
        except Exception as e:
            print(e)
            result = {
                "code": "0",
                "msg": "加载失败！",
            }
    return JsonResponse(result)


# echarts数据接口
def echartsData(request):
    datatype = request.GET.get("type")
    api = BaiduApi()
    # 近7天流量分析
    if datatype == "trend":
        data = {}
        trend = api.countTrend()
        trend_xAxis = trend["items"][0]
        xAxis = []
        for i in reversed(trend_xAxis):
            xAxis.append(i[0])
        data['xAxis'] = xAxis
        trend_data = trend["items"][1]
        pv = []
        uv = []
        add_user = []
        ip = []
        time = []
        page = []
        for i in reversed(trend_data):
            pv.append(i[0])
            uv.append(i[1])
            add_user.append(i[2])
            ip.append(i[3])
            time.append(i[4])
            page.append(i[5])
        data['pv'] = pv
        data['uv'] = uv
        data['add_user'] = add_user
        data['ip'] = ip
        data['time'] = time
        data['page'] = page
        result = {
            "data": data,
            "code": "1",
            "msg": "加载成功！",
        }
    # 受访页面统计
    elif datatype == 'page':
        data = {}
        page = api.countPage()
        page_xAxis = page["items"][0]
        xAxis = []
        for i in page_xAxis:
            if i[0]['name'][27:] == '':
                xAxis.append("/")
            else:
                xAxis.append(i[0]['name'][27:])
        data['xAxis'] = xAxis
        trend_data = page["items"][1]
        pv = []
        uv = []
        in_count = []
        time = []
        for i in trend_data:
            pv.append(i[0])
            uv.append(i[1])
            in_count.append(i[2])
            time.append(i[3])
        data['pv'] = pv
        data['uv'] = uv
        data['in_count'] = in_count
        data['time'] = time
        result = {
            "data": data,
            "code": "1",
            "msg": "加载成功！",
        }
    # 访客设备统计
    elif datatype == 'device':
        device = api.countDevice()
        data = {}
        data['pc'] = device['pc']
        data['mobile'] = device['mobile']
        result = {
            "data": data,
            "code": "1",
            "msg": "加载成功！",
        }
    # 访客区域统计
    elif datatype == 'map':
        map = api.countMap()
        data_count = []
        # data_rate = []
        pv_max = 0
        for i in range(len(map['items'][0])):
            pv_count = {}
            pv_count['name'] = map['items'][0][i][0]['name']
            pv_count['value'] = map['items'][1][i][0]
            if pv_max < map['items'][1][i][0]:
                pv_max = map['items'][1][i][0]
            data_count.append(pv_count)
            # pv_rate = {}
            # pv_rate['name'] = map['items'][0][i][0]['name']
            # pv_rate['value'] = map['items'][1][i][1]
            # data_rate.append(pv_rate)
        data = {}
        data['count'] = data_count
        data['pv_max'] = pv_max
        # data['rate'] = data_rate
        result = {
            "data": data,
            "code": "1",
            "msg": "加载成功！",
        }
    # 用户浏览趋势
    elif datatype == 'view':
        date_list = []
        for i in range(6, 0, -1):
            date_list.append((datetime.datetime.now() - datetime.timedelta(days=i)).strftime("%Y-%m-%d"))
        date_list.append(datetime.datetime.now().strftime("%Y-%m-%d"))
        article_view = []
        article_like = []
        article_comment = []
        section_view = []
        section_like = []
        section_comment = []
        for date in date_list:
            article_view.append(ArticleViewHistory.objects.filter(user=request.user).filter(time__date=date).count())
            article_like.append(
                ArticleViewHistory.objects.filter(user=request.user).filter(time__date=date).filter(is_like=1).count())
            article_comment.append(CommentMessage.objects.filter(user=request.user).filter(time__date=date).count())
            section_view.append(SectionViewHistory.objects.filter(user=request.user).filter(time__date=date).count())
            section_like.append(
                SectionViewHistory.objects.filter(user=request.user).filter(time__date=date).filter(is_like=1).count())
            section_comment.append(SectionMessage.objects.filter(user=request.user).filter(time__date=date).count())
        data = {}
        data['xAxis'] = date_list
        data['article_view'] = article_view
        data['article_like'] = article_like
        data['article_comment'] = article_comment
        data['section_view'] = section_view
        data['section_like'] = section_like
        data['section_comment'] = section_comment
        result = {
            "data": data,
            "code": "1",
            "msg": "加载成功！",
        }
    # 用户浏览文章分类统计
    elif datatype == 'category':
        category_list = []
        data = {}
        end_date = datetime.datetime.now().strftime("%Y-%m-%d") + ' 23:59:59'
        start_date = ((datetime.datetime.now() - datetime.timedelta(days=6)).strftime("%Y-%m-%d")) + ' 00:00:01'
        series = []
        for i in Category.objects.all():
            category_list.append(i.name)
            info = {}
            info['value'] = ArticleViewHistory.objects.filter(user=request.user).filter(time__range=[start_date, end_date]).filter(
                category=i).count()
            info['name'] = i.name
            series.append(info)
        data["legend"] = category_list
        data["series"] = series
        result = {
            "data": data,
            "code": "1",
            "msg": "加载成功！",
        }
    # 用户浏览笔记统计
    elif datatype == 'note':
        indicator = []
        serise = []
        data = {}
        end_date = datetime.datetime.now().strftime("%Y-%m-%d") + ' 23:59:59'
        start_date = ((datetime.datetime.now() - datetime.timedelta(days=6)).strftime("%Y-%m-%d")) + ' 00:00:01'
        for i in Note.objects.all():
            info = {}
            info['name'] = i.name
            info['max'] = 50
            indicator.append(info)
            serise.append(SectionViewHistory.objects.filter(user=request.user).filter(time__range=[start_date, end_date]).filter(
                note=i).count())
        data['indicator'] = indicator
        data['serise'] = serise
        result = {
            "data": data,
            "code": "1",
            "msg": "加载成功！",
        }
    # 用户浏览时间统计
    elif datatype == 'time':
        data = {}
        article_sum = []
        section_sum = []
        for i in range(6, -1, -1):
            if i == 6:
                # print("第一天")
                day = (datetime.datetime.now() - datetime.timedelta(days=i)).strftime("%Y-%m-%d")
                for j in range(0, 24, 2):
                    start_time = day + " " + str(j) + ":00:01"
                    end_time = day + " " + str(int(j) + 1) + ":59:59"
                    article_count = ArticleViewHistory.objects.filter(user=request.user).filter(
                        time__range=[start_time, end_time]).count()
                    section_count = SectionViewHistory.objects.filter(user=request.user).filter(
                        time__range=[start_time, end_time]).count()
                    article_sum.append(article_count)
                    section_sum.append(section_count)
            else:
                # print("不是第一天")
                day = (datetime.datetime.now() - datetime.timedelta(days=i)).strftime("%Y-%m-%d")
                for j in range(12):
                    start_time = day + " " + str(j * 2) + ":00:01"
                    end_time = day + " " + str(j * 2 + 1) + ":59:59"
                    article_count = ArticleViewHistory.objects.filter(user=request.user).filter(
                        time__range=[start_time, end_time]).count()
                    section_count = SectionViewHistory.objects.filter(user=request.user).filter(
                        time__range=[start_time, end_time]).count()
                    article_sum[j] = article_sum[j] + article_count
                    section_sum[j] = section_sum[j] + section_count
        data["article"] = article_sum
        data["section"] = section_sum
        result = {
            "data": data,
            "code": "1",
            "msg": "加载成功！",
        }
    return JsonResponse(result)
