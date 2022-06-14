from django.shortcuts import render, redirect
from api1 import models
from api1.utils.pagination import Pagination
from api1.utils.form import PrettyModelForm, PrettyEditModelForm


def pretty_list(request):
    """ 靓号列表 """

    data_dict = {}  # 默认为空字典 ，为空字典时 表示models.PrettyNum.objects.filter(**data_dict)搜索全部数据
    search_data = request.GET.get("q", '')  # 利用html的get请求得到http://127.0.0.1:8000/pretty/list/?q=99 中的q值，q没有值默认为空
    if search_data:  # search_data不为空时，将搜索框中的内容放入字典data_dict，为空不放
        data_dict["mobile__contains"] = search_data  # mobile__contains表示mobile这个字段包含

    # prettyinfo = models.PrettyNum.objects.filter(**data_dict).order_by("-level")[
    #              start:end]  # order_by("-level")根据级别倒序排序,[1,10]表示显示1至10条数据
    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-level")

    page_object = Pagination(request, queryset)  # Pagination自定义的分页类
    context = {
        "search_data": search_data,

        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
    }

    return render(request, 'pretty_list.html', context)


def pretty_add(request):
    """ 添加靓号 """
    if request.method == 'GET':
        form = PrettyModelForm()
        return render(request, 'pretty_add.html', {'form': form})
    # 用户POST提交数据，数据校验
    form = PrettyModelForm(data=request.POST)
    if form.is_valid():
        # 如果数据合法不为空,调用ModelForm类的save()函数自动保存到数据库
        form.save()
        return redirect("/pretty/list/")
    # 校验失败，在页面上展示错误信息
    return render(request, 'pretty_add.html', {'form': form})


def pretty_edit(request, nid):
    """ 编辑靓号 """
    row_obj = models.PrettyNum.objects.filter(id=nid).first()

    if request.method == 'GET':
        form = PrettyEditModelForm(instance=row_obj)  # 实例化,instance-实例，在modelForm中instance这个属性有值，它会默认显示拿到的值
        return render(request, 'pretty_edit.html', {'form': form})

    # 用户POST提交数据，数据校验
    form = PrettyEditModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        # 如果数据合法不为空,调用ModelForm类的save()函数自动保存到数据库
        form.save()
        return redirect("/pretty/list/")
        # 校验失败，在页面上展示错误信息
    return render(request, 'pretty_edit.html', {'form': form})


def pretty_delete(request, nid):
    """ 删除靓号 """
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect('/pretty/list')