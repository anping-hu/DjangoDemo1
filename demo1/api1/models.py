from django.db import models


# Create your models here.
class Admin(models.Model):
    """ 管理员表 """
    username = models.CharField(verbose_name='用户名', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=64)

    def __str__(self):
        return self.username


class Department(models.Model):
    """ 部门表 """
    title = models.CharField(verbose_name='标题', max_length=32)  # verbose_name 表示给字段加注解

    def __str__(self):
        return self.title


class Userinfo(models.Model):
    """ 员工表 """
    name = models.CharField(verbose_name='姓名', max_length=32)  # verbose_name 表示给字段加注解
    password = models.CharField(verbose_name='密码', max_length=64)
    age = models.IntegerField(verbose_name='年龄')
    account = models.DecimalField(verbose_name='账户余额', max_digits=10, decimal_places=2, default=0)
    # max_digits=10, decimal_places=2, default=0表示总共长度10，小数点后2位，默认值为0
    # create_time = models.DateTimeField(verbose_name='入职时间')  年月日时分秒
    create_time = models.DateField(verbose_name='入职时间')  # 年月日 修改了数据库models。py需要做更新makemigrations和migrate
    # 与部门表关联
    # to，与那张表关联
    # to_field，与表中那个字段关联
    # 这里的字段是depart，但是在数据库中是depart_id（django自动生成）
    # null=True, blank=True表示能制空，on_delete=models.SET_NULL表示如果部门表中的数据删除后制空
    depart = models.ForeignKey(verbose_name='部门id', to='Department', to_field='id', null=True, blank=True,
                               on_delete=models.SET_NULL)
    gender_choices = (
        (1, '男'),
        (2, '女'),
    )  # 定义一个男女选择元组
    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choices)


class PrettyNum(models.Model):
    """ 靓号表 """
    mobile = models.CharField(verbose_name='号码', max_length=11)
    price = models.IntegerField(verbose_name='价钱', default=0)
    level_choices = (
        (1, '一级'),
        (2, '二级'),
        (3, '三级'),
    )
    level = models.SmallIntegerField(verbose_name='级别', choices=level_choices, default=1)
    status_choices = (
        (1, '已占用'),
        (2, '未使用'),
    )
    status = models.SmallIntegerField(verbose_name='状态', choices=status_choices, default=2)


class Task(models.Model):
    """ 任务 """
    level_choices = (
        (1, "紧急"),
        (2, "重要"),
        (3, "临时"),
    )
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=1)
    title = models.CharField(verbose_name="标题", max_length=64)
    detail = models.TextField(verbose_name="详细信息")
    user = models.ForeignKey(verbose_name="负责人", to="Admin", on_delete=models.CASCADE)
    # on_delete=models.CASCADE表示级联删除


class Order(models.Model):
    """ 订单 """
    oid = models.CharField(verbose_name="订单号", max_length=64)
    title = models.CharField(verbose_name="商品名称", max_length=32)
    price = models.IntegerField(verbose_name='价钱', default=0)
    status_choices = (
        (1, '已支付'),
        (2, '待支付'),
    )
    status = models.SmallIntegerField(verbose_name='状态', choices=status_choices, default=2)
    admin = models.ForeignKey(verbose_name='管理员', to='Admin', on_delete=models.CASCADE)


class Boss(models.Model):
    """ 老板 """
    name = models.CharField(verbose_name="姓名", max_length=32)
    age = models.IntegerField(verbose_name="年龄")
    img = models.CharField(verbose_name="头像", max_length=128)


class City(models.Model):
    """ 城市 """
    name = models.CharField(verbose_name="名称", max_length=32)
    count = models.IntegerField(verbose_name="人口")

    # 本质上数据库也是CharField，自动保存数据。upload_to='city/'这个属性指，文件它会自动放到media目录下的city目录下，数据库里还是存储的文件路径
    img = models.FileField(verbose_name="Logo", max_length=128, upload_to='city/')