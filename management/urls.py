from django.urls import path
from . import views

app_name = "management"

urlpatterns = [
    path('', views.management, name='management'),
    # 后台管理模块
    path('dashboard/', views.dashboard, name='dashboard'),
    # 后台管理dashboard
    path('articleAdd/', views.articleAdd, name='articleAdd'),
    # 新增文章
    path('articleList/', views.articleList, name='articleList'),
    # 文章列表
    path('articleCategory/', views.articleCategory, name='articleCategory'),
    # 文章分类
    path('articleTag/', views.articleTag, name='articleTag'),
    # 文章标签
    path('articleComment/', views.articleComment, name='articleComment'),
    # 文章评论
    path('sectionNote/', views.sectionNote, name='sectionNote'),
    # 笔记名称
    path('sectionList/', views.sectionList, name='sectionList'),
    # 笔记列表
    path('sectionAdd/', views.sectionAdd, name='sectionAdd'),
    # 新增笔记内容
    path('sectionComment/', views.sectionComment, name='sectionComment'),
    # 笔记评论
    path('sectionCatalog/', views.sectionCatalog, name='sectionCatalog'),
    # 笔记目录编排
    path('websiteLeaveMessage/', views.websiteLeaveMessage, name='websiteLeaveMessage'),
    # 网站留言
    path('websiteCarousel/', views.websiteCarousel, name='websiteCarousel'),
    # 网站轮播图
    path('carouselAdd/', views.carouselAdd, name='carouselAdd'),
    # 新增轮播图
    path('websiteLink/', views.websiteLink, name='websiteLink'),
    # 网站友情链接
    path('linkAdd/', views.linkAdd, name='linkAdd'),
    # 新增友情链接
    path('websiteAbout/', views.websiteAbout, name='websiteAbout'),
    # 网站关于
    path('websiteConfig/', views.websiteConfig, name='websiteConfig'),
    # 网站配置
    path('BloggerInfo/', views.BloggerInfo, name='BloggerInfo'),
    # 博主信息
    path('managementUser/', views.managementUser, name='managementUser'),
    # 用户管理

    path('coverUpload/', views.coverUpload, name='coverUpload'),
    # ajax文章封面图片上传
    path('articleDel/', views.articleDel, name='articleDel'),
    # ajax删除文章
    path('articleEdit-<int:article_id>/', views.articleEdit, name='articleEdit'),
    # ajax修改文章
    path('categoryDel/', views.categoryDel, name='categoryDel'),
    # ajax删除分类
    path('categoryEdit/', views.categoryEdit, name='categoryEdit'),
    # ajax修改分类
    path('categoryAdd/', views.categoryAdd, name='categoryAdd'),
    # ajax新增分类
    path('tagAdd/', views.tagAdd, name='tagAdd'),
    # ajax新增标签
    path('tagEdit/', views.tagEdit, name='tagEdit'),
    # ajax修改标签
    path('tagDel/', views.tagDel, name='tagDel'),
    # ajax删除标签
    path('noteAdd/', views.noteAdd, name='noteAdd'),
    # ajax新增笔记名称
    path('noteDel/', views.noteDel, name='noteDel'),
    # ajax删除笔记名称
    path('noteEdit/', views.noteEdit, name='noteEdit'),
    # ajax修改笔记名称
    path('sectionDel/', views.sectionDel, name='sectionDel'),
    # ajax删除笔记内容
    path('sectionEdit-<int:section_id>/', views.sectionEdit, name='sectionEdit'),
    # ajax修改笔记内容
    path('catalogEdit/', views.catalogEdit, name='catalogEdit'),
    # ajax获取章节名称
    path('carouselDel/', views.carouselDel, name='carouselDel'),
    # ajax删除轮播图
    path('carouselEdit-<int:carousel_id>/', views.carouselEdit, name='carouselEdit'),
    # ajax编辑轮播图
    path('linkDel/', views.linkDel, name='linkDel'),
    # ajax删除友链
    path('linkEdit-<int:link_id>/', views.linkEdit, name='carouselEdit'),
    # ajax编辑友链
    path('userDel/', views.userDel, name='userDel'),
    # ajax删除用户
    path('echartsData', views.echartsData, name='echartsData'),
    # ajax echarts数据接口
]
