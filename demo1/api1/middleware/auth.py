from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect


class AuthMiddleware(MiddlewareMixin):
    # """
    #     自定义的中间件
    #     浏览器的请求（request）会先经过django中一个个中间件后才到后面的每一个视图函数（view）
    #     使用中间件需要在setting里的MIDDLEWARE列表中添加中间件的路径
    # """
    def process_request(self, request):
        # 0.排除那些不需要登录就能访问的页面
        #   request.path_info 获取当前用户请求的URL /login/
        if request.path_info in ["/login/", "/image/code/"]:
            return

        # 1.读取当前访问的用户的session信息，如果能读到，说明已登陆过，就可以继续向后走。
        info_dict = request.session.get("info")
        # print(info_dict)
        if info_dict:
            return

        # 2.没有登录过，重新回到登录页面
        return redirect('/login/')
