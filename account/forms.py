from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.models import User
from account.models import UserInfo


# 用户登录表单
class LoginForm(forms.Form):
    user = forms.CharField(
        label='用户名',
        max_length=20,
        error_messages={'required': '用户名或邮箱号不能为空'},
        widget=forms.TextInput(attrs={'class': 'form-style',
                                      'placeholder': '用户名或邮箱号',
                                      'lay-verify': 'required',
                                      'lay-reqtext': '请输入用户名或邮箱号！'}))
    password = forms.CharField(
        max_length=16,
        error_messages={'required': '密码不能为空'},
        widget=forms.PasswordInput(attrs={'class': 'form-style',
                                          'placeholder': '密码',
                                          'lay-verify': 'required',
                                          'autocomplete': 'off',
                                          'lay-reqtext': '请输入密码！'}))

    captcha = CaptchaField(
        required=True,
        error_messages={'required': '验证码不能为空'})

    # 用户注册表单


# 用户注册表单
class RegisterForm(forms.ModelForm):
    email_code = forms.CharField(max_length=6,
                                 error_messages={'required': '邮箱验证码不能为空'},
                                 widget=forms.TextInput(attrs={'class': 'form-style',
                                                               'placeholder': '邮箱验证码',
                                                               'lay-verify': 'required',
                                                               'lay-reqtext': '请输入邮件验证码！'}))
    password1 = forms.CharField(max_length=20,
                                error_messages={'required': '密码不能为空'},
                                widget=forms.PasswordInput(attrs={'class': 'form-style',
                                                                  'placeholder': '密码',
                                                                  'lay-verify': 'password|password_same',
                                                                  'autocomplete': 'off',
                                                                  'lay-reqtext': '请输入密码！'}))
    password2 = forms.CharField(max_length=20,
                                error_messages={'required': '密码不能为空'},
                                widget=forms.PasswordInput(attrs={'class': 'form-style',
                                                                  'placeholder': '确认密码',
                                                                  'lay-verify': 'password|password_same',
                                                                  'autocomplete': 'off',
                                                                  'lay-reqtext': '请输入确认密码！'}))

    class Meta:
        model = User
        fields = ("username", "email")
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': '用户名', 'class': 'form-style',
                                               'lay-verify': 'username|check_username', 'lay-reqtext': '请输入用户名！'}),
            'email': forms.EmailInput(attrs={'placeholder': '邮箱号', 'class': 'form-style',
                                             'lay-verify': 'email|check_email', 'lay-reqtext': '请输入邮箱号！'})
        }


# 重置密码表单
class ForgetForm(forms.ModelForm):
    email_code = forms.CharField(max_length=6,
                                 error_messages={'required': '邮箱验证码不能为空'},
                                 widget=forms.EmailInput(attrs={'class': 'form-style',
                                                                'placeholder': '邮箱验证码',
                                                                'lay-verify': 'required',
                                                                'lay-reqtext': '请输入邮件验证码！'}))
    password1 = forms.CharField(max_length=20,
                                error_messages={'required': '密码不能为空'},
                                widget=forms.PasswordInput(attrs={'class': 'form-style',
                                                                  'placeholder': '密码',
                                                                  'lay-verify': 'password|password_same',
                                                                  'autocomplete': 'off',
                                                                  'lay-reqtext': '请输入密码！'}))
    password2 = forms.CharField(max_length=20,
                                error_messages={'required': '密码不能为空'},
                                widget=forms.PasswordInput(attrs={'class': 'form-style',
                                                                  'placeholder': '确认密码',
                                                                  'lay-verify': 'password|password_same',
                                                                  'autocomplete': 'off',
                                                                  'lay-reqtext': '请输入确认密码！'}))

    class Meta:
        model = User
        fields = ("email",)
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': '邮箱号', 'class': 'form-style',
                                             'lay-verify': 'email|check_email', 'lay-reqtext': '请输入邮箱号！'})
        }


# 修改密码表单
class ChangePasswordForm(forms.Form):
    password_old = forms.CharField(
        label='当前密码',
        max_length=20,
        error_messages={'required': '当前密码不能为空'},
        widget=forms.PasswordInput(attrs={'class': 'layui-input', 'lay-verify': 'required',
                                          'autocomplete': 'off', 'lay-reqtext': '请输入当前密码！'}))
    password1 = forms.CharField(
        label='新密码',
        max_length=20,
        error_messages={'required': '新密码不能为空'},
        widget=forms.PasswordInput(attrs={'class': 'layui-input', 'lay-verify': 'password|password_same',
                                          'autocomplete': 'off', 'lay-reqtext': '请输入新密码！'}))
    password2 = forms.CharField(
        label='确认密码',
        max_length=20,
        error_messages={'required': '确认密码不能为空'},
        widget=forms.PasswordInput(attrs={'class': 'layui-input', 'lay-verify': 'password|password_same',
                                          'autocomplete': 'off', 'lay-reqtext': '请输入确认密码！'}))


# 修改邮箱表单
class ChangeEmailForm(forms.Form):
    password = forms.CharField(
        label='当前密码:',
        max_length=20,
        error_messages={'required': '当前密码不能为空'},
        widget=forms.PasswordInput(attrs={'class': 'layui-input', 'lay-verify': 'required',
                                          'autocomplete': 'off', 'lay-reqtext': '请输入当前密码！'}))
    email = forms.CharField(
        label='新邮箱号:',
        max_length=20,
        error_messages={'required': '新邮箱号不能为空'},
        widget=forms.EmailInput(attrs={'class': 'layui-input', 'lay-verify': 'email',
                                       'autocomplete': 'off', 'lay-reqtext': '请输入新邮箱号！'}))
    email_code = forms.CharField(
        label='邮箱验证码:',
        max_length=6,
        error_messages={'required': '确认密码不能为空'},
        widget=forms.TextInput(attrs={'class': 'layui-input', 'lay-verify': 'required',
                                      'autocomplete': 'off', 'lay-reqtext': '请输入邮箱验证码！'}))


# 用户修改信息表单
class UserInfoForm(forms.ModelForm):
    sex_choice = [('1', '男'), ('2', '女')]
    sex = forms.ChoiceField(choices=sex_choice, widget=forms.RadioSelect)

    class Meta:
        model = UserInfo
        fields = ("phone", "sex", "web", "aboutme")
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'layui-input'}),
            'web': forms.TextInput(attrs={'class': 'layui-input'}),
            'aboutme': forms.Textarea(attrs={'class': 'layui-textarea', 'rows': 5}),
        }


# 用户信息表单
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email", "username")
        widgets = {
            'username': forms.TextInput(attrs={'lay-verify': "username", 'class': 'layui-input'}),
            'email': forms.EmailInput(attrs={'readonly': 'readonly', 'class': 'layui-input'})
        }
