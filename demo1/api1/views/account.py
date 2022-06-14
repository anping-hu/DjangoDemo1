"""
登录视图
"""
from io import BytesIO

from django.shortcuts import render, redirect, HttpResponse
from django import forms

from api1 import models
from api1.utils.encrypt import md5
from api1.utils.code import check_code


class LoginForm(forms.Form):
    username = forms.CharField(label="用户名", widget=forms.TextInput, required=True)
    password = forms.CharField(label="密码", widget=forms.PasswordInput, required=True)
    code = forms.CharField(label="验证码", widget=forms.TextInput, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环ModelForm中的所有字段，给每个字段的插件设置
        for name, field in self.fields.items():
            # 字段中有属性，保留原来的属性，没有属性，才增加。
            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = field.label
            else:
                field.widget.attrs = {
                    "class": "form-control",
                    "placeholder": field.label
                }

    # 勾子方法，修改密码的值
    def clean_password(self):
        pwd = self.cleaned_data.get("password")  # 拿到页面上的密码
        md5_pwd = md5(pwd)  # md5加密
        return md5_pwd  # 返回加密后的密码


def login(request):
    """ 登录 """
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 数据都不为空后
        # form.cleaned_data中就保存着（{‘username’： ‘huanping’， ‘password’：‘60af3df8262eb0f2d5631a38d2f6f074’， 'code': XXX}）
        # 验证码的校验
        user_input_code = form.cleaned_data.pop('code')     # 页面上输入的验证码
        # pop函数：将cleaned_data中的code拿到后，在cleaned_data中将code去除掉，因为下面的**form.cleaned_data里面只要username和password
        # session中的验证码,如果超时后image_code为none时，默认没空，.upper()表示全部变大写
        code = request.session.get('image_code', '')
        if user_input_code.upper() != code.upper():
            form.add_error("code", "验证码错误")
            return render(request, 'login.html', {'form': form})

        # 将网页上的用户名和密码拿到数据库去对比
        model_obj = models.Admin.objects.filter(**form.cleaned_data).first()
        if not model_obj:  # 如果没有
            form.add_error("password", "用户名或密码错误")
            return render(request, 'login.html', {'form': form})
        # 用户名和密码正确
        # 网站生成随机字符串，写到用户浏览器的cookie中；再写入到session中；
        request.session["info"] = {'id': model_obj.id, 'name': model_obj.username}
        request.session.set_expiry(60 * 60 * 24 * 7)
        # 因为之前图片验证码的时候设置了session的超时为60秒，在登录成功后需要重新设置session超时时间，表示session超时为7天
        return redirect("/admin/list/")

    return render(request, 'login.html', {"form": form})


def image_code(request):
    """ 生成图片验证码 """

    img, code_string = check_code()  # 利用自定义的函数返回图片（img）和图片中的字符串（code_string）

    request.session['image_code'] = code_string     # 将图片中的字符串保存到session中
    request.session.set_expiry(60)      # 设置60秒的超时，超过时间验证码就无效了

    stream = BytesIO()  # 在内存中定义一块区域
    img.save(stream, 'png')  # 将图片保存到内存中
    return HttpResponse(stream.getvalue())  # 将图片显示出来


def logout(request):
    """ 注销 """
    request.session.clear()  # 将当前用户的session清楚掉
    return redirect("/login/")
