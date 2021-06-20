from django.contrib import admin
from management.models import Carousel, Link, About, WebsiteConfig, Info, ImagesConfig


# Register your models here.


# 轮播图
@admin.register(Carousel)
class CarouselAdmin(admin.ModelAdmin):
    list_display = ('id', 'info', 'img', 'url', 'is_show')


# 友情链接
@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'logo', 'name', 'url', 'describe', 'type')


# 关于
@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('id', 'time')


# 网站配置
@admin.register(WebsiteConfig)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('name', 'domain', 'index_title', 'keywords', 'descript', 'copyright')


# 图片配置
@admin.register(ImagesConfig)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('foreground', 'background', 'icon', 'photo', 'cover', 'pay')


# 博主信息
@admin.register(Info)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('position', 'company', 'location', 'email', 'csdn', 'github', 'qq', 'weixin')
