# -*- coding: utf-8 -*-
import logging
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import *
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from models import *
from forms import *

logger = logging.getLogger('blog.view')


# Create your views here.
def global_setting(request):
    category_list = Category.objects.all()
    date_list = Article.objects.date_distinct()
    return {
        'category_list':category_list,
        'date_list':date_list,
        'SITE_NAME' : settings.SITE_NAME,
        'SITE_DESC' : settings.SITE_DESC,
    }

#首页
def index(request):
    try:
        article_list = archive_auto(request, Article.objects.all())
    except Exception as e:
        logger.error(e)
    return render(request, 'index.html', locals())

#文章归档
def archive(request):
    try:
        year = request.GET.get('year', None)
        month = request.GET.get('month', None)
        article_list = archive_auto(request, Article.objects.filter(date_publish__icontains=year + '-' + month))
    except Exception as e:
        logger.error(e)
    return render(request, 'archive.html', locals())

#自动分页
def archive_auto(request, article_list):
    paginator = Paginator(article_list, 3)
    try:
        page_num = int(request.GET.get('page', 1))
        article_list = paginator.page(page_num)
    except (EmptyPage, PageNotAnInteger, InvalidPage):
        article_list = paginator.page(1)
    return article_list

#文章详情页
# 文章详情
def article(request):
    try:
        # 获取文章id
        id = request.GET.get('id', None)
        try:
            # 获取文章信息
            article = Article.objects.get(pk=id)
        except Article.DoesNotExist:
            return render(request, 'failure.html', {'reason': '没有找到对应的文章'})

        # 评论表单
        comment_form = CommentForm({'author': request.user.username,
                                    'email': request.user.email,
                                    'url': request.user.url,
                                    'article': id} if request.user.is_authenticated() else{'article': id})
        # 获取评论信息
        comments = Comment.objects.filter(article=article).order_by('id')
        comment_list = []
        for comment in comments:
            for item in comment_list:
                if not hasattr(item, 'children_comment'):
                    setattr(item, 'children_comment', [])
                if comment.pid == item:
                    item.children_comment.append(comment)
                    break
            if comment.pid is None:
                comment_list.append(comment)
    except Exception as e:
        print e
        logger.error(e)
    return render(request, 'article.html', locals())


#登录
def login_do(request):
    try:
        if request.method == 'POST':
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data["username"]
                password = login_form.cleaned_data["password"]
                user = authenticate(username = username, password = password)
                print(request.META['HTTP_REFERER'])
                if user is not None:
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request, user)
                else:
                    return render(request, 'failure.html', {'reason':"登录验证失败！"})
                return redirect(request.POST.get('source_url'))
            else:
                return render(request, 'failure.html', {'reason':login_form.errors})
        else:
            login_form = LoginForm()
    except Exception as e:
        logger.error(e)
    return render(request, 'login.html', locals())


# 注册
def region_do(request):
    try:
        if request.method == 'POST':
            reg_form = RegForm(request.POST)
            if reg_form.is_valid():
                user = User.objects.create(username=reg_form.cleaned_data["username"],
                                           password=make_password(reg_form.cleaned_data["password1"]),
                                           email=reg_form.cleaned_data["email"],
                                           url=reg_form.cleaned_data["url"],)
                user.save()
                user.backend = 'django.contrib.auth.backends.ModelBackend'# 指定默认的登录验证方式
                login(request, user)
                return redirect(request.POST.get('source_url'))
            else:
                return render(request, 'failure.html', {'reason': reg_form.errors})
        else:
            reg_form = RegForm()
    except Exception as e:
        logger.error(e)
    return render(request, 'reg.html', locals())


#注销
def logoff(request):
    try:
        logout(request)
    except Exception as e:
        print("注销有问题")
        logger.error(e)
    return redirect(request.META['HTTP_REFERER'])

# 提交评论
def  comment_post(request):
    try:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            #获取表单信息
            comment = Comment.objects.create(username=comment_form.cleaned_data["author"],
                                             email=comment_form.cleaned_data["email"],
                                             url=comment_form.cleaned_data["url"],
                                             content=comment_form.cleaned_data["comment"],
                                             article_id=comment_form.cleaned_data["article"],
                                             user=request.user if request.user.is_authenticated() else None)
            comment.save()
        else:
            return render(request, 'failure.html', {'reason': comment_form.errors})
    except Exception as e:
        logger.error(e)
    return redirect(request.META['HTTP_REFERER'])