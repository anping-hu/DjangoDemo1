from django.shortcuts import render, HttpResponse, redirect
from api1 import models
from api1.utils.pagination import Pagination
from api1.utils.form import UserModelForm


def user_list(request):
    """ 用户管理 """
    userinfo = models.Userinfo.objects.all()
    # 分页
    page_object = Pagination(request, userinfo)

    context = {
        "userinfo": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 生成页码
    }
    return render(request, 'user_list.html', context)


def user_add(request):
    """ 添加用户 """
    if request.method == "GET":
        myform = UserModelForm()  # 实例化
        return render(request, 'user_add.html', {'form': myform})

    # 用户POST提交数据，数据校验
    myform = UserModelForm(data=request.POST)
    if myform.is_valid():
        # 如果数据合法不为空,调用ModelForm类的save()函数自动保存到数据库
        myform.save()
        return redirect("/user/list/")
    # 校验失败，在页面上展示错误信息
    return render(request, 'user_add.html', {'form': myform})


def user_edit(request, nid):
    """ 用户编辑 """
    # 根据nid去数据库找到编辑哪一行的数据(对象)
    row_obj = models.Userinfo.objects.filter(id=nid).first()

    if request.method == 'GET':
        myform = UserModelForm(instance=row_obj)  # 实例化,instance-实例，在modelForm中instance这个属性有值，它会默认显示拿到的值
        return render(request, 'user_edit.html', {'form': myform})

    # 用户POST提交数据，数据校验
    myform = UserModelForm(data=request.POST, instance=row_obj)
    if myform.is_valid():
        # 如果数据合法不为空,调用ModelForm类的save()函数自动保存到数据库
        myform.save()
        return redirect("/user/list/")
        # 校验失败，在页面上展示错误信息
    return render(request, 'user_edit.html', {'form': myform})


def user_delete(request, nid):
    """ 用户删除 """
    models.Userinfo.objects.filter(id=nid).delete()
    return redirect('/user/list')