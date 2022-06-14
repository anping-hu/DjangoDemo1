import os
from django.conf import settings
from django.shortcuts import render, HttpResponse
from api1 import models
from django import forms
from api1.utils.bootstrap import BootStrapForm, BootStrapModelForm


class UpForm(BootStrapForm):
    bootstrap_exclude_fields = ['img']

    name = forms.CharField(label="姓名")
    age = forms.IntegerField(label="年龄")
    img = forms.FileField(label="头像")


def upload_form(request):
    title = "Form上传"
    if request.method == "GET":
        form = UpForm()
        return render(request, 'upload_form.html', {"form": form, "title": title})

    form = UpForm(data=request.POST, files=request.FILES)  # 表单的数据会放在request.POST中，文件会放在request.FILES中
    if form.is_valid():
        # {'name': '武沛齐', 'age': 123, 'img': <InMemoryUploadedFile: 图片 1.png (image/png)>}
        # 1.读取图片内容，写入到文件夹中并获取文件的路径。
        image_object = form.cleaned_data.get("img")

        # media_path = os.path.join(settings.MEDIA_ROOT, image_object.name)
        media_path = os.path.join("media", image_object.name)  # media_path-文件存储路径，media-用户上传的文件都放在这个文件里
        # os.path.join('static','1.png') 代表 static/1.png
        f = open(media_path, mode='wb')  # 打开文件，写方式
        for chunk in image_object.chunks():  # 循环写入
            f.write(chunk)
        f.close()  # 关闭文件

        # 2.将图片文件路径写入到数据库
        models.Boss.objects.create(
            name=form.cleaned_data['name'],
            age=form.cleaned_data['age'],
            img=media_path,
        )
        return HttpResponse("提交成功")
    return render(request, 'upload_form.html', {"form": form, "title": title})


class UpModelForm(BootStrapModelForm):
    bootstrap_exclude_fields = ['img']      # img这个字段不要BootStrap样式

    class Meta:
        model = models.City
        fields = "__all__"


def upload_modal_form(request):
    """ 上传文件和数据（modelForm）"""
    title = "ModelForm上传文件"
    if request.method == "GET":
        form = UpModelForm()
        return render(request, 'upload_form.html', {"form": form, 'title': title})

    form = UpModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # 对于文件：自动保存；
        # 字段 + 上传路径写入到数据库
        form.save()

        return HttpResponse("成功")
    return render(request, 'upload_form.html', {"form": form, 'title': title})
