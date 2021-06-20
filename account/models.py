from django.contrib.auth.models import User
from blog.models import Article, Category, Section, Note
from django.db import models


# Create your models here.
# 用户详细信息表，信息可以为空


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    # 与自带用户表一对一
    phone = models.CharField(verbose_name='手机号', max_length=20, default="保密")
    sex_choice = [('1', '男'), ('2', '女')]
    sex = models.CharField(verbose_name='性别', max_length=1, choices=sex_choice, default=1)
    web = models.CharField(verbose_name='个人网站', max_length=50, default="#")
    aboutme = models.TextField(verbose_name='个性签名', max_length=200, default="这个人很懒，什么都没留下！")
    photo = models.ImageField(upload_to='photo/', verbose_name='头像', default='photo/default.jpg')

    class Meta:
        verbose_name = '用户详细信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "user:{}".format(self.user.username)


class ArticleViewHistory(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, blank=True, null=True, verbose_name='文章名')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, verbose_name='所属分类')
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='用户名')
    time = models.DateTimeField(auto_now_add=True, verbose_name='浏览时间')
    is_like = models.BooleanField(verbose_name='是否收藏', default=0)

    class Meta:
        ordering = ('-time',)
        verbose_name = '博文浏览记录'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "article:{0},username:{1}".format(self.article, self.user.username)


class SectionViewHistory(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, blank=True, null=True, verbose_name='笔记标题')
    note = models.ForeignKey(Note, on_delete=models.CASCADE, blank=True, null=True, verbose_name='所属笔记')
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='用户名')
    time = models.DateTimeField(auto_now_add=True, verbose_name='浏览时间')
    is_like = models.BooleanField(verbose_name='是否收藏', default=0)

    class Meta:
        ordering = ('-time',)
        verbose_name = '笔记浏览记录'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "content:{0},username:{1}".format(self.section, self.user.username)


class LeaveMessage(models.Model):
    content = models.TextField(verbose_name='留言内容', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='用户名')
    time = models.DateTimeField(auto_now_add=True, verbose_name='留言时间')
    level = models.IntegerField(verbose_name='留言等级', default=0)
    like = models.IntegerField(verbose_name='留言点赞数', default=0)
    reply_id = models.IntegerField(verbose_name='回复留言ID', blank=True, null=True, default=None)
    root_id = models.IntegerField(verbose_name='根留言ID', blank=True, null=True, default=None)

    class Meta:
        ordering = ('root_id', 'level', '-time')
        verbose_name = '留言回复记录'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "content:{0},username:{1}".format(self.content, self.user.username)


class CommentMessage(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, blank=True, null=True, verbose_name='文章')
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='用户名')
    content = models.TextField(verbose_name='评论内容', blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    level = models.IntegerField(verbose_name='评论等级', default=0)
    like = models.IntegerField(verbose_name='评论点赞数', default=0)
    reply_id = models.IntegerField(verbose_name='回复评论ID', blank=True, null=True, default=None)
    root_id = models.IntegerField(verbose_name='回复根ID', blank=True, null=True, default=None)

    class Meta:
        ordering = ('root_id', 'level', '-time')
        verbose_name = '博文评论回复记录'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "content:{0},username:{1}".format(self.content, self.user.username)


class SectionMessage(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, blank=True, null=True, verbose_name='笔记')
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='用户名')
    content = models.TextField(verbose_name='评论内容', blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    level = models.IntegerField(verbose_name='评论等级', default=0)
    like = models.IntegerField(verbose_name='评论点赞数', default=0)
    reply_id = models.IntegerField(verbose_name='回复评论ID', blank=True, null=True, default=None)
    root_id = models.IntegerField(verbose_name='回复根ID', blank=True, null=True, default=None)

    class Meta:
        ordering = ('root_id', 'level', '-time')
        verbose_name = '笔记评论回复记录'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "content:{0},username:{1}".format(self.section, self.user.username)
