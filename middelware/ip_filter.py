import time
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse

class OverTime(MiddlewareMixin):
    def process_request(self, request):
        # 获取客户端IP地址
        IP = request.META.get('REMOTE_ADDR')
        # 获取该IP地址的值，如果没有，给一个默认列表[]
        lis = request.session.get(IP, [])
        # 获取当前时间
        curr_time = time.time()
        # 判断操作次数是否小于3次
        if len(lis) < 120:
            # 如果小于3次,添加本次操作时间
            lis.append(curr_time)
            # 保存
            request.session[IP] = lis
        else:
            # 如果本次操作时间减去第一次操作时间小于60秒,则不让其继续操作
            if time.time() - lis[0] < 20:
                return HttpResponse('操作过于频繁')
            else:
                # 如果大于60秒则交叉复制
                lis[0], lis[1], lis[2] = lis[1], lis[2], time.time()
                # 保存
                request.session[IP] = lis

    def process_response(self, request, response):
        return response
