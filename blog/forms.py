from django import forms


# 文章搜索表单
class searchForm(forms.Form):
    key = forms.CharField(
        label='用户名',
        max_length=20,
        error_messages={'required': '用户名或邮箱号不能为空'},
        widget=forms.TextInput(attrs={'class': 'form-style',
                                      'placeholder': '搜标题，搜内容',
                                      'lay-verify': 'required',
                                      'lay-reqtext': '请输入关键字！'}))
