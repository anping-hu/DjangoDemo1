from django.shortcuts import render, redirect

from api1 import models
from api1.utils.pagination import Pagination
from api1.utils.form import AdminModelForm, AdminEditModelForm, AdminResetModelForm


def admin_list(request):
    """ 管理员列表 """

    # 搜索值
    data_dict = {}
    search_data = request.GET.get("q", '')
    if search_data:
        data_dict["username__contains"] = search_data

    # 符合搜索条件的
    queryset = models.Admin.objects.filter(**data_dict)

    # 分页
    page_object = Pagination(request, queryset)

    context = {
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 生成页码
    }
    return render(request, 'admin_list.html', context)


def admin_add(request):
    """ 添加管理员 """
    title = "添加管理员"
    # 如果是GET请求
    if request.method == "GET":
        form = AdminModelForm()
        return render(request, 'change.html', {"title": title, "form": form})
    # 如果是POST请求
    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        # 如果数据合法不为空,调用ModelForm类的save()函数自动保存到数据库
        form.save()
        return redirect("/admin/list/")
    # 校验失败，在页面上展示错误信息
    return render(request, 'change.html', {"title": title, "form": form})


def admin_edit(request, nid):
    """ 编辑管理员 """
    title = "编辑管理员"
    admin_object = models.Admin.objects.filter(id=nid).first()  # 先去数据库里检索这个数据是否存在
    if not admin_object:
        return redirect("/admin/list/")

    if request.method == "GET":
        form = AdminEditModelForm(instance=admin_object)
        return render(request, 'change.html', {"title": title, "form": form})

    form = AdminEditModelForm(data=request.POST, instance=admin_object)
    if form.is_valid():
        # 如果数据合法不为空,调用ModelForm类的save()函数自动保存到数据库
        form.save()
        return redirect("/admin/list/")
        # 校验失败，在页面上展示错误信息
    return render(request, 'change.html', {"title": title, "form": form})


def admin_delete(nid):
    """ 删除管理员 """
    models.Admin.objects.filter(id=nid).delete()
    return redirect('/admin/list')


def admin_reset(request, nid):
    """ 重置管理员密码 """

    admin_object = models.Admin.objects.filter(id=nid).first()  # 先去数据库里检索这个数据是否存在
    if not admin_object:
        return redirect("/admin/list/")
    title = "重置-{}密码".format(admin_object.username)

    if request.method == "GET":
        form = AdminResetModelForm()
        return render(request, 'change.html', {"title": title, "form": form})

    form = AdminResetModelForm(data=request.POST, instance=admin_object)
    if form.is_valid():
        # 如果数据合法不为空,调用ModelForm类的save()函数自动保存到数据库
        form.save()
        return redirect("/admin/list/")
        # 校验失败，在页面上展示错误信息
    return render(request, 'change.html', {"title": title, "form": form})
