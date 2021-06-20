from django.contrib import admin
from .models import UserInfo, ArticleViewHistory, LeaveMessage, CommentMessage, SectionViewHistory, SectionMessage


# Register your models here.


# 用户详细信息
@admin.register(UserInfo)
class RegisterAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone', 'sex', 'aboutme', 'web', 'photo')
    # 文章列表里显示想要显示的字段
    list_display_links = ('id', 'sex', 'phone')
    # 设置哪些字段可以点击进入编辑界面


# 用户博文浏览记录
@admin.register(ArticleViewHistory)
class ArticleViewHistoryAdmin(admin.ModelAdmin):
    list_display = ('article', 'category', 'user', 'time', 'is_like')
    # 文章列表里显示想要显示的字段
    list_display_links = ('article', 'category', 'is_like')
    # 设置哪些字段可以点击进入编辑界面


# 用户笔记浏览记录
@admin.register(SectionViewHistory)
class SectionViewHistoryAdmin(admin.ModelAdmin):
    list_display = ('section', 'note', 'user', 'time', 'is_like')
    # 文章列表里显示想要显示的字段
    list_display_links = ('section', 'note', 'is_like')
    # 设置哪些字段可以点击进入编辑界面


# 用户留言记录
@admin.register(LeaveMessage)
class LeaveMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'user', 'time', 'level', 'like', 'reply_id', 'root_id')
    list_display_links = ('content', 'user')


# 博文评论记录
@admin.register(CommentMessage)
class CommentMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'article', 'content', 'user', 'time', 'level', 'like', 'reply_id', 'root_id')
    list_display_links = ('content', 'user')


# 笔记评论记录
@admin.register(SectionMessage)
class SectionMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'section', 'content', 'user', 'time', 'level', 'like', 'reply_id', 'root_id')
    list_display_links = ('section', 'user')
