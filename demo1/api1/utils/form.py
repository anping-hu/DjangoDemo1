from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from api1.utils.encrypt import md5

# 定义一个ModelForm类从models.py文件里拿到Userinfo表的信息
from api1 import models
from api1.utils.bootstrap import BootStrapModelForm


class UserModelForm(BootStrapModelForm):
    name = forms.CharField(min_length=3, max_length=20, label="姓名")  # 重新定义name字段 如果你想做更多的校验就只有重写这个字段了，这个字段最小3最长20，标题是姓名

    class Meta:
        model = models.Userinfo
        fields = ["name", "password", "age", "account", "create_time", "depart", "gender"]


class PrettyModelForm(BootStrapModelForm):
    """ 创建一个靓号类 """

    # 验证：方式1
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机格式错误'), ],
    )  # 自定义校验字段的正确性 正则表达式

    # 验证：方式2
    def clean_mobile(self):
        tex_mobile = self.cleaned_data["mobile"]  # 拿到输入框里面的手机号
        exists = models.PrettyNum.objects.filter(mobile=tex_mobile).exists()  # 判断手机号在数据库中是否存在，返回True或false
        if exists:
            # 验证不通过
            raise ValidationError("手机号已存在")
        # 通过返回
        return tex_mobile

    class Meta:
        model = models.PrettyNum
        fields = ["mobile", "price", "level", "status"]


class PrettyEditModelForm(BootStrapModelForm):
    """ 创建一个靓号编辑类，手机号不能修改 """
    mobile = forms.CharField(disabled=True)

    class Meta:
        model = models.PrettyNum
        fields = ["mobile", "price", "level", "status"]


class AdminModelForm(BootStrapModelForm):
    """ 管理员添加类 """
    confirm_password = forms.CharField(label="确认密码",
                                       widget=forms.PasswordInput)  # 自定义字段 widget=forms.PasswordInput表示确认密码输入为***

    class Meta:
        model = models.Admin
        fields = ["username", "password", "confirm_password"]
        widgets = {
            "password": forms.PasswordInput
        }  # 表示密码这个字段输入为***在页面上

    def clean_password(self):
        """ 给密码加密 """
        pwd = self.cleaned_data.get("password")
        return md5(pwd)  # 利用自定义的MD5函数对密码加密,再将加密后的数据放入cleaned_data的password值中

    def clean_confirm_password(self):
        """ 验证密码是否一致 """
        # 在form.is_valid()验证提交的数据正确后，cleaned_data这个函数能拿到页面提交的数据
        pwd = self.cleaned_data.get("password")  # 页面的密码数据
        confirm = md5(self.cleaned_data.get("confirm_password"))  # 页面的确认密码数据
        if pwd != confirm:
            raise ValidationError("密码不一致")
        return confirm  # 最后return confirm，是将confirm的值重新放到cleaned_data的confirm_password值这个里面去


class AdminEditModelForm(BootStrapModelForm):
    """ 编辑管理员类 """

    class Meta:
        model = models.Admin
        fields = ["username"]  # 只让编辑用户名


class AdminResetModelForm(BootStrapModelForm):
    """ 管理员重置密码类 """
    confirm_password = forms.CharField(label="确认密码", widget=forms.PasswordInput)

    class Meta:
        model = models.Admin
        fields = ["password", "confirm_password"]  # 只让编辑密码和确认密码
        widgets = {
            "password": forms.PasswordInput
         }

    def clean_password(self):
        """ 给密码加密 """
        pwd = self.cleaned_data.get("password")
        md5_pwd = md5(pwd)  # 网页上输入的密码
        db_pwd = models.Admin.objects.filter(id=self.instance.pk).first().password  # 数据库里拿到的密码
        if md5_pwd == db_pwd:
            raise ValidationError("密码不能与上一次一样") 
        return md5_pwd

    def clean_confirm_password(self):
        """ 验证密码是否一致 """

        pwd = self.cleaned_data.get("password")  # 页面的密码数据
        confirm = md5(self.cleaned_data.get("confirm_password"))  # 页面的确认密码数据
        if pwd != confirm:
            raise ValidationError("密码不一致")
        return confirm
