from django import forms


class BootStrap:
    bootstrap_exclude_fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环ModelForm中的所有字段，给每个字段的插件设置
        for name, field in self.fields.items():
            if name in self.bootstrap_exclude_fields:
                continue
            # 字段中有属性，保留原来的属性，没有属性，才增加。
            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = field.label
            else:
                field.widget.attrs = {
                    "class": "form-control",
                    "placeholder": field.label
                }


class BootStrapModelForm(BootStrap, forms.ModelForm):
    pass


class BootStrapForm(BootStrap, forms.Form):
    pass

# from django import forms
#
#
# class BootStrapModelForm(forms.ModelForm):
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # 循环ModelForm中的所有字段，给每个字段的插件设置
#         for name, field in self.fields.items():
#             # 字段中有属性，保留原来的属性，没有属性，才增加。
#             if field.widget.attrs:
#                 field.widget.attrs["class"] = "form-control"
#                 field.widget.attrs["placeholder"] = field.label
#             else:
#                 field.widget.attrs = {
#                     "class": "form-control",
#                     "placeholder": field.label
#                 }


# 解释
# # 修改这个类的构造函数，继承父类的构造函数，在这里的作用是将页面上的插件input框添加class属性
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # 循环找到所有插件，添加class="form-control"
#         for name, field in self.fields.items():
#             '''
#             # 如果不想哪一个插件不用这个属性就跳过
#             if name == "password":
#                 continue
#             '''
#             field.widget.attrs = {"class": "form-control", "placeholder": field.label}
