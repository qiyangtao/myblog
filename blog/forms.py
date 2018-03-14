# -*- coding:utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError, ViewDoesNotExist


# 登录
class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "用户名", "required": "required",}),
                               max_length=30,error_messages={"required": "用户名不能为空",})
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "密码", "required": "required",}),
                              max_length=15,error_messages={"required": "密码不能为空",})


# 注册
class RegForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "用户名", "required": "required",}),
                               max_length=30,error_messages={"required": "用户名不能为空",})
    email = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "个人邮箱", "required": "required",}),
                               max_length=30,error_messages={"required": "邮箱不能为空",})
    url = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "个人地址", "required": "required",}),
                               max_length=50,error_messages={"required": "个人地址不能为空",})
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "请输入密码", "required": "required",}),
                               max_length=15,error_messages={"required": "密码不能为空",})
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "请再次输入密码", "required": "required",}),
                               max_length=15,)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise ValidationError('密码不一致!')


class CommentForm(forms.Form):
    '''
    评论表单
    '''
    author = forms.CharField(widget=forms.TextInput(attrs={"id": "author", "class": "comment_input",
                                                           "required": "required","size": "25", "tabindex": "1"}),
                              max_length=50,error_messages={"required":"username不能为空",})
    email = forms.EmailField(widget=forms.TextInput(attrs={"id":"email","type":"email","class": "comment_input",
                                                           "required":"required","size":"25", "tabindex":"2"}),
                                 max_length=50, error_messages={"required":"email不能为空",})
    url = forms.URLField(widget=forms.TextInput(attrs={"id":"url","type":"url","class": "comment_input",
                                                       "size":"25", "tabindex":"3"}),
                              max_length=100, required=False)
    comment = forms.CharField(widget=forms.Textarea(attrs={"id":"comment","class": "message_input",
                                                           "required": "required", "cols": "25",
                                                           "rows": "5", "tabindex": "4"}),
                                                    error_messages={"required":"评论不能为空",})
    article = forms.CharField(widget=forms.HiddenInput())
